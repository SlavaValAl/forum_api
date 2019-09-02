from sanic import Sanic

from views.post import post_bp
from views.topic import topic_bp


def configure_routes(app: Sanic):
    app.blueprint(topic_bp)
    app.blueprint(post_bp)


if __name__ == '__main__':
    forum_app = Sanic()
    configure_routes(forum_app)
    forum_app.run(host='0.0.0.0', port=8000)
