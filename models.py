from typing import Optional
from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=500)
    status: bool = Field(default=False)


class TaskOut(BaseModel):
    task_id: int
    title: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=500)
    status: bool = Field(default=False)
