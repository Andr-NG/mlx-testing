from typing import Optional
from pydantic import BaseModel, StrictStr, ConfigDict


class Data(BaseModel):
    email: StrictStr
    password: StrictStr
    workspace_id: Optional[str] = None
    folder_id: Optional[str] = None
    token: Optional[str] = None
    refresh_token: Optional[str] = None


class UserData(BaseModel):
    owner: Data
    manager: Data
    launcher: Data
    user: Data

    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
