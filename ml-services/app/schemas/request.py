"""
Request schemas for API validation using Pydantic.
"""

from pydantic import BaseModel, Field, validator


class Query(BaseModel):
    """
    Request schema for video generation endpoint.
    
    Attributes:
        topic: Educational topic to generate video for
    """
    
    topic: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="The educational topic to generate a video for"
    )
    
    @validator('topic')
    def topic_not_empty(cls, v):
        """Validate that topic is not just whitespace"""
        if not v.strip():
            raise ValueError('Topic cannot be empty or whitespace')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "Binary Search Algorithm"
            }
        }


class RefinementRequest(BaseModel):
    """
    Request schema for video refinement endpoint.
    
    Attributes:
        feedback: User feedback for refining the video
    """
    
    feedback: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Feedback for refining the generated video (e.g., 'make it slower', 'darker background')"
    )
    
    @validator('feedback')
    def feedback_not_empty(cls, v):
        """Validate that feedback is not just whitespace"""
        if not v.strip():
            raise ValueError('Feedback cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "feedback": "Make the animations slower and use a darker background"
            }
        }