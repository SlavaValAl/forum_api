import http

from sanic.exceptions import InvalidUsage
from sanic.response import text
from sanic import Blueprint

from db.topic import get_topic_repo

topic_bp = Blueprint('topic')


@topic_bp.get('/topics')
async def get_all(request):
    topic_repo = get_topic_repo()
    topics = await topic_repo.get_all()
    return text(topics)


@topic_bp.post('/topics')
async def post(request):
    topic_repo = get_topic_repo()
    try:
        data = request.json
    except InvalidUsage as e:
        return text(
            'request body "%s" cannot be parsed. Err: %s' % (request.body, e),
            status=http.HTTPStatus.BAD_REQUEST,
        )
    await topic_repo.save(data)
    return text(data)


@topic_bp.get('/topic/<topic_id:string>')
async def get_one(request, topic_id):
    topic_repo = get_topic_repo()
    topic = await topic_repo.get(topic_id)
    return text(topic)


@topic_bp.put('/topic/<topic_id:string>')
async def put(request, topic_id):
    topic_repo = get_topic_repo()
    try:
        data = request.json
    except InvalidUsage as e:
        return text(
            'request body "%s" cannot be parsed. Err: %s' % (request.body, e),
            status=http.HTTPStatus.BAD_REQUEST,
        )
    updated_topic = await topic_repo.update(topic_id, data)
    return text(updated_topic)


@topic_bp.delete('/topic/<topic_id:string>')
async def delete(request, topic_id):
    topic_repo = get_topic_repo()
    await topic_repo.delete(topic_id)
    return text("ok")
