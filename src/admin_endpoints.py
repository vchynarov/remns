from werkzeug.wrappers import Request, BaseResponse as Response
from endpoints import EndPoint
from werkzeug.utils import redirect
import uuid
import base64
import time
from json.encoder import JSONEncoder

json_encoder = JSONEncoder()
# Store a timeout. This is meant for single users,
# a dict is more than sufficient.
session_cookies = {}

def generate_cookie():
   return base64.b64encode(str(uuid.uuid4()))

class AdminEndPoint(EndPoint):
    def get_response(self, request):
        authenticated = session_cookies.get(request.cookies.get('remns_session_id'))
        login_page = isinstance(self, Login)
        if(authenticated):
            if(login_page):
                return redirect('/admin/posts')
            return super(AdminEndPoint, self).get_response(request)
        elif(login_page):
            return super(AdminEndPoint, self).get_response(request)
        else:
            return redirect('/admin')
                
class ViewPost(AdminEndPoint):
    def get(self, request):
        print "get request!"
        print request
        self.response = "getting posts"

    def post(self, request):
        print "post request!"
        print request
        self.response = "postin posts!"

class Login(AdminEndPoint):
    def __init__(self, template_env, username, password):
        super(Login, self).__init__(template_env)
        self.username = username
        self.password = password

    def get(self, request):
        template = self.template_env.get_template('login.html')
        return Response(template.render(), mimetype="text/html")

    def post(self, request):
        login_form = request.form
        if login_form.has_key('admin-username') and login_form.has_key('admin-password'):
        
            submitted_user = request.form['admin-username']
            submitted_password = request.form['admin-password']
            print submitted_password
            print submitted_user
            print self.username
            print self.password
            if submitted_user == self.username and submitted_password == self.password:
                cookie = generate_cookie()
                session_cookies[cookie] = int(time.time())
                response = redirect(request.path)
                response.set_cookie('remns_session_id', cookie)
                return response

        return Response("BAD LOGIN!")


class Post(AdminEndPoint):
    def get(self, request):
        return Response("yoo")

    def post(self, request):
        pass

class AllPosts(AdminEndPoint):
    def get(self, request):
        return Response("Yo!") 

    def post(self, request):
        print dir(request)
        print request.form
        print "Submitted!"
        if(True):
            response_json = {"status": "success", "id": 2}
        else:
            response_json = {"status": "error"}
        return Response(json_encoder.encode(response_json))


class CreatePost(AdminEndPoint):
    def get(self, request):
        template = self.template_env.get_template('new_post.html')
        return Response(template.render(), mimetype="text/html")


class AllCategories(AdminEndPoint):
    def get(self, request):
        return Response("..")

    def post(self, request):
        return Response("..")

class CreateCategory(AdminEndPoint):
    def get(self, request):
        return Response("...")




