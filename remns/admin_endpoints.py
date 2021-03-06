from werkzeug.wrappers import Request, BaseResponse as Response
from endpoints import EndPoint
from werkzeug.utils import redirect
import uuid
import base64
import time
import bcrypt
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

class Login(AdminEndPoint):
    def __init__(self, template_env, username, hashed_password):
        super(Login, self).__init__(template_env)
        self.username = username
        self.hashed_password = hashed_password

    def get(self, request):
        template = self.template_env.get_template('login.html')
        return Response(template.render(), mimetype="text/html")

    def post(self, request):
        login_form = request.form
        if 'admin-username' in login_form and 'admin-password' in login_form:
            submitted_user = request.form['admin-username']
            submitted_password = request.form['admin-password'].encode()  # Bcrypt doesn't work with Unicode strings
            if submitted_user == self.username and bcrypt.hashpw(submitted_password, self.hashed_password) == self.hashed_password:
                cookie = generate_cookie()
                session_cookies[cookie] = int(time.time())
                response = redirect(request.path)
                response.set_cookie('remns_session_id', cookie)
                return response
        return Response("BAD LOGIN!")

class Logout(AdminEndPoint):
    """
    Deletes the associated cookie in the cookie store.
    """
    def __init__(self):
        super(Logout, self).__init__(None)

    def get(self, request):
        cookie = request.cookies.get('remns_session_id')
        try:
            session_cookies.pop(cookie)
        except KeyError:
            pass
        return redirect("/admin/")

# /admin/posts/:id
class Post(AdminEndPoint):
    def __init__(self, template_env, post_service, tag_service, tagging_service):
        super(Post, self).__init__(template_env)
        self.post_service = post_service
        self.tag_service = tag_service
        self.tagging_service = tagging_service


    def get(self, request):
        template = self.template_env.get_template("edit_view.html")
        saved_post = self.post_service.find(request.path_params['id'])
        values = {
            "title_placeholder": saved_post.title,
            "post": saved_post
        }
        return Response(template.render(values), mimetype="text/html")

    def put(self, request):
        try:
            tag_ids = self.tag_service.initialize_tags(request.data["tags"])
            self.post_service.update(request.path_params["id"], request.data)
            self.tagging_service.set_tags(int(request.path_params["id"]), tag_ids)
            response_json = {"status": "success"}

        except Exception as e:
            print e
            response_json = {"status": "error"}

        return Response(json_encoder.encode(response_json), mimetype='application/json')

# /admin/posts
class AllPosts(AdminEndPoint):
    def __init__(self, template_env, post_service, tag_service, tagging_service):
        super(AllPosts, self).__init__(template_env)
        self.post_service = post_service
        self.tag_service = tag_service
        self.tagging_service = tagging_service

    def get(self, request):
        posts = self.post_service.get_all()
        template = self.template_env.get_template("all_posts.html")
        return Response(template.render(posts=posts), mimetype="text/html")

    
    def post(self, request):
        try:
            new_post = self.post_service.create(request.data)
            tag_ids = self.tag_service.initialize_tags(request.data["tags"])
            self.tagging_service.set_tags(new_post.id, tag_ids)
            response_json = {"status": "success", "id": new_post.id}
        except Exception as e:
            print e
            response_json = {"status": "error"}

        return Response(json_encoder.encode(response_json), mimetype='application/json')

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

