from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pymongo import DESCENDING
from bson import ObjectId
import dotenv
import os



dotenv.load_dotenv()

MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Replace this with your MongoDB collection name for assets
ASSETS_COLLECTION_NAME = "assets"


class AssetDB:
    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION_URL)
        self.db = self.client[DATABASE_NAME]
        self.assets_collection = self.db.get_collection(ASSETS_COLLECTION_NAME)

    async def create_asset(self, asset_data):
        new_asset = await self.assets_collection.insert_one(asset_data)
        new_asset_id = str(new_asset.inserted_id)
        return new_asset_id
    
    async def get_scatter_assets(self):
        projection = {
            "_id": 1,
            "src": 1,
            "created_at": 1
        }

        assets = await self.assets_collection.find({}, projection).to_list(length=None)
        return assets

    async def get_asset(self, asset_id):
        asset = await self.assets_collection.find_one({"_id": ObjectId(asset_id)})
        return asset
    
    async def get_newest_asset(self):
        asset = await self.assets_collection.find_one(sort=[("_id", DESCENDING)]) # Find the newest document
        return asset
    
    async def get_user_assets(self, user_id):
        projection = {
            "_id": 1,
        }

        assets = await self.assets_collection.find({"user_id": user_id}, projection).to_list(length=None)
        return assets
    
    async def delete_asset(self, asset_id, user_id):
        await self.assets_collection.delete_one({"_id": ObjectId(asset_id), "user_id": user_id})
        return True
    
    async def get_latest_slogan(self):
        projection = {
            "forecastAndStories": 1,
            "src": 1
        }

        slogan = await self.assets_collection.find_one(sort=[("_id", DESCENDING)], projection=projection)
        return slogan
    