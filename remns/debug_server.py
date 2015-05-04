import os
from wsgiref import simple_server
from remns import main

os.chdir('./remns')

httpd = simple_server.make_server('', 3000, main.app)

httpd.serve_forever()


