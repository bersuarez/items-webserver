import sys
import cgi
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Restaurant, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# from http.server import BaseHTTPRequestHandler, HTTPServer



Base=declarative_base()

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = "" 
                output += "<a href = '/restaurants/new'> Make a new Restaurant </a></br></br></br>" 
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>" 
                    output += "<a href = '/restaurants/%s/edit'> Edit </a>"  %restaurant.id
                    output += "</br>" 
                    output += "<a href = '/restaurants/%s/delete'> Delete </a>"  %restaurant.id
                    output += "</br> </br>"
                output += "</body></html>"
                self.wfile.write(output)
                # self.wfile.write(output.encode())
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                # self.wfile.write(output.encode())
                return


            # if self.path.endswith("/restaurants/%s/edit" %self.path[13:14]): 
                # currentRestaurant = session.query(Restaurant).filter_by(id=self.path[13:14]).one()
            if self.path.endswith("/edit"):
                restaurantID=self.path.split("/")[2]
                currentRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>"%currentRestaurant.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" %restaurantID
                output += "<input name = 'updatedName' type = 'text' placeholder = 'New name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                # self.wfile.write(output.encode())
                return

            if self.path.endswith("/delete"):
                restaurantID=self.path.split("/")[2]
                currentRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s</h1>"%currentRestaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action ='/restarants/%s/delete'>" %restaurantID
                output += "<input type='submit' value='Delete'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                # self.wfile.write(output.encode())
                return


        except IOError:
            self.send_error(404,"File Not Found %s" % self.path)

#convert to python3!
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            
            if self.path.endswith("/edit"):
                restaurantID=self.path.split("/")[2]
                currentRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newName = fields.get('updatedName')
                    currentRestaurant.name=newName[0]
                    session.add(currentRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                
            if self.path.endswith("/delete"):
                ctype, pdict =cgi.parse_header(self.headers.getheader('content-type'))
                restaurantID=self.path.split("/")[2]
                currentRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                session.delete(currentRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except:
            pass



def main():
    try:
        port=5000#redirected to 8085 in vagrant file
        server_address = ('', port)
        print("Web server running on port %s" %port)
        httpd = HTTPServer(server_address, webserverHandler)
        httpd.serve_forever() 
    except KeyboardInterrupt: #when user hold ^C
        print("^C entered, stopping web server...")
        httpd.socket.close()


#immediately run the main method when Python interpreter executes scrypt        
if __name__ == '__main__':
    main()

