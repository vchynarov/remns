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
    def __init__(self, template_env, post_service):
        super(Login, self).__init__(self, template_env)
        self.post_service = post_service

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


# /admin/posts/:id
class Post(AdminEndPoint):
    def __init__(self, template_env, post_service):
        super(Post, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        template = self.template_env.get_template("edit_view.html")
        print request.path_params
        saved_post = self.post_service.find(request.path_params['id'])
        values = {
            "title_placeholder": saved_post.title,
            "post": saved_post
        }
        return Response(template.render(values), mimetype="text/html")

    def post(self, request):
        pass

# /admin/posts
class AllPosts(AdminEndPoint):
    def __init__(self, template_env, post_service):
        super(AllPosts, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        posts = self.post_service.get_all()
        template = self.template_env.get_template("all_posts.html")
        return Response(template.render(posts=posts), mimetype="text/html")

    def post(self, request):
        print dir(request)
        print request.form
        try:
            new_id = self.post_service.create(request.form)
            response_json = {"status": "success", "id": new_id}
        except Exception as e:
            print e
            response_json = {"status": "error"}

        return Response(json_encoder.encode(response_json))

# /admin/posts/new
class CreatePost(AdminEndPoint):
    def __init__(self, template_env, post_service):
        super(CreatePost, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        template = self.template_env.get_template("edit_view.html")
        values = {
            "title_placeholder": "Post title"
        }
        return Response(template.render(values), mimetype="text/html")


class AllTags(AdminEndPoint):
    def __init__(self, template_env, tag_service):
        super(AllTags, self).__init__(template_env)
        self.tag_service = tag_service

    def get(self, request):
        return Response("..")

    def post(self, request):
        return Response("..")

class CreateTag(AdminEndPoint):
    def __init__(self, template_env, tag_service):
        super(CreateTag, self).__init__(template_env)
        self.tag_service = tag_service

    def get(self, request):
        return Response("...")

