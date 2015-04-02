from werkzeug.wrappers import Request
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
SessionMaker = get_session_maker()

tag_service = TagService(SessionMaker)
post_service = PostService(SessionMaker)
tagging_service = TaggingService(SessionMaker)

## Instantiate controllers
view_post = endpoints.ViewPost(admin_env, post_service)
login = admin_endpoints.Login(admin_env, config.USER, config.PASSWORD )
create_post = admin_endpoints.CreatePost(admin_env, post_service)
edit_post = admin_endpoints.Post(admin_env, post_service, tag_service, tagging_service)
admin_all_posts = admin_endpoints.AllPosts(admin_env, post_service, tag_service, tagging_service)
admin_all_tags = admin_endpoints.AllTags(admin_env, tag_service)

url_map = Map([
    Rule('/admin/', endpoint=login),
    Rule('/admin/posts/', endpoint=admin_all_posts),
    Rule('/admin/posts/new/', endpoint=create_post),
    Rule('/admin/posts/<int:id>/', endpoint=edit_post),
    Rule('/admin/tags/', endpoint=admin_all_tags),
    Rule('/', endpoint=view_post),
    Rule('/<int:year>/', endpoint=view_post),
    Rule('/<int:year>/<int:month>/', endpoint=view_post),
    Rule('/<int:year>/<int:month>/<int:day>/', endpoint=view_post),
    Rule('/<int:year>/<string:month>/<int:day>/', endpoint=view_post)
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
    if(endpoint):
        response = endpoint.get_response(request)
        return response
    else:
        print  "Essentially a 404"
        return Response('this is way cleaner')

