from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import endpoints
import admin_endpoints

url_map = Map([
    Rule('/', endpoint=endpoints.ViewPost),
    Rule('/admin', endpoint=admin_endpoints.Login),
    Rule('/admin/posts', endpoint=admin_endpoints.AllPosts),
    Rule('/admin/posts/new', endpoint=admin_endpoints.CreatePost),
    Rule('/admin/posts/<int:id>', endpoint=admin_endpoints.Post),
    Rule('/admin/categories', endpoint=admin_endpoints.AllCategories),
    Rule('/admin/categories/new', endpoint=admin_endpoints.CreateCategory),
    Rule('/<int:year>/', endpoint=endpoints.ViewPost),
    Rule('/<int:year>/<int:month>/', endpoint=endpoints.ViewPost),
    Rule('/<int:year>/<int:month>/<int:day>/', endpoint=endpoints.ViewPost),
    Rule('/<int:year>/<string:month>/<int:day>/', endpoint=endpoints.ViewPost)
])

@Request.application
def app(request):
    urls = url_map.bind_to_environ(request.environ)
    endpoint, args = urls.match()

    if(endpoint):
        controller = endpoint(request, args)
        response = controller.get_response()
        print response
        return response

    else:
        print  "Essentially a 404"
        return Response('this is way cleaner')

