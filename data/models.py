from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class User(BaseModel):
    id: int | None
    email: str
    username: str
    password: str
    is_admin: bool = False

    @classmethod
    def from_query_result(cls, id, email, username, password):
        return cls(
            id=id,
            email=email,
            username=username,
            password=password
        )


class LoginData(BaseModel):
    username: str
    password: str
