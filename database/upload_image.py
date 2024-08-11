from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pymongo import DESCENDING
from bson import ObjectId
import dotenv
import os
from datetime import datetime, timedelta


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
        """
        This function retrieves the most recent asset that was uploaded within the last 5 minutes.
        If no assets meet this criteria, it returns the latest asset regardless of upload time.

        The process works as follows:
        1. Calculate the current time and the time 5 minutes ago.
        2. Fetch assets from the collection, sorted by their creation time in descending order (latest first).
        3. Iterate through the assets to find the first one uploaded within the last 5 minutes.
        4. Return the found asset.
        5. If no asset is found within the last 5 minutes, return the latest asset in the collection.

        This ensures that each new asset gets at least 5 minutes of display time before the next one is shown.
        """
        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(minutes=5)

        cursor = self.assets_collection.find().sort([("_id", DESCENDING)])

        async for asset in cursor:
            asset_time = datetime.strptime(
                str(asset["created_at"]), "%Y-%m-%d %H:%M:%S")
            if asset_time > five_minutes_ago: # If the asset was uploaded is within or just first after the last 5 minutes
                return asset

        # If no asset is found within the last 5 minutes, return the latest one
        latest_asset = await self.assets_collection.find_one(sort=[("_id", DESCENDING)])
        return latest_asset

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
    
    async def search_assets(self, disaster = None, device = None, modelNo = None, search = None, photo = None, video = None, audio = None, archival = None, document = None, portfolio = None, event = None, place = None, date = None, day = None):
        projection = {
            "_id": 1,
            "src": 1,
            "created_at": 1
        }

        search_query = []
        if disaster:
            search_query.append({"disaster": disaster})
        if device:
            search_query.append({"device": device})
        if modelNo:
            search_query.append({"cameraModel": modelNo})
        if search:
            search_query.append({"keywords": search})
        if photo:
            search_query.append({"photo": True})
        if video:
            search_query.append({"video": True})
        if audio:
            search_query.append({"audio": True})
        if archival:
            search_query.append({"archival": archival})
        if document:
            search_query.append({"document": document})
        # if portfolio:
        #     search_query.append({"portfolio": portfolio})
        if event:
            search_query.append({"title": event})
        if place:
            search_query.append({"place": place})
        if date:
            search_query.append({"date": date})
        if day:
            search_query.append({"day": day})
        

        assets = await self.assets_collection.find({"$and": search_query}, projection).to_list(length=None)
        return assets
    
    async def get_all_assets(self):
        projection = {
            "_id": 1,
            "src": 1,
            "forecastAndStories": 1,
        }

        assets = await self.assets_collection.find({}, projection).to_list(length=None)
        return assets
