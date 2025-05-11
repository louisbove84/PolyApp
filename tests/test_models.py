from generate_llm_yaml.models import LessonConfig, ShortConfig, Difficulty, Topic, AnimationType

def test_lesson_config():
    """Test that LessonConfig can be created with valid data."""
    data = {
        "lesson": {
            "title": "Python for Beginners",
            "topic": "Coding",
            "duration": 30,
            "difficulty": "Beginner"
        },
        "content": {
            "introduction": "Learn foundational skills.",
            "explanation": "Break down complex concepts.",
            "example": "Hands-on example."
        }
    }
    config = LessonConfig(**data)
    assert config.lesson["title"] == "Python for Beginners"
    assert config.lesson["topic"] == Topic.CODING
    assert config.lesson["difficulty"] == Difficulty.BEGINNER

def test_short_config():
    """Test that ShortConfig can be created with valid data."""
    data = {
        "script": "Explain E=MC² in simple terms.",
        "animations": [
            {
                "description": "Mass to Light",
                "duration": 10,
                "color": "Blue"
            }
        ]
    }
    config = ShortConfig(**data)
    assert config.script == "Explain E=MC² in simple terms."
    assert len(config.animations) == 1
    assert config.animations[0]["description"] == AnimationType.MASS_TO_LIGHT 