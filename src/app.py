from werkzeug.wrappers import Request, Response

class Resource(object):
    def __init__(self, request):
        print dir(request);
        
        
        

class PostCollection(Resource):
   pass 

class Post(Resource):
    pass

from werkzeug.routing import Map, Rule, NotFound, RequestRedirect

class EndPoint(object):
    def __init__(self, request, path_params):
        self.response = "Default response!"
        self.request = request
        self.path_params  = path_params
        print self.request.method
        verb_map = {
            'GET' : self.get,
            'POST': self.post

        }

        verb_map[self.request.method]()

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

    def get_response(self):
        return Response(self.response)

class ViewPost(EndPoint):
    def get(self):
        print "get request!"
        print self.request
        self.response = "getting posts"

    def post(self):
        print "post request!"
        print self.request
        self.response = "postin posts!"

    def get_response(self):
        print "getting response!"
        return Response(self.response)

class AdminLogin(object):
    def get(self):
        print "get admin request!"
        print self.request

    def post(self):
        print "post request!"
        print self.request

class AdminPost(object):
    def get(self):
        pass

    def post(self):
        pass


url_map = Map([
    Rule('/', endpoint=ViewPost),
    Rule('/<int:year>/', endpoint=ViewPost),
    Rule('/<int:year>/<int:month>/', endpoint=ViewPost),
    Rule('/<int:year>/<int:month>/<int:day>/', endpoint=ViewPost),
    Rule('/<int:year>/<string:month>/<int:day>/', endpoint=ViewPost)
])

@Request.application
def app(request):
#    print dir(request)

#    tokens = request.path.split("/")    
    urls = url_map.bind_to_environ(request.environ)
    endpoint, args = urls.match()
    if(endpoint):
        print endpoint
        print args
        print request.values

        controller = endpoint(request, args)
        print "initiated controller!"
        print controller.get_response()
        return controller.get_response()

    else:
        print  "Essentially a 404"
        return Response('this is way cleaner')

