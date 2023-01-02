###################### SQL INJECTION EXAMPLE ######################
# Caution: this script is for demonstration purpose only! This is #
# obviously not the way one should do stuff to create a server in #
# python and connect MySQL to  it. There are important security   #
# issues in this script, thus it is useful only for injections.   #
###################################################################
# Running this script requires installing the MySQLdb lib, which  #
# can be installed using the command: pip install mysqlclient     #
###################################################################
# To execute the script, run 'python example.py' (file index.html #
# must be in the same directory. Then, use your browser to go to  #
# http://localhost:8000/ and test how the service responds to     #
# different input data. Scenarios to check:                       #
# - Id = 8, Name = (whatever)                                     #
# - Id = (empty), Name = Kylie Minogue                            #
# - Id = 0 or 1=1, Name = (whatever)                              #
# - Id = (empty), Name = " or ""="                                #
# - Id = 0; DROP TABLE performers_tracks, Name = (whatever)       #
###################################################################

import cgi
import MySQLdb
from os import curdir, sep
try:
	from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # for python 2
except:
	from http.server import BaseHTTPRequestHandler, HTTPServer # for python 3

db = MySQLdb.connect(host="localhost", user="student", passwd="student", db="student")
cur = db.cursor()

def execute_command(cursor, sql_command):
	for statement in sql_command.split(';'):
		if len(statement) > 0:
			cursor.execute(statement + ';')

class myHandler(BaseHTTPRequestHandler):
	def write_to_page(self, text):
		try:
			self.wfile.write(text) # for python 2
		except:
			self.wfile.write(str(text).encode()) # for python 3

	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		try:
			f = open(curdir + sep + self.path) 
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.write_to_page(f.read().encode())
			f.close()
			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		if self.path=="/":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
						environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']})
			self.path="/index.html"
		try:
			f = open(curdir + sep + self.path) 
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.write_to_page(f.read())
			if "your_id" in form:
				self.write_to_page("The performer id you gave is %s" % str(form["your_id"].value))
				query = "SELECT * FROM performers WHERE id = " + form["your_id"].value
				#self.write_to_page("<br>Query: [" + query + "]")
				self.write_to_page("<br>Database Data for the performer: <br>")
				execute_command(cur, query)
				for row in cur.fetchall():
					self.write_to_page(row)
					self.write_to_page("<br>")
			else:
				self.write_to_page("The performer you gave is %s" % form["your_name"].value)
				query = "SELECT * FROM performers WHERE name = \"" + form["your_name"].value + "\""
				#self.write_to_page("<br>Query: [" + query + "]")
				self.write_to_page("<br>Database Data for the performer: <br>")
				execute_command(cur, query)
				for row in cur.fetchall():
					self.write_to_page(row)
					self.write_to_page("<br>")
			f.close()
			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	server = HTTPServer(('', 8000), myHandler)
	print('Started httpserver on port 8000')
	server.serve_forever()
except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()

db.close()

