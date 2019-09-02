from motor.motor_asyncio import AsyncIOMotorClient

__mongo_client = None


def get_mongo_db():
    global __mongo_client
    if __mongo_client is None:
        # TODO: to settings
        __mongo_client = AsyncIOMotorClient('localhost', 27017)
    # TODO: db name to settings
    return __mongo_client['test_database']
