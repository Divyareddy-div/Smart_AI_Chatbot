"""
================================================================================
SMART AI CHATBOT - WEB APPLICATION SERVER
================================================================================
Description: A web interface server for Smart AI Chatbot built purely with
             Python standard libraries (`http.server`, `json`, `urllib`).
             Serves a modern glassmorphic web UI (`index.html`) and handles
             asynchronous HTTP POST requests for chatbot intent processing.

Author:      B.Tech AI Student
Language:    Python 3.8+
================================================================================
"""

import http.server
import json
import os
import socketserver
import sys
import webbrowser
from urllib.parse import parse_qs, urlparse

from chatbot import ChatState, process_response, match_exit

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class ChatbotHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP Request Handler serving static web files and REST API endpoint for chat messages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        """Handles POST requests to /api/chat."""
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                user_name = data.get('name', 'Friend')
                message = data.get('message', '')

                # Initialize temporary ChatState for session query
                state = ChatState()
                state.set_user_name(user_name)

                # Process intent response
                if match_exit(message):
                    response_text = f"Goodbye, {state.user_name}! Have a wonderful day! 👋 🤖"
                    is_exit = True
                else:
                    response_text = process_response(message, state)
                    is_exit = False

                response_data = {
                    "status": "success",
                    "user_name": state.user_name,
                    "response": response_text,
                    "is_exit": is_exit
                }

                # Send 200 OK JSON response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                err_data = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(err_data).encode('utf-8'))
        else:
            self.send_error(440, "File Not Found")

    def do_GET(self):
        """Serves default index.html on root route."""
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()


def run_web_server():
    """Starts the Web Application HTTP Server."""
    handler = ChatbotHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 72)
        print(f"🤖 SMART AI CHATBOT - WEB APPLICATION SERVER RUNNING")
        print(f"🔗 Server Link: {url}")
        print("   Press Ctrl+C in terminal to stop the web server.")
        print("=" * 72)

        # Open web browser automatically
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped successfully.")
            httpd.server_close()


if __name__ == "__main__":
    run_web_server()
