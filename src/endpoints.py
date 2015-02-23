from werkzeug.wrappers import Request, BaseResponse as Response

from jinja2 import Environment, FileSystemLoader 

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

class ViewPost(EndPoint):
    def get(self):
        print "get request!"
        print self.request
        self.response = "getting posts"

    def post(self):
        print "post request!"
        print self.request
        self.response = "postin posts!"


