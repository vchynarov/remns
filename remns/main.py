from werkzeug.wrappers import Request, BaseResponse as Response
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader 
from json import JSONDecoder
import config
import endpoints
import admin_endpoints
from db import get_session_maker
from models import PostService, TagService, TaggingService


json_decoder = JSONDecoder()
admin_env = Environment(loader=FileSystemLoader(config.ADMIN_TEMPLATES_PATH))
env = Environment(loader=FileSystemLoader(config.TEMPLATES_PATH))
SessionMaker = get_session_maker()

tag_service = TagService(SessionMaker)
post_service = PostService(SessionMaker)
tagging_service = TaggingService(SessionMaker)

## Instantiate controllers
login = admin_endpoints.Login(admin_env, config.USER, config.HASHED_PASSWORD)
create_post = admin_endpoints.CreatePost(admin_env, post_service)
edit_post = admin_endpoints.Post(admin_env, post_service, tag_service, tagging_service)
admin_all_posts = admin_endpoints.AllPosts(admin_env, post_service, tag_service, tagging_service)

all_tags = endpoints.AllTags(None, tag_service) # Does not need env, so not passing one in.
post_tags = endpoints.PostTags(None, post_service)
posts = endpoints.Posts(env, post_service)
single_post = endpoints.SinglePost(env, post_service)

url_map = Map([
    Rule('/admin/', endpoint=login),
    Rule('/admin/posts/', endpoint=admin_all_posts),
    Rule('/admin/posts/new/', endpoint=create_post),
    Rule('/admin/posts/<int:id>/', endpoint=edit_post),
    Rule('/tags/', endpoint=all_tags),
    Rule('/posts/<int:id>/tags/', endpoint=post_tags),
    Rule('/', endpoint=posts),
    Rule('/<int:year>/', endpoint=posts),
    Rule('/<int:year>/<int:month>/', endpoint=posts),
    Rule('/<int:year>/<int:month>/<string:web_title>/', endpoint=single_post)
])

@Request.application
def app(request):
    urls = url_map.bind_to_environ(request.environ)

    try:
        endpoint, args = urls.match()
    except RequestRedirect, e:
        return redirect(request.url + "/")

    request.path_params = args
    if request.data:
        try:
            request.data = json_decoder.decode(request.data)

        except ValueError:
            print "Couldn't convert to json."
    if endpoint:
        response = endpoint.get_response(request)
        return response
    else:
        return Response('404')

