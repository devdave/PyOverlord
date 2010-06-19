import sys
import cherrypy
from controller.root import Root

try:
    from paste import evalexception
    from paste.httpexceptions import *
except ImportError:
    print "Missing paster, a non-critical dependancy that makes debugging easier"
    friendlyExceptions = False
else:
    friendlyExceptions = True
    
#@TODO perhaps stub out a library folder for this?    
import sqlite3
def sqlite3connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("./temp.sl3")
    cherrypy.log.error("Kicking off sqlite connection for thread %s" % thread_index)
    

#@todo stub out to a lib module?
def getConfig():
    port = 8080 if len(sys.argv) <= 1 else sys.argv[1]
    return {
        "global" : {
            "server.socket_port"   : int(port)
            , "server.thread_pool" : 10
            , "tools.sessions.on"  : True
            , 'request.throw_errors': True
            , 'log.screen': True
            , "engine.autoreload_on": True
        }
    }
    
    
if __name__ == "__main__":

    #@TODO read the src code for engine module to learn more
    cherrypy.engine.subscribe('start_thread', sqlite3connect)    
    cherrypy.config.update(getConfig())
    #@todo find out if there are negative connotations to going WSGI route with cherrypy
    # Create a WSGI application
    app = cherrypy.Application(Root())
    if friendlyExceptions:
        app.wsgiapp.pipeline.append(('paste_exc', evalexception.middleware.EvalException))
    cherrypy.quickstart(app)
    