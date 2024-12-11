from pydantic import BaseModel

from app.core.entities.company import Visibility


class CreateCompanySchema(BaseModel):
    name: str
    description: str


class EditCompanyNameSchema(BaseModel):
    new_name: str


class EditCompanyDescriptionSchema(BaseModel):
    new_description: str


class EditCompanyVisibilitySchema(BaseModel):
    visibility: Visibility
