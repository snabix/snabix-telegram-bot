from pydantic import BaseModel, ConfigDict, Field


class BackendHealthDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    ok: bool = True
    status: int = 200
    message: str = "Backend is available."


class BackendServiceIdentityDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    service: str
    mode: str
    version: str


class BackendStatsDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    users_total: int = Field(validation_alias="usersTotal")
    listings_total: int = Field(validation_alias="listingsTotal")
    listings_pending_review: int = Field(validation_alias="listingsPendingReview")
    listings_published: int = Field(validation_alias="listingsPublished")
    listings_archived: int = Field(validation_alias="listingsArchived")
