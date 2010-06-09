
import cherrypy
from cherrypy import expose
import urllib2
import urllib

class Overlord(object):
    
    @property    
    def host_name(self):
        return cherrypy.session.get("host_name", "ominian.com")
    
    @host_name.setter    
    def host_name(self, value):        
        cherrypy.session['host_name'] = value
        return value
            
    @property
    def host_ip(self):
        return cherrypy.session.get("host_ip", "69.163.238.103")
    
    @host_ip.setter
    def host_ip(self, value):
        cherrypy.session['host_ip'] = value
        return value
    
    @expose
    def index(self):
        
        return """<form action="/overlord/process" method="post" name="assignment">
                      <label>Desired hostname</label><br/>
                      <input name="host_name" value="%s" /> <br/>
                      
                      <label>IP address</label><br/>
                      <input name="host_ip" value="%s" /> <br/>
                      
                      <input type="submit">
                   </form>
               """ % (self.host_name, self.host_ip)
    @expose
    def process(self, host_name, host_ip):
        self.host_ip   = host_ip
        self.host_name = host_name
        raise cherrypy.HTTPRedirect("/")
        
    def __str__(self):
        return "Host: %s @ %s " % ( self.host_name, self.host_ip, )
    

class Root(object):
    
    
    overlord = Overlord()
    
    @property
    def count(self):
        cherrypy.session['count'] = cherrypy.session.get('count', 0) + 1
        return cherrypy.session['count']
    
    @expose
    def default(self, *args, **kwargs):
        if self.overlord.host_ip == "" or self.overlord.host_name == "":
            raise cherrypy.HTTPRedirect("/overlord")
                    
        
        
        
        return self.proxyCall(args, kwargs)
    
    def proxyCall(self, uriSegments, kwargs):
                    
        target = "http://%s%s" % ( self.overlord.host_ip, cherrypy.request.request_line.split(" ")[1])        
        
        requestArguments = dict()
        requestArguments['headers'] = cherrypy.request.headers        
        requestArguments['headers']["Host-name"] = self.overlord.host_name
        requestArguments['headers']["Host"] = self.overlord.host_name
        
        
        if cherrypy.request.method != "GET":
            requestArguments['data'] = urllib.urlencode(kwargs)
            
        request = urllib2.Request(target, **requestArguments)
                
        response = urllib2.urlopen(request)
        
        for k, v in response.headers.dict.items():
            cherrypy.response.headers[k] = v
        
        contentType = response.headers['content-type'].split(";")[0]
        charset = response.headers['content-type'].split("charset=")[-1] if response.headers['content-type'].find("charset=") >= 0 else None
                
        #TODO 
        if contentType.find("text/") >= 0:            
            payload = response.read()
            
            if charset:
                try:
                    payload = payload.decode(charset).encode("utf-8")
                except UnicodeDecodeError , e1:
                    cherrypy.log("Attempt 1 to decode bytestream failed: %s " % e1)
                    try:
                        payload = unicode(payload, charset)
                    except UnicodeDecodeError , e2:
                        cherrypy.log("Attempt 2 to decode bytestream failed %s" % e2)
                        
                
            return self.cleanOutput(payload )
        else:
            return response.read()
        
    
    def cleanOutput(self, payload):
        target = u"http://%s" % self.overlord.host_name
        cherrypy.log("%s" % payload.__class__)        
        cherrypy.log("Attempting to fix URLS for %s" % target )        
        payload = payload.replace(target, "wtf/")
        
        
        return  payload
        
    
    
    
 