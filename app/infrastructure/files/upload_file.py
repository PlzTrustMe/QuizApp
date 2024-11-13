from io import BytesIO

import pandas as pd

from app.core.interfaces.upload_file import UploadFile


class ExcelFileUpload(UploadFile):
    def upload_quiz(self, file: bytes) -> list[dict]:
        excel_file = BytesIO(file)

        quizzes_df = pd.read_excel(excel_file, sheet_name="Quizzes")
        questions_df = pd.read_excel(excel_file, sheet_name="Questions")
        answers_df = pd.read_excel(excel_file, sheet_name="Answers")

        quizzes_data = quizzes_df.to_dict(orient="records")
        questions_data = questions_df.to_dict(orient="records")
        answers_data = answers_df.to_dict(orient="records")

        questions_map = {}
        for question in questions_data:
            question_id = question["question_id"]
            question["answers"] = []
            questions_map[question_id] = question

        for answer in answers_data:
            question_id = answer["question_id"]
            questions_map.setdefault(question_id, {"answers": []})
            questions_map[question_id]["answers"].append(answer)

        quizzes_map = {}
        for quiz in quizzes_data:
            quiz_id = quiz["quiz_id"]
            quiz["questions"] = []
            quizzes_map[quiz_id] = quiz

        for question in questions_map.values():
            quiz_id = question["quiz_id"]
            quizzes_map.setdefault(quiz_id, {"questions": []})
            quizzes_map[quiz_id]["questions"].append(question)

        return quizzes_data
