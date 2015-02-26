from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from jinja2 import Environment, FileSystemLoader 
import config
import endpoints
import admin_endpoints
from db import get_session_maker
from models import PostService, TagService

admin_env = Environment(loader=FileSystemLoader(config.ADMIN_TEMPLATES_PATH))
SessionMaker = get_session_maker()
post_service = PostService(SessionMaker)
tag_service = TagService(SessionMaker)

## Instantiate controllers
view_post = endpoints.ViewPost(admin_env, post_service)
login = admin_endpoints.Login(admin_env, config.USER, config.PASSWORD )
create_post = admin_endpoints.CreatePost(admin_env, post_service)
create_tag = admin_endpoints.CreateTag(admin_env, tag_service)
edit_post = admin_endpoints.Post(admin_env, post_service)
admin_all_posts = admin_endpoints.AllPosts(admin_env, post_service)
admin_all_tags = admin_endpoints.AllTags(admin_env, tag_service)

url_map = Map([
    Rule('/admin', endpoint=login),
    Rule('/admin/posts', endpoint=admin_all_posts),
    Rule('/admin/posts/new', endpoint=create_post),
    Rule('/admin/posts/<int:id>', endpoint=edit_post),
    Rule('/admin/categories', endpoint=admin_all_tags),
    Rule('/admin/categories/new', endpoint=create_tag),
    Rule('/', endpoint=view_post),
    Rule('/<int:year>/', endpoint=view_post),
    Rule('/<int:year>/<int:month>/', endpoint=view_post),
    Rule('/<int:year>/<int:month>/<int:day>/', endpoint=view_post),
    Rule('/<int:year>/<string:month>/<int:day>/', endpoint=view_post)
])

@Request.application
def app(request):
    urls = url_map.bind_to_environ(request.environ)

    endpoint, args = urls.match()
    request.path_params = args
    if(endpoint):
        response = endpoint.get_response(request)
        return response
    else:
        print  "Essentially a 404"
        return Response('this is way cleaner')

