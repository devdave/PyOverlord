
import cherrypy
from root import Root
from paste import evalexception
from paste.httpexceptions import *
    
import sqlite3

def sqlite3connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("./temp.sl3")
    cherrypy.log.error("Kicking off sqlite connection for thread %s" % thread_index)
    
cherrypy.engine.subscribe('start_thread', sqlite3connect)

def getConfig():
    return {
        "global" : {
            "server.socket_port"   : 8080
            , "server.thread_pool" : 10
            , "tools.sessions.on"  : True
            , 'request.throw_errors': True
            , 'log.screen': True
            , "engine.autoreload_on": True
        }
    }
    
    
if __name__ == "__main__":
    
    cherrypy.config.update(getConfig())
    # Create a WSGI application
    app = cherrypy.Application(Root())
    app.wsgiapp.pipeline.append(('paste_exc', evalexception.middleware.EvalException))
    cherrypy.quickstart(app)
    