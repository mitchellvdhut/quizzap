from pydantic import ConfigDict, BaseModel, Field


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
    model_config = ConfigDict(validate_assignment=True)
