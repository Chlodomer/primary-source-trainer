from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class Event(BaseModel):
    id: str
    title: str
    year: int
    place: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    composition_info: Optional[str] = None  # 2-line description about the historical composition/sources


class TransmissionStep(BaseModel):
    via: str
    year: int
    type: Literal["copy", "summary", "translation", "compilation"]


class SourceNode(BaseModel):
    id: str
    type: Literal["text", "artifact"]
    title: str
    author_role: str
    year: int
    place: Optional[str] = None
    extant: bool
    transmission: List[TransmissionStep] = []
    description: Optional[str] = None


class Edge(BaseModel):
    from_id: str = Field(alias="from")
    to: str
    kind: str

    class Config:
        populate_by_name = True


class Topic(BaseModel):
    id: str
    label: str
    anchor: str  # ID of event or node that serves as anchor


class Scenario(BaseModel):
    id: str
    event: Event
    nodes: List[SourceNode]
    edges: List[Edge]
    topics: List[Topic]
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class Classification(BaseModel):
    node_id: str
    classification: Literal["primary", "secondary", "dependent_on_topic"]
    justification: str


class TopicToggle(BaseModel):
    topic_id: str


class Submission(BaseModel):
    scenario_id: str
    student_name: Optional[str] = "Anonymous"
    classifications: List[Classification]
    topic_id: str


class GradingResult(BaseModel):
    node_id: str
    student_answer: str
    correct_answer: str
    is_correct: bool
    points: int
    feedback: str


class ScenarioResult(BaseModel):
    scenario_id: str
    score: int
    max_score: int
    results: List[GradingResult]
    topic_label: str


class SessionSubmission(BaseModel):
    student_name: str
    student_email: Optional[str] = None
    scenario_results: List[ScenarioResult]
    timestamp: datetime = Field(default_factory=datetime.now)


class EmailResponse(BaseModel):
    success: bool
    message: str
