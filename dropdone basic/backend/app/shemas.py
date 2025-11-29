
from pydantic import BaseModel
from typing import List, Any

class FunnelStep(BaseModel):
    label: str
    count: int
    rate: str
    color: str

class StatsResponse(BaseModel):
    total_calls: int
    total_messages: int
    total_contacts: int
    ai_success_rate: float
    funnel: List[FunnelStep]
    time_series: List[Any]
    comparison: List[Any]
    status_pie: List[Any]
    channel_bars: List[Any]
