from pydantic import BaseModel
from typing import Literal
from enum import Enum

# Enum for difficulty levels
class Difficulty(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

# Enum for lesson topics
class Topic(str, Enum):
    PHYSICS = "Physics"
    CRYPTO = "Cryptocurrency"
    CODING = "Coding"

# Enum for animation types
class AnimationType(str, Enum):
    MASS_TO_LIGHT = "Mass to Light"
    EQUATION_REVEAL = "Equation Reveal"
    ENERGY_BURST = "Energy Burst"

# Pydantic model for lesson configuration
class LessonConfig(BaseModel):
    lesson: dict[str, str | int | Difficulty | Topic]
    content: dict[str, str]

    class Config:
        extra = "forbid"  # Prevent additional fields

    lesson: dict = {
        "title": Literal["E=MC² Basics", "Blockchain 101", "Python for Beginners"],
        "topic": Topic,
        "duration": Literal[15, 30, 45, 60],
        "difficulty": Difficulty
    }
    content: dict = {
        "introduction": Literal[
            "Explore a key concept.",
            "Learn foundational skills.",
            "Dive into an exciting topic."
        ],
        "explanation": Literal[
            "Understand the core idea.",
            "Break down complex concepts.",
            "See how it works in practice."
        ],
        "example": Literal[
            "Real-world application.",
            "Practical case study.",
            "Hands-on example."
        ]
    }

# Pydantic model for YouTube Shorts configuration
class ShortConfig(BaseModel):
    script: str
    animations: list[dict[str, str | int | AnimationType]]

    class Config:
        extra = "forbid"  # Prevent additional fields

    script: Literal[
        "Explain E=MC² in simple terms.",
        "Introduce blockchain basics.",
        "Teach a Python concept."
    ]
    animations: list[dict] = [
        {
            "description": AnimationType,
            "duration": Literal[5, 10, 15],
            "color": Literal["Blue", "Yellow", "White"]
        }
    ]