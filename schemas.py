from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=100)
class FeedbackRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=4000)
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)
