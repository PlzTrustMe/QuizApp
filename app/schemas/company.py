from pydantic import BaseModel


class CreateCompanySchema(BaseModel):
    name: str
    description: str
