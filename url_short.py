import cgi
import random
import string
import re
import urllib
import wsgiref.handlers


from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class URLlist(db.Model):
  orginal = db.StringProperty(multiline=True)
  shortened = db.StringProperty(multiline=True)


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>
		<h1> URL Shortner</h1> 
		<body bgcolor="#00FFFF">

              <form action="/sign" method="post">
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="Short this URL"></div>
              </form>
            </body>
          </html>""")


class URLshortner(webapp.RequestHandler):
    def post(self):
        longurl = cgi.escape(self.request.get('content'))
        flag = 0
        urlobjects = URLlist.all()
        for urls in urlobjects:
          if longurl == urls.orginal:
            flag = 1
        if flag == 0:                  
          match=re.search(r'http://(.*)',cgi.escape(self.request.get('content')))
          strng=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(5))
          shorturl=strng
          newobject = URLlist(orginal= longurl, shortened= shorturl)
          newobject.put()
        else:
          listurl = []
          listurl = URLlist.gql("WHERE orginal= :orginal",
                                  orginal = longurl)
          shorturl = listurl[0].shortened
        link = 'http://nrjurlshort.appspot.com/' + shorturl
        self.response.out.write('<html><body><body bgcolor="00FFFF"><h2>OriginalURL is:</h2>')
        self.response.out.write('<a href=%s>%s</a>'%(longurl,longurl))
        self.response.out.write('<h2>Shortened URL is:</h2><pre>')
        self.response.out.write ('<a href=%s>%s</a>'%(link,link))
        self.response.out.write('</pre></body></html>')

class Redirect(webapp.RequestHandler):
    def get(self):
     val = self.request.path
     links = URLlist.all()
     for objects in links:
       if val[1:] == objects.shortened:
         self.redirect(objects.orginal)
     self.response.out.write(val)

      
      

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', URLshortner),
                                      (r'/[\w]+',Redirect)],
                                     debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
