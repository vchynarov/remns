from werkzeug.wrappers import Request, BaseResponse as Response


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
            'GET' : self.get,
            'POST': self.post
        }
        return verb_map[request.method](request)

class ViewPost(EndPoint):
    def get(self, request):
        print "get request!"
        print request
        self.response = "getting posts"

    def post(self, request):
        print "post request!"
        print request
        self.response = "postin posts!"


