# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime, timedelta

from .database import create_db_and_tables, engine
from .models import User, Contact, Call, Message, ActivityLog
from .schemas import (
    UserCreate, UserRead, Token,
    ContactCreate, ContactRead,
    CallCreate, CallRead,
    MessageCreate, MessageRead,
    ActivityRead, StatsResponse, FunnelStep
)
from .auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_user
)
from .seed import seed

app = FastAPI(title="Dropdone Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    try:
        seed()
    except Exception as e:
        print("Seed error:", e)

# ----- AUTH -----
@app.post("/auth/register", response_model=UserRead)
def register(payload: UserCreate):
    with Session(engine) as session:
        # uniqueness checks
        if session.exec(select(User).where(User.username == payload.username)).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        if session.exec(select(User).where(User.email == payload.email)).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(username=payload.username, email=payload.email, hashed_password=get_password_hash(payload.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.post("/auth/login", response_model=Token)
def login(form: dict):
    # Accept JSON { "username": "...", "password": "..." }
    username = form.get("username")
    password = form.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    # update last_login
    with Session(engine) as session:
        u = session.get(User, user.id)
        u.last_login = datetime.utcnow()
        session.add(u)
        session.commit()
    return {"access_token": access_token, "token_type": "bearer"}

# ----- Current user -----
@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# ----- Contacts -----
@app.post("/contacts", response_model=ContactRead)
def create_contact(payload: ContactCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        c = Contact(user_id=current_user.id, name=payload.name, email=payload.email, phone=payload.phone)
        session.add(c)
        session.commit()
        session.refresh(c)
        # log
        session.add(ActivityLog(user_id=current_user.id, action="create_contact", details=f"contact_id={c.id}"))
        session.commit()
        return c

@app.get("/contacts", response_model=list[ContactRead])
def list_contacts(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        stmt = select(Contact).where(Contact.user_id == current_user.id).order_by(Contact.created_at.desc())
        return session.exec(stmt).all()

# ----- Calls -----
@app.post("/calls", response_model=CallRead)
def create_call(payload: CallCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        c = Call(user_id=current_user.id, contact_id=payload.contact_id, timestamp=payload.timestamp, duration_sec=payload.duration_sec, status=payload.status, response_time=payload.response_time)
        session.add(c)
        session.commit()
        session.refresh(c)
        session.add(ActivityLog(user_id=current_user.id, action="create_call", details=f"call_id={c.id}"))
        session.commit()
        return c

@app.get("/calls", response_model=list[CallRead])
def list_calls(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        stmt = select(Call).where(Call.user_id == current_user.id).order_by(Call.timestamp.desc())
        return session.exec(stmt).all()

# ----- Messages -----
@app.post("/messages", response_model=MessageRead)
def create_message(payload: MessageCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        m = Message(user_id=current_user.id, contact_id=payload.contact_id, timestamp=payload.timestamp, channel=payload.channel, content=payload.content, response_time=payload.response_time)
        session.add(m)
        session.commit()
        session.refresh(m)
        session.add(ActivityLog(user_id=current_user.id, action="create_message", details=f"message_id={m.id}"))
        session.commit()
        return m

@app.get("/messages", response_model=list[MessageRead])
def list_messages(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        stmt = select(Message).where(Message.user_id == current_user.id).order_by(Message.timestamp.desc())
        return session.exec(stmt).all()

# ----- Activity (dev preview) -----
@app.get("/activity", response_model=list[ActivityRead])
def get_activity(limit: int = 20, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        stmt = select(ActivityLog).where(ActivityLog.user_id == current_user.id).order_by(ActivityLog.timestamp.desc()).limit(limit)
        return session.exec(stmt).all()

# ----- Stats (per-user) -----
@app.get("/stats", response_model=StatsResponse)
def get_stats(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        total_calls = session.exec(select(Call).where(Call.user_id == current_user.id)).count()
        total_messages = session.exec(select(Message).where(Message.user_id == current_user.id)).count()
        total_contacts = session.exec(select(Contact).where(Contact.user_id == current_user.id)).count()

        # simple funnel example (these should be computed from data in a real system)
        funnel = [
            {"label":"Leads","count": total_contacts, "rate": "100%", "color": "#09c2d7"},
            {"label":"Prospects","count": max(0, int(total_contacts*0.6)), "rate": "60%", "color": "#8b5cf6"},
            {"label":"Customers","count": max(0, int(total_contacts*0.3)), "rate": "30%", "color": "#10b981"},
        ]

        # time series: simple hourly buckets for the last 24h
        points = []
        base = datetime.utcnow()
        for hours in range(0,24,2):
            t = (base - timedelta(hours=hours)).strftime("%H:00")
            points.append({"time": t, "call": 0, "message": 0})
        points = list(reversed(points))

        # fill with real counts (coarse)
        calls = session.exec(select(Call).where(Call.user_id == current_user.id)).all()
        messages = session.exec(select(Message).where(Message.user_id == current_user.id)).all()
        # naive fill: put counts in buckets
        for c in calls:
            hour = c.timestamp.strftime("%H:00")
            for p in points:
                if p["time"] == hour:
                    p["call"] += 1
        for m in messages:
            hour = m.timestamp.strftime("%H:00")
            for p in points:
                if p["time"] == hour:
                    p["message"] += 1

        comparison = [
            {"name":"Avg Response Time","ai":2,"human":45},
            {"name":"Satisfaction Rate","ai":95,"human":85},
            {"name":"Calls Handled/Day","ai":50,"human":20},
        ]

        status_pie = [
            {"name":"Completed","value": session.exec(select(Call).where(Call.user_id==current_user.id).where(Call.status=="completed")).count()},
            {"name":"Missed","value": session.exec(select(Call).where(Call.user_id==current_user.id).where(Call.status=="missed")).count()}
        ]
        channel_bars = []
        chs = ["Email","WhatsApp","SMS","Chat"]
        for ch in chs:
            channel_bars.append({"channel": ch, "value": session.exec(select(Message).where(Message.user_id==current_user.id).where(Message.channel==ch)).count()})

        return {
            "total_calls": total_calls,
            "total_messages": total_messages,
            "total_contacts": total_contacts,
            "ai_success_rate": 98.5,
            "funnel": funnel,
            "time_series": points,
            "comparison": comparison,
            "status_pie": status_pie,
            "channel_bars": channel_bars
        }
