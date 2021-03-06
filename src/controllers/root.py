
import cherrypy
from cherrypy import expose
import urllib2
import urllib
import StringIO
import gzip

from overlord import Overlord

class HTTPRewriteRedirect(urllib2.HTTPRedirectHandler):
    """Potentially deprecated before it started?"""
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
        
    
    
    
 