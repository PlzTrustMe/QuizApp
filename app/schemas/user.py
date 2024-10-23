from typing import Self

from pydantic import BaseModel, model_validator


class SignUpSchema(BaseModel):
    email: str
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1, pw2 = self.password, self.password2

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Passwords do not match")

        return self


class SignInSchema(BaseModel):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserDetail(BaseModel):
    full_name: str
    email: str
