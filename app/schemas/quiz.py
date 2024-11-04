from pydantic import BaseModel


class AnswerSchema(BaseModel):
    text: str
    is_correct: bool = False


class QuestionSchema(BaseModel):
    title: str
    answers: list[AnswerSchema]


class CreateQuizSchema(BaseModel):
    company_id: int
    title: str
    description: str
    questions: list[QuestionSchema]


class EditQuizTitleSchema(BaseModel):
    new_title: str


class TakeQuizSchema(BaseModel):
    quiz_id: int


class SaveQuizResultSchema(BaseModel):
    participation_id: int
    correct_answers: int
