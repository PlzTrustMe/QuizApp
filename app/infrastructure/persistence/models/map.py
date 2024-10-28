from .company import map_companies_table
from .company_user import map_company_users_table
from .user import map_users_table


def map_tables() -> None:
    map_users_table()
    map_companies_table()
    map_company_users_table()
