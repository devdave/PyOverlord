
import cherrypy
from cherrypy import expose
import urllib2
import urllib
import StringIO
import gzip


class HTTPRewriteRedirect(urllib2.HTTPRedirectHandler):
    def __init__(self, sourceURL, targetURL):
        """
        Given the two URL, rewrite the redirect URL if it contains sourceURL with targetURL
        @param sourceURL a FQDN URL (ex http://remoteserver.com)
        @param targetURL a FQDN URL (ex http://myserver.com )
        """
        self.sourceURL = sourceURL
        self.targetURL = targetURL
    
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if newurl.find(self.sourceURL):
            newurl = newurl.replace(self.sourceURL, self.targetURL)
        
        urllib2.HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, headers, newurl)
        super(HTTPRewriteRedirect, self).redirect_request(self, req, fp, code, msg, headers, newurl)

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
        
        charset = None
        encoded = False
        
        for k, v in response.headers.dict.items():
            if k == "cotent-type":
                contentType = response.headers['content-type'].split(";")[0]
                charset = response.headers['content-type'].split("charset=")[-1] if response.headers['content-type'].find("charset=") >= 0 else None
            if k == "content-encoding":
                encoded = True
                continue
                #we're going to be de-compressing the stream, so prevent passing this one on
            
            cherrypy.response.headers[k] = v
        
        contentType = response.headers['content-type'].split(";")[0]
        
                
        #TODO 
        if contentType.find("text/") >= 0:
            payload = response.read()
            payload = self.decompressResponse(payload) if encoded == True else payload
            payload = payload.decode(charset) if charset else payload
                
            return self.cleanOutput(payload )
        else:
            return response.read()
    
    def decompressResponse(self, payload):
        compressed = StringIO.StringIO(payload)
        gzipObj = gzip.GzipFile(fileobj=compressed)
        return gzipObj.read();
    
    def cleanOutput(self, payload):
        target = u"http://%s" % self.overlord.host_name
        cherrypy.log("%s" % payload.__class__)        
        cherrypy.log("Attempting to fix URLS for %s" % target )        
        payload = payload.replace(target, u"http://127.0.0.1:8080")
        
        
        return  payload
        
    
    
    
 