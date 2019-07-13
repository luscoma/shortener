"""A url shortner

Usage:
  shortener.py (-h | --help)
  shortener.py [options]

Options:
  --port=<port>         Set the port [default: 8080]
  --redis_host=<host>   Set the redis host name [default: localhost]
  -d    		Enable flasks debug mode
"""
import docopt
import flask
import re
import redis
import os
import socket
from url_normalize import url_normalize

# My stuff
from lib import data

flask_app = flask.Flask(__name__)
VERSION = 'Shortener 0.0.1'

PATH_REGEXP = re.compile('^\w+$')

def validate_path(path):
  if not PATH_REGEXP.match(path):
    return flask.abort(400)

@flask_app.route("/")
def home():
    visits = data.get_visits(flask_app.db)
    start = flask.request.args.get('start')
    count = flask.request.args.get('count', default=50, type=int)
    cursor, existing_redirects = data.list_redirects(flask_app.db, cursor=start, count=count)
    return flask.render_template('home.html', 
       hostname=socket.gethostname(),
       visits=visits,
       cursor=cursor,
       rows_per_page=count,
       existing_redirects=existing_redirects)

@flask_app.route("/admin")
@flask_app.route("/admin/<path>")
def view_path(path=None):
    path = path or flask.request.args.get('path')
    validate_path(path)
    redirection, visits  = data.get_redirect(flask_app.db, path) if path else None
    return flask.render_template('admin.html', 
       path=path,
       redirect_to=redirection,
       hostname=socket.gethostname(),
       visits=visits)

@flask_app.route("/admin", methods=["POST"])
@flask_app.route("/admin/<path>", methods=["POST"])
def update_path(path=None):
    path = path or flask.request.args.get('path')
    validate_path(path)
    action = flask.request.form.get('action')
    if not action:
      return flask.abort(500)

    if action.lower() == 'delete':
      data.remove_redirect(flask_app.db, path)
      # 303 See Other to redirect us back home
      return flask.redirect('/', code=303)
    elif action.lower() == 'update':  
      destination = flask.request.form['redirect_to']
      data.set_redirect(flask_app.db, path, url_normalize(destination, default_scheme='http'))
      # 303 See Other to redirect us back to the get page
      return flask.redirect('/admin/' + path, code=303)

@flask_app.route("/<path>")
@flask_app.route("/<path>/*")
def redirect_path(path):
    validate_path(path)
    redirection, _ = data.get_redirect(flask_app.db, path)
    if redirection:
      data.increment_visits(flask_app.db, path=path)
      return flask.redirect(redirection, code=302)
    return flask.redirect('/admin/' + path, code=302)


def main():
  flags = docopt.docopt(__doc__, version=VERSION)
  flask_app.db = redis.Redis(host=flags['--redis_host'], db=0, socket_connect_timeout=2, socket_timeout=2)
  flask_app.run(host='0.0.0.0', port=flags['--port'], debug=flags.get('-d', False))

if __name__ == "__main__":
  main()

