###################################################################
# To execute the script, run 'python example.py' (file index.html #
# must be in the same directory. Then, use your browser to go to  #
# http://localhost:8000/ and test how the service responds to     #
# different input data. Scenarios to check:                       #
# - LineID = 2, Name = a.s , ikea , κλπ                           #
# - StopId = 13027, Name = Kamara                                 #
# - ItineraryId = 81 , Direction = outward                        #
# - Line has stop: lineId = 2, stopid = 1051                      #
# - Admin: select * from vehicle                                  #
###################################################################

import cgi
import MySQLdb
from os import curdir, sep
try:
	from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # for python 2
except:
	from http.server import BaseHTTPRequestHandler, HTTPServer # for python 3

#db = MySQLdb.connect(host="your_hostname", user="your_username", passwd="your_password", db="publictransportdb")
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
		elif self.path.startswith("/images/"):  # Check if the request is for an image file
			filename = self.path.split("/")[-1]
			self.send_response(200)
			self.send_header('Content-type', 'image/jpeg')
			self.end_headers()
			with open(f'images/{filename}', 'rb') as f:
				self.wfile.write(f.read())
			return
		elif self.path.startswith("/css/"):  # Check if the request is for a .css file
			filename = self.path.split("/")[-1]
			self.send_response(200)
			self.send_header('Content-type', 'text/css')
			self.end_headers()
			with open(f'css/{filename}', 'r', encoding='utf-8') as f:
				self.wfile.write(f.read().encode())
			return
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
			self.path="/queries.html"
		try:
			f = open(curdir + sep + self.path) 
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.write_to_page(f.read())
			if "your_lineid" in form:
				c=0
				for x in str(form["your_lineid"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				if(c==0):
					self.write_to_page("<div class=\"gen\">The Line ID you gave is %s" % str(form["your_lineid"].value))
					query = "SELECT * FROM line WHERE lineid = " + form["your_lineid"].value
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<br>Database Data for the line: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
                    
			if "your_linename" in form:
				c=0
				for x in str(form["your_linename"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1   
				if(c==0):
					self.write_to_page("<div class=\"gen\">The Line name you gave is %s" % str(form["your_linename"].value))
					query = "SELECT * FROM line WHERE linename like \"%" + form["your_linename"].value+"%\" "
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<br>Database Data for the line: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
			if "your_stopid" in form:
				c=0
				for x in str(form["your_stopid"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				if(c==0):
					self.write_to_page("<div class=\"gen\">The Stop ID you gave is %s" % str(form["your_stopid"].value))
					query = "SELECT * FROM stop WHERE stopid = " + form["your_stopid"].value
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<br>Database Data for the Stop: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
			if "your_stopname" in form:
				c=0
				for x in str(form["your_stopname"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				if(c==0):
					self.write_to_page("<div class=\"gen\">The Stop Name you gave is %s" % str(form["your_stopname"].value))
					query = "SELECT * FROM stop WHERE stopname like \"%" + form["your_stopname"].value+"%\" "
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<br>Database Data for the Stop: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
			if "your_linestopid" in form:
				c=0
				for x in str(form["your_linestopid"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				if(c==0):
					self.write_to_page("<div class=\"gen\">The Line ID you gave is %s" % str(form["your_linestopid"].value))
					query = "SELECT * FROM line_has_stop WHERE lineid = " + form["your_linestopid"].value
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<br>Database Data for the line: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
			if "your_stoplineid" in form:
				c=0
				for x in str(form["your_stoplineid"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				if(c==0):
					self.write_to_page("<div class=\"gen\">The Stop ID you gave is %s" % str(form["your_stoplineid"].value))
					query = "SELECT * FROM line_has_stop WHERE stopid = " + form["your_stoplineid"].value
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<br>Database Data for the Stop: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
                        
			if ("your_itinerarylineid" and "your_itinerarydirection") in form:
				c=0
				for x in str(form["your_itinerarylineid"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				for x in str(form["your_itinerarydirection"].value):
					if (x==";"):
								self.write_to_page(" <div class=\"gen\">Please dont SQL Inject</div> ")
								c+=1             
				if(c==0):
					query = "SELECT ItineraryID,VehicleID FROM itinerary WHERE lineid =" + form["your_itinerarylineid"].value +" and direction=\"" + form["your_itinerarydirection"].value+"\""
					#self.write_to_page("<br>Query: [" + query + "]")
					self.write_to_page("<div class=\"gen\"><br>Database Data: <br> </div>")
					execute_command(cur, query)
					cur.execute(query)
					rows = cur.fetchall()
					column_names = [column[0] for column in cur.description]
					html_table = "<table>"
					html_table += "<tr>"
					for col in column_names:
						html_table += "<th>" + col + "</th>"
					html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					for row in rows:
						html_table += "<tr>"
						for col in row:
							html_table += "<td>" + str(col) + "</td>"
						html_table += "</tr>"
					html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
					html_table += "</table>"
					self.write_to_page("<div class=\"gen\">")
					self.write_to_page(html_table)
					self.write_to_page("</div>")
			if "your_itinerarylineid" in form and "your_itinerarydirection" not in form:
				self.write_to_page(" <div class=\"gen\">Please also provide the Direction</div> ")                
			if "your_drivervalues" in form:
				query ="INSERT INTO itinerary(ItineraryID,driverssn,lineid,direction,VehicleID) VALUES"+str(form["your_drivervalues"].value)
				#self.write_to_page("<br>Query: [" + query + "]")
				self.write_to_page("<div class=\"gen\"><br>Successfully added to Database!<br> </div>")
				execute_command(cur, query)
			if "your_conductorvalues" in form:
				query ="INSERT INTO Itinerary_Has_Conductor(ItineraryID,ConductorSSN,LineID,Direction) VALUES"+str(form["your_conductorvalues"].value)
				#self.write_to_page("<br>Query: [" + query + "]")
				self.write_to_page("<div class=\"gen\"><br>Successfully added to Database!<br> </div>")
				execute_command(cur, query)
			if "your_adminrest" in form:
				query = str(form["your_adminrest"].value)
				#self.write_to_page("<br>Query: [" + query + "]")
				self.write_to_page("<div class=\"gen\"><br>Successfully committed query<br> </div>")
				execute_command(cur, query)
			if "your_adminselect" in form:
				self.write_to_page("<div class=\"gen\">The query you gave is %s" % str(form["your_adminselect"].value))
				query = str(form["your_adminselect"].value)
				#self.write_to_page("<br>Query: [" + query + "]")
				self.write_to_page("<br>Database Data for your query: <br> </div>")
				execute_command(cur, query)
				cur.execute(query)
				rows = cur.fetchall()
				column_names = [column[0] for column in cur.description]
				html_table = "<table>"
				html_table += "<tr>"
				for col in column_names:
					html_table += "<th>" + col + "</th>"
				html_table += "</tr>"
				html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
				for row in rows:
					html_table += "<tr>"
					for col in row:
						html_table += "<td>" + str(col) + "</td>"
					html_table += "</tr>"
				html_table += "<tr><td colspan='" + str(len(column_names)) + "'><hr></td></tr>"
				html_table += "</table>"
				self.write_to_page("<div class=\"gen\">")
				self.write_to_page(html_table)
				self.write_to_page("</div>")
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