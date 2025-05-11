from generate_llm_yaml.models import (
    AnimationType,
    Difficulty,
    LessonConfig,
    ShortConfig,
    Topic,
)

# Constants for test values
TEST_TITLE = "E=MC² Basics"
TEST_TOPIC = Topic.PHYSICS
TEST_DURATION = 15
TEST_DIFFICULTY = Difficulty.BEGINNER
TEST_INTRO = "Explore a key concept."
TEST_EXPLANATION = "Understand the core idea."
TEST_EXAMPLE = "Real-world application."
TEST_SCRIPT = "Explain E=MC² in simple terms."
TEST_ANIMATION_TYPE = AnimationType.MASS_TO_LIGHT
TEST_ANIMATION_DURATION = 5
TEST_ANIMATION_COLOR = "Blue"


def test_lesson_config() -> None:
    """Test creating a LessonConfig with valid data."""
    config = LessonConfig(
        lesson={
            "title": TEST_TITLE,
            "topic": TEST_TOPIC,
            "duration": TEST_DURATION,
            "difficulty": TEST_DIFFICULTY,
        },
        content={
            "introduction": TEST_INTRO,
            "explanation": TEST_EXPLANATION,
            "example": TEST_EXAMPLE,
        },
    )

    assert config.lesson["title"] == TEST_TITLE
    assert config.lesson["topic"] == TEST_TOPIC
    assert config.lesson["duration"] == TEST_DURATION
    assert config.lesson["difficulty"] == TEST_DIFFICULTY
    assert config.content["introduction"] == TEST_INTRO
    assert config.content["explanation"] == TEST_EXPLANATION
    assert config.content["example"] == TEST_EXAMPLE


def test_short_config() -> None:
    """Test creating a ShortConfig with valid data."""
    config = ShortConfig(
        script=TEST_SCRIPT,
        animations=[
            {
                "description": TEST_ANIMATION_TYPE,
                "duration": TEST_ANIMATION_DURATION,
                "color": TEST_ANIMATION_COLOR,
            }
        ],
    )

    assert config.script == TEST_SCRIPT
    assert len(config.animations) == 1
    assert config.animations[0]["description"] == TEST_ANIMATION_TYPE
    assert config.animations[0]["duration"] == TEST_ANIMATION_DURATION
    assert config.animations[0]["color"] == TEST_ANIMATION_COLOR
