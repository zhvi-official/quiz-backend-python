class UserRole(str, enum.Enum):
    AUTHOR = "author"
    PARTICIPANT = "participant"
    ADMIN = "admin"

class QuizDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuizStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class QuestionType(str, enum.Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    TEXT = "text"

class AttemptStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    ABANDONED = "abandoned"