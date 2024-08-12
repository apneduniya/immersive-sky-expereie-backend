from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from pydantic.networks import HttpUrl
from typing import Optional, Annotated


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class AssetBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None) # This will be aliased to `_id` when sent to MongoDB, but provided as `id` in the API requests and responses.
    title: Optional[str] = Field(None, description="Title of the event")
    disaster: Optional[str] = Field(None, description="Type of disaster")
    event: Optional[str] = Field(None, description="Event details")
    date: Optional[str] = Field(None, description="Date of the event")
    day: Optional[str] = Field(None, description="Day of the event")
    time: Optional[str] = Field(None, description="Time of the event")
    duration: Optional[str] = Field(None, description="Duration of the event")
    place: Optional[str] = Field(None, description="Place where the event occurred")
    affectedAreas: Optional[str] = Field(None, description="Areas affected by the event")
    geolocation: Optional[str] = Field(None, description="Geolocation in Longitude/Latitude")
    device: Optional[str] = Field(None, description="Device used")
    cameraModel: Optional[str] = Field(None, description="Model of the camera used")
    name: Optional[str] = Field(None, description="Name of the user if logged in")
    biography: Optional[str] = Field(None, description="Biography of the user if logged in")
    forecastAndStories: Optional[str] = Field(None, description="Forecast and stories related to the event")
    keywords: Optional[str] = Field(None, description="Keywords related to the event")
    imageSource: Optional[str] = Field(None, description="Source of the image")
    imageCopyright: Optional[str] = Field(None, description="Copyright information of the image")
    software: Optional[str] = Field(None, description="Software used for editing or processing")
    aspectRatio: Optional[str] = Field(None, description="Aspect ratio of the image or video")
    resolution: Optional[str] = Field(None, description="Resolution of the image or video")
    iso: Optional[str] = Field(None, description="ISO setting used in the camera")
    shutterSpeed: Optional[str] = Field(None, description="Shutter speed setting used in the camera")
    aperture: Optional[str] = Field(None, description="Aperture setting used in the camera")
    photo: Optional[bool] = Field(None, description="If the asset is a photo")
    video: Optional[bool] = Field(None, description="If the asset is a video")
    audio: Optional[bool] = Field(None, description="If the asset is an audio")
    sound: Optional[bool] = Field(None, description="If the asset is a sound")
    fileName: Optional[str] = Field(None, description="Name of the file")
    fileSize: Optional[str] = Field(None, description="Size of the file")
    fileType: Optional[str] = Field(None, description="Type of the file")
    archival: Optional[str] = Field(None, description="Archival information or status")
    document: Optional[str] = Field(None, description="Document related to the event or record")
    src: Optional[str] = Field(None, description="Image sources")
    user_id: Optional[PyObjectId] = Field(default="guest", alias="user_id", description="User ID if available") # This will be aliased to `user_id` when sent to MongoDB, but provided as `user_id` in the API requests and responses.
    created_at: Optional[str] = Field(None, description="Date and time of creation")

    model_config = ConfigDict(
        populate_by_name=True, # Populate the model with the values from the JSON by name (e.g. `{"name": "Jane Doe"}` will populate the `name` field)
        arbitrary_types_allowed=True, # Allow arbitrary types to be passed in the JSON (e.g. `datetime`, `ObjectId`, etc.)
        json_schema_extra={
            "example": {
                "_id": "5f4f7b4e5e9c4f001f6d8a4c",
                "title": "Flood in City A",
                "disaster": "Flood",
                "event": "Heavy rains caused flooding in several areas",
                "date": "2023-08-01",
                "day": "Tuesday",
                "time": "14:00",
                "duration": "3 hours",
                "place": "City A",
                "affectedAreas": "Downtown, Uptown",
                "geolocation": "34.052235, -118.243683",
                "device": "Drone",
                "cameraModel": "DJI Mavic Air 2",
                "name": "John Doe",
                "biography": "A journalist with 10 years of experience",
                "forecastAndStories": "Expected to rain for the next week",
                "keywords": "flood, city A, rain",
                "imageSource": "John Doe",
                "imageCopyright": "John Doe © 2023",
                "software": "Adobe Photoshop",
                "aspectRatio": "16:9",
                "resolution": "1920x1080",
                "iso": "100",
                "shutterSpeed": "1/100",
                "aperture": "f/2.8",
                "photo": True,
                "video": False,
                "audio": False,
                "sound": False,
                "fileName": "flood_city_a.jpg",
                "fileSize": "2MB",
                "fileType": "image/jpeg",
                "archival": "Archived",
                "document": "https://www.example.com/document.pdf",
                "src": "https://www.example.com/image.jpg",
                "user_id": "5f4f7b4e5e9c4f001f6d8a4c",
                "created_at": "2024-08-01 07:42:53"
            }
        },
    )


class AssetScatter(AssetBase):
    scale: float = Field(..., description="Scale value based on the creation date of the asset")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "5f4f7b4e5e9c4f001f6d8a4c",
                "src": "https://www.example.com/image.jpg",
                "scale": 0.5
            }
        },
    )

class AssetProcess(BaseModel):
    image_url: HttpUrl = Field(..., description="URL of the image to be processed")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "image_url": "https://www.example.com/image.jpg"
            }
        },
    )


