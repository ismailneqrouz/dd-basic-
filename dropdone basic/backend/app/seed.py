from sqlmodel import Session
from .database import engine
from .models import Call, Message, Contact
from datetime import datetime, timedelta
import random

def seed():
    with Session(engine) as session:
        # Escape reserved words using backticks for MySQL
        session.exec("DELETE FROM `call`")
        session.exec("DELETE FROM `message`")
        session.exec("DELETE FROM `contact`")

        for i in range(1, 6):
            session.add(Contact(name=f"Contact {i}", email=f"user{i}@example.com"))

        now = datetime.utcnow()

        for i in range(10):
            t = now - timedelta(hours=i * 2)
            session.add(Call(
                timestamp=t,
                duration_sec=random.uniform(30, 300),
                status=random.choice(["completed", "missed"]),
                response_time=random.uniform(1.0, 5.0)
            ))

        channels = ["Email", "WhatsApp", "SMS", "Chat"]
        for i in range(10):
            t = now - timedelta(hours=i * 3)
            session.add(Message(
                timestamp=t,
                channel=random.choice(channels),
                response_time=random.uniform(0.5, 4.0)
            ))

        session.commit()
        print("✔ Database seeded")
