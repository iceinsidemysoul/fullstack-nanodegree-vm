from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create
	# model = *ClassName(attributes...)
	# session.add(model)
	# session.commit()
# Read
	# models = session.query(*ClassName).all() or somthing else
# Update
	# model = session.query(*ClassName).all() or something to find model to update
	# model.attribute = new_data
	# session.add(model)
	# session.commit()
# Delete
	# model = session we want to deleted
	# session.delete(model)
	# session.commit()

class WebServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path.endswith("/restaurants/new"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>"
			output += "<h1>Make a New Restaurant</h1>"
			output += """<form action="/restaurants/new" method="POST" enctype="multipart/form-data"><input type="text" name="new_rest"><input type="submit" value="Create"></form>"""
			output += "</body></html>"
			self.wfile.write(output)
			return

		if self.path.endswith("/restaurants"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			restaurants = session.query(Restaurant).all()
			output = ""
			output += "<html><body>"
			output += "<h1><a href='/restaurants/new'>Create new restaurant here</a></h1>"
			for restaurant in restaurants:
				output += "<h3> %s </h3>" % restaurant.name
				output += "<a href='#'>edit</a><br>"
				output += "<a href='#'>delete</a>"
			output += "</body></html>"
			self.wfile.write(output)
			return

		if self.path.startswith('/restaurants') and self.path.endswith('edit'):
			self.send_response(200)
			self.send_header('content_type', 'text/html')
			self.end_headers()

			id = self.path.replace('/restaurants/', '')
			id = id.replace('/edit', '')
			id = int(id)
			restaurant = session.query(Restaurant).filter_by(id = id).first()
			
			output = ""
			output += "<html><body>"
			output += "<h1>Update Restaurant</h1>"

		else:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					print self.rfile
					print pdict
					fields = cgi.parse_multipart(self.rfile, pdict)
					new_restaurant = fields.get('new_rest')

					# save to database
					newRestaurant = Restaurant(name=new_restaurant[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()


			if self.path.endswith('/restaurants/new'):

		except:
			pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()