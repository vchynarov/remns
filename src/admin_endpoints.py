from werkzeug.wrappers import Request, BaseResponse as Response
from endpoints import EndPoint
from werkzeug.utils import redirect
import uuid
import base64
import time
from json.encoder import JSONEncoder
from jinja2 import Environment, FileSystemLoader 


### Load templates
admin_templates_path='/home/viktor/Projects/remns/templates/admin'
admin_env = Environment(loader=FileSystemLoader(admin_templates_path))
json_encoder = JSONEncoder()


class AdminEndPoint(EndPoint):
    def get_response(self):
        authenticated = session_cookies.get(self.request.cookies.get('remns_session_id'))
        login_page = isinstance(self, Login)
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

class ViewPost(AdminEndPoint):
    def get(self):
        print "get request!"
        print self.request
        self.response = "getting posts"

    def post(self):
        print "post request!"
        print self.request
        self.response = "postin posts!"

class Login(AdminEndPoint):
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


class Post(AdminEndPoint):
    def get(self):
        print "in admin post"
        self.request = "YOOOO"

    def post(self):
        pass

class AllPosts(AdminEndPoint):
    def get(self):
        return Response("Yo!") 

    def post(self):
        print dir(self.request)
        print self.request.form
        print "Submitted!"
        if(True):
            response_json = {"status": "success", "id": 2}
        else:
            response_json = {"status": "error"}
        return Response(json_encoder.encode(response_json))


class CreatePost(AdminEndPoint):
    def get(self):
        template = admin_env.get_template('new_post.html')
        return Response(template.render(), mimetype="text/html")


class AllCategories(AdminEndPoint):
    def get(self):
        return Response("..")

    def post(self):
        return Response("..")

class CreateCategory(AdminEndPoint):
    def get(self):
        return Response("...")





