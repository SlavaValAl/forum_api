from typing import List, Dict

from bson import ObjectId
from pymongo import ReturnDocument

from drivers.mongo import get_mongo_db


class PostRepo(object):
    def __init__(self, db):
        self._db = db

    async def save(self, post: dict):
        return await self._db.posts.insert_one(post)

    async def get(self, post_id: str) -> dict:
        return await self._db.posts.find_one({"_id": ObjectId(post_id)})

    async def get_all(self) -> List[Dict]:
        return await self._db.posts.find().to_list(None)

    async def delete(self, post_id: str):
        await self._db.posts.delete_one({"_id": ObjectId(post_id)})

    async def delete_by_topic_id(self, topic_id: str):
        await self._db.posts.delete_many({"topic_id": ObjectId(topic_id)})

    async def update(self, post_id: str, data: Dict) -> Dict:
        return await self._db.posts.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )


__post_repo = None


def get_post_repo():
    global __post_repo
    if __post_repo is None:
        __post_repo = PostRepo(get_mongo_db())
    return __post_repo
