from werkzeug.wrappers import Request, BaseResponse as Response
from helpers import encode 


class EndPoint(object):
    def __init__(self, template_env):
        self.template_env = template_env
                
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

    def get_response(self, request):
        verb_map = {
            'GET': self.get,
            'POST': self.post,
            'PUT': self.put
        }
        return verb_map[request.method](request)

class Posts(EndPoint):
    def __init__(self, template_env, post_service):
        super(Posts, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        if request.path_params.get("year"):
            posts = self.post_service.filter(request.path_params.get("year"), request.path_params.get("month"))
        else:
            posts = self.post_service.get_all()
        template = self.template_env.get_template("multiple_view.html")
        return Response(template.render(posts=posts), mimetype="text/html")

class SinglePost(EndPoint):
    def __init__(self, template_env, post_service):
        super(SinglePost, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        post = self.post_service.retrieve(
            request.path_params.get("year"),
            request.path_params.get("month"),
            request.path_params.get("web_title"))
        template = self.template_env.get_template("single_view.html")
        return Response(template.render(post=post), mimetype="text/html")

class PostTags(EndPoint):
    def __init__(self, template_env, post_service):
        super(PostTags, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        post_tags = self.post_service.get_post_tags(request.path_params['id'])
        return Response(encode(post_tags), mimetype="application/json")


class AllTags(EndPoint):
    def __init__(self, template_env, tag_service):
        super(AllTags, self).__init__(template_env)
        self.tag_service = tag_service

    def get(self, request):
        tags = self.tag_service.get_all()
        return Response(encode(tags), mimetype="application/json")