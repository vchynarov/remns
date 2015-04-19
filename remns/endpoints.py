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

class ViewPost(EndPoint):
    def __init__(self, template_env, post_service):
        super(ViewPost, self).__init__(template_env)
        self.post_service = post_service

    def get(self, request):
        print "get request!"
        print request
        self.response = "getting posts"

    def post(self, request):
        print "post request!"
        print request
        self.response = "postin posts!"

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


