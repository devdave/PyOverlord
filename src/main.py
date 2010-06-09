
import cherrypy
from root import Root
    
def getConfig():
    return {
        "global" : {
            "server.socket_port"   : 8080
            , "server.thread_pool" : 10
            , "tools.sessions.on"  : True
        }
    }
    
    
if __name__ == "__main__":
    
    cherrypy.quickstart(Root(), "/", config = getConfig() )