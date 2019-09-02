from typing import List, Dict

from bson import ObjectId
from pymongo import ReturnDocument

from db.post import get_post_repo
from drivers.mongo import get_mongo_db


class TopicRepo(object):
    def __init__(self, db):
        self._db = db
        self.post_repo = get_post_repo()

    async def save(self, topic: dict):
        return await self._db.topics.insert_one(topic)

    async def get(self, topic_id: str) -> dict:
        return await self._db.topics.find_one({"_id": ObjectId(topic_id)})

    async def get_all(self) -> List[dict]:
        return await self._db.topics.find().to_list(None)

    async def delete(self, topic_id: str):
        # TODO: wrap inside one transaction
        await self.post_repo.delete_by_topic_id(topic_id)
        await self._db.topics.delete_one({"_id": ObjectId(topic_id)})

    async def update(self, topic_id: str, data: Dict) -> Dict:
        return await self._db.topics.find_one_and_update(
            {"_id": ObjectId(topic_id)},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )


__topic_repo = None


def get_topic_repo():
    global __topic_repo
    if __topic_repo is None:
        __topic_repo = TopicRepo(get_mongo_db())
    return __topic_repo
