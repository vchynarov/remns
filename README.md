## The minimalistic yet logically blog built with Werkzeug ##

Minimalistic is nice but sometimes it gets too minimalistic, ya dig?
For instance, Markdown is a cool idea for blogs, but the problem is if 
you just store it as a static files then how do you do efficient querying 
of documents? It should make more sense to just use a caching layer on
top of a SQL database using something like SQLAlchemy.

## Usage ##

To use this to set-up a blog, please ensure you have the following things first:
* WSGI-compatible webserver. Something such as uWSGI, gunicorn; things capable of running a WSGI app.
* A database set-up and an appropriate driver downloaded. remns uses SQLAlchemy so anything popular should work.
* Set up a virtual env to isolate the above dependencies.

```pip install remns```

### Creating your first blog ###
    
    * Go into a directory such as /srv/http, or /var/www
    * After installing please run `remns [blogname]` to create a new directory to host your blog.
    * Run `pip install [driver] && pip install [server]` to install a SQL driver and WSGI app server.
    * Edit your config.yaml to update your author information and database connection info.
    * The WSGI app is available as main:app from your blog directory. 

## Development ##

* Clone the repository.
* `npm install`
* `bower install`
* `gulp`

Gulp is used build the static assets (HTML/CSS) required for the admin panel.
Run `gulp` without options to build everything.
