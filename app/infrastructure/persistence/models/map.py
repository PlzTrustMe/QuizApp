from .company import map_companies_table
from .company_user import map_company_users_table
from .invite import map_invitations_table, map_user_requests_table
from .quiz import map_answers_table, map_questions_table, map_quizzes_table
from .user import map_users_table


def map_tables() -> None:
    map_users_table()
    map_companies_table()
    map_company_users_table()
    map_invitations_table()
    map_user_requests_table()
    map_quizzes_table()
    map_questions_table()
    map_answers_table()
