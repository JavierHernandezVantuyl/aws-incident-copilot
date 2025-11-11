from __future__ import annotations
from pydantic import BaseModel
from typing import List


class Incident(BaseModel):
    id: str
    title: str
    severity: str  # LOW/MEDIUM/HIGH/CRITICAL
    resource: str
    description: str
    suggested_fix: str
    evidence_files: List[str] = []
