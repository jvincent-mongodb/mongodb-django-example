from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

GRID_FS_CONNECTION_STRING = "mongodb+srv://jeffreyvincent:QmxTvZAjCMJiuOVQ@cluster0.epkne.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class MongoDBConnection():
    def __init__(self):
        self.client = AsyncIOMotorClient(GRID_FS_CONNECTION_STRING)
        self.db = self.client.example_video_stream
        self.user_collection = self.db.user_collection
        self.fs = AsyncIOMotorGridFSBucket(self.db)
