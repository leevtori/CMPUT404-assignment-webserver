#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode('utf-8')
        string_list = self.data.split(' ')     # Split request from spaces
 
        method = string_list[0] # First string is a method
        request_path = string_list[1] #Second string is requesting page
        print("method is: " + method)
        print("file : " + request_path)
        
        file_path=""
        er_301 = False

        if (method != 'GET'):
            header = "HTTP/1.1 405 Method not allowed\n\n"
            response = '''<html>
                          <body>
                            <center>
                             <h3>Error 405: Method not allowed</h3>
                             <p>Python HTTP Server</p>
                            </center>
                          </body>
                        </html>
            '''.encode('utf-8')

        if (request_path == "/"):
            file_path = "index.html"
        elif (request_path[-1] == '/'):
            # we know it's a directory, to take the abs path
            file_path = os.path.abspath(request_path)
            file_path += "/index.html"
        else:
            file_path = os.path.abspath(request_path)
            er_301 = True
       # if (request_path == "/deep" or request_path == "/deep/"):
        #    request_path = "deep/index.html"

        try: 
            if (er_301):
                header = "HTTP/1.1 301 Moved Permanently\n\n"
                response = '''<html>
                            <body>
                                <center>
                                <h3>Error 301: Permanently moved</h3>
                                <p>Location : ''' + file_path + "/index.html" +'''</p>
                                </center>
                            </body>
                            </html>
                '''.encode('utf-8')
                er_301 = False
            else:
                file = open("./www/"+request_path, 'rb')
                response = file.read()
                file.close()

                header = 'HTTP/1.1 200 OK\n'
                if (request_path.endswith(".css")):
                    mimetype = 'text/css'
                elif (request_path.endswith(".html")):
                    mimetype = 'text/html'
                header += 'Content-Type: '+str(mimetype)+'\n\n'
        except Exception as e:
            header = "HTTP/1.1 404 Not Found\n\n"
            response = '''<html>
                          <body>
                            <center>
                             <h3>Error 404: File not found</h3>
                             <p>Python HTTP Server</p>
                            </center>
                          </body>
                        </html>
            '''.encode('utf-8')

        final_response = header.encode('utf-8')
        final_response += response
        self.request.sendall(final_response)
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True

    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
