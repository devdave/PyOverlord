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
