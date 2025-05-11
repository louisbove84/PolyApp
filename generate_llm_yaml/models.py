from enum import Enum
from typing import Literal, TypedDict, Union

from pydantic import BaseModel


class Difficulty(str, Enum):
    """Enum for difficulty levels to ensure consistent options."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class Topic(str, Enum):
    """Enum for lesson topics."""

    PHYSICS = "Physics"
    CRYPTO = "Cryptocurrency"
    CODING = "Coding"


class LessonDict(TypedDict):
    title: Literal["E=MC² Basics", "Blockchain 101", "Python for Beginners"]
    topic: Topic
    duration: Literal[15, 30, 45, 60]
    difficulty: Difficulty


class ContentDict(TypedDict):
    introduction: Literal[
        "Explore a key concept.",
        "Learn foundational skills.",
        "Dive into an exciting topic.",
    ]
    explanation: Literal[
        "Understand the core idea.",
        "Break down complex concepts.",
        "See how it works in practice.",
    ]
    example: Literal[
        "Real-world application.", "Practical case study.", "Hands-on example."
    ]


class LessonConfig(BaseModel):
    """Pydantic model for lesson configuration."""

    lesson: LessonDict = {
        "title": "E=MC² Basics",
        "topic": Topic.PHYSICS,
        "duration": 15,
        "difficulty": Difficulty.BEGINNER,
    }
    content: ContentDict = {
        "introduction": "Explore a key concept.",
        "explanation": "Understand the core idea.",
        "example": "Real-world application.",
    }

    class Config:
        """Pydantic config."""

        extra = "forbid"  # Prevent additional fields


class AnimationType(str, Enum):
    """Enum for animation types."""

    MASS_TO_LIGHT = "Mass to Light"
    EQUATION_REVEAL = "Equation Reveal"
    ENERGY_BURST = "Energy Burst"


class AnimationDict(TypedDict):
    description: AnimationType
    duration: Literal[5, 10, 15]
    color: Literal["Blue", "Yellow", "White"]


class ShortConfig(BaseModel):
    """Pydantic model for YouTube Shorts configuration."""

    script: Literal[
        "Explain E=MC² in simple terms.",
        "Introduce blockchain basics.",
        "Teach a Python concept.",
    ] = "Explain E=MC² in simple terms."
    animations: list[AnimationDict] = [
        {
            "description": AnimationType.MASS_TO_LIGHT,
            "duration": 5,
            "color": "Blue",
        }
    ]

    class Config:
        """Pydantic config."""

        extra = "forbid"  # Prevent additional fields
