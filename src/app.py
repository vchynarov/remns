from werkzeug.wrappers import Request, BaseResponse as Response
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader 
import uuid
import base64
import time


### Load templates
admin_templates_path='/home/viktor/Projects/remns/templates/admin'
admin_env = Environment(loader=FileSystemLoader(admin_templates_path))

class EndPoint(object):
    def __init__(self, request, path_params):
        self.response = "Default response!"
        self.request = request
        self.path_params  = path_params
                
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def get_response(self):
        verb_map = {
            'GET' : self.get,
            'POST': self.post
        }
        return verb_map[self.request.method]()

class AdminEndPoint(EndPoint):
    def get_response(self):
        authenticated = session_cookies.get(self.request.cookies.get('remns_session_id'))
        login_page = isinstance(self, AdminLogin)
        if(authenticated):
            if(login_page):
                return redirect('/admin/posts')
            return EndPoint.get_response(self)
        elif(login_page):
            return EndPoint.get_response(self)
        else:
            return redirect('/admin')
                
remns_user = "viktor"
remns_password = "password"

# Store a timeout. This is meant for single users,
# a dict is more than sufficient.
session_cookies = {}

class ViewPost(EndPoint):
    def get(self):
        print "get request!"
        print self.request
        self.response = "getting posts"

    def post(self):
        print "post request!"
        print self.request
        self.response = "postin posts!"

class AdminLogin(AdminEndPoint):
    def get(self):
        print "get admin request!"
        template = admin_env.get_template('login.html')
        return Response(template.render(), mimetype="text/html")

    def generate_cookie(self):
       return base64.b64encode(str(uuid.uuid4())) 

    def post(self):
        login_form = self.request.form
        if login_form.has_key('admin-username') and login_form.has_key('admin-password'):
        
            submitted_user = self.request.form['admin-username']
            submitted_password = self.request.form['admin-password']
            if submitted_user == remns_user and submitted_password == remns_password:
                cookie = self.generate_cookie()
                session_cookies[cookie] = int(time.time())
                response = redirect(self.request.path)
                response.set_cookie('remns_session_id', cookie)
                return response

        return Response("BAD LOGIN!")


class AdminPost(AdminEndPoint):
    def get(self):
        print "in admin post"
        self.request = "YOOOO"

    def post(self):
        pass

class AdminAllPosts(AdminEndPoint):
    def get(self):
        return Response("Yo!") 

    def post(self):
        pass


class AdminCreatePost(AdminEndPoint):
    def get(self):
        template = admin_env.get_template('new_post.html')
        return Response(template.render(), mimetype="text/html")



url_map = Map([
    Rule('/', endpoint=ViewPost),
    Rule('/admin', endpoint=AdminLogin),
    Rule('/admin/posts', endpoint=AdminAllPosts),
    Rule('/admin/posts/new', endpoint=AdminCreatePost),
    Rule('/admin/posts/<int:id>', endpoint=AdminPost),
    Rule('/<int:year>/', endpoint=ViewPost),
    Rule('/<int:year>/<int:month>/', endpoint=ViewPost),
    Rule('/<int:year>/<int:month>/<int:day>/', endpoint=ViewPost),
    Rule('/<int:year>/<string:month>/<int:day>/', endpoint=ViewPost)
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

