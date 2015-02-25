from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import endpoints
import admin_endpoints
import json

from jinja2 import Environment, FileSystemLoader 


admin_templates_path='/home/viktor/Projects/remns/templates/admin'
admin_env = Environment(loader=FileSystemLoader(admin_templates_path))

with open('config.json', 'r') as config_data_file:
    config_data = json.load(config_data_file)

admin_user = config_data['admin']['username']
admin_password = config_data['admin']['password']

## Instantiate controllers
view_post = endpoints.ViewPost(admin_env)
login = admin_endpoints.Login(admin_env, admin_user, admin_password )
create_post = admin_endpoints.CreatePost(admin_env)
create_category = admin_endpoints.CreateCategory(admin_env )
edit_post = admin_endpoints.Post(admin_env )
admin_all_posts = admin_endpoints.AllPosts(admin_env )
admin_all_categories = admin_endpoints.AllCategories(admin_env )

url_map = Map([
    Rule('/admin', endpoint=login),
    Rule('/admin/posts', endpoint=admin_all_posts),
    Rule('/admin/posts/new', endpoint=create_post),
    Rule('/admin/posts/<int:id>', endpoint=edit_post),
    Rule('/admin/categories', endpoint=admin_all_categories),
    Rule('/admin/categories/new', endpoint=create_category),
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

