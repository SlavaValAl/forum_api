import http

from sanic.exceptions import InvalidUsage
from sanic.response import text
from sanic import Blueprint

from db.post import get_post_repo

post_bp = Blueprint('post')


@post_bp.get('/posts')
async def get_all(request):
    post_repo = get_post_repo()
    posts = await post_repo.get_all()
    return text(posts)


@post_bp.post('/posts')
async def post(request):
    """
    :param request:
    :return:

    post_id should be included inside post body
    """
    post_repo = get_post_repo()
    try:
        post = request.json
    except InvalidUsage as e:
        return text(
            'request body "%s" cannot be parsed. Err: %s' % (request.body, e),
            status=http.HTTPStatus.BAD_REQUEST,
        )
    post = await post_repo.save(post)
    return text(post)


@post_bp.get('/post/<post_id:string>')
async def get_one(request, post_id):
    post_repo = get_post_repo()
    post = await post_repo.get(post_id)
    return text(post)


@post_bp.put('/post/<post_id:string>')
async def put(request, post_id):
    post_repo = get_post_repo()
    try:
        data = request.json
    except InvalidUsage as e:
        return text(
            'request body "%s" cannot be parsed. Err: %s' % (request.body, e),
            status=http.HTTPStatus.BAD_REQUEST,
        )
    updated_post = await post_repo.update(post_id, data)
    return text(updated_post)


@post_bp.delete('/post/<post_id:string>')
async def delete(request, post_id):
    post_repo = get_post_repo()
    await post_repo.delete(post_id)
    return text("ok")
