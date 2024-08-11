from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status
from models.users import UserBase
from models.upload_image import AssetBase, AssetScatter
from database.upload_image import AssetDB
import datetime
from utils.auth import (
    get_current_active_user
)
from utils.scale_image import get_scale_value
import requests
from utils.image_edit import image_to_base64, process_image
from PIL import Image
from io import BytesIO
import numpy as np
from pydantic.networks import HttpUrl


router = APIRouter()
asset_db = AssetDB()


@router.post('/create', response_description="Create new asset", status_code=status.HTTP_201_CREATED)
async def create_asset(asset: AssetBase = Body(...), current_user: UserBase = Depends(get_current_active_user)):

    asset.user_id = current_user["_id"]
    asset.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_asset = await asset_db.create_asset(asset.model_dump(by_alias=True, exclude=["id"]))
    return new_asset


@router.get("/new", response_description="Get first new asset", status_code=status.HTTP_200_OK)
async def get_new_asset():
    asset = await asset_db.get_newest_asset()

    return AssetBase(**asset).model_dump(include=("src", "keywords", "geolocation"))


@router.get('/scatter', response_description="Get all assets for scatter page", status_code=status.HTTP_200_OK)
async def get_assets_scatter():
    assets = await asset_db.get_scatter_assets()

    scatter_assets = []
    for asset in assets:
        asset["scale"] = get_scale_value(asset["created_at"])
        scatter_assets.append(AssetScatter(**asset).model_dump(by_alias=True, include=["src", "scale", "id"]))

    return scatter_assets


@router.get('/id/{asset_id}', response_description="Get asset by ID", status_code=status.HTTP_200_OK)
async def get_asset(asset_id: str):
    asset = await asset_db.get_asset(asset_id)
    return AssetBase(**asset).model_dump(by_alias=True)


@router.delete('/id/{asset_id}', response_description="Delete asset by ID", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(asset_id: str, current_user: UserBase = Depends(get_current_active_user)):
    # Fetch the asset to ensure it exists and the user is authorized to delete it
    asset = await asset_db.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    asset = AssetBase(**asset)
    
    if str(asset.user_id) != str(current_user["_id"]):
        print(asset.user_id, current_user["_id"])
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this asset")
    
    # Proceed with deletion
    await asset_db.delete_asset(asset_id, current_user["_id"])
    return {"message": "Asset deleted successfully"}


@router.get('/me', response_description="Get all assets for user", status_code=status.HTTP_200_OK)
async def get_user_assets(current_user: UserBase = Depends(get_current_active_user)):
    assets = await asset_db.get_user_assets(current_user["_id"])

    return [AssetBase(**asset).model_dump(by_alias=True, include=["id"]) for asset in assets]


@router.get('/slogan', response_description="Get latest slogan", status_code=status.HTTP_200_OK)
async def get_latest_slogan():
    slogan = await asset_db.get_latest_slogan()

    return AssetBase(**slogan).model_dump(by_alias=True, include=["forecastAndStories", "src"])


@router.get('/search/', response_description="Search assets", status_code=status.HTTP_200_OK)
async def search_assets(disaster: str = None, device: str = None, modelNo: str = None, search: str = None, photo: bool = None, video: bool = None, audio: bool = None, archival: str = None, document: str = None, portfolio: str = None, event: str = None, place: str = None, date: str = None, day: str = None):
    assets = await asset_db.search_assets(disaster, device, modelNo, search, photo, video, audio, archival, document, portfolio, event, place, date, day)

    if not assets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assets found")

    scatter_assets = []
    for asset in assets:
        asset["scale"] = get_scale_value(asset["created_at"])
        scatter_assets.append(AssetScatter(**asset).model_dump(by_alias=True, include=["src", "scale", "id"]))

    return scatter_assets


@router.post("/process_image", response_description="Process image from URL", status_code=status.HTTP_200_OK)
async def process_image_endpoint(image_url: HttpUrl):
    # Get the image from the URL
    response = requests.get(image_url)
    img_array = np.array(Image.open(BytesIO(response.content)))

    # Process the image
    processed_img = process_image(img_array)

    # Convert the processed image to base64
    img_base64 = image_to_base64(processed_img)

    return {"image_base64": img_base64}


@router.get("/all", response_description="Get all assets", status_code=status.HTTP_200_OK)
async def get_all_assets():
    assets = await asset_db.get_all_assets()

    return [AssetBase(**asset).model_dump(by_alias=True, include=["src", "id", "forecastAndStories"]) for asset in assets]

