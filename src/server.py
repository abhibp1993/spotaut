import json
import translate
from http.server import HTTPServer, BaseHTTPRequestHandler


class SpotServiceHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)           # <--- Gets the data itself.

        # Extract data
        input_dict = json.loads(post_data)

        try:
            formula = input_dict["formula"]
            options = input_dict["options"]

            print(f"TRANSLATING formula:{formula} with options:{options}")
            aut = translate.translate(
                formula=formula,
                options=options
            ).toJSON()

        except Exception as err:
            self.send_error(500, str(err))
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(json.dumps(aut).encode())


def run(server_class=HTTPServer, handler_class=SpotServiceHandler):
    server_address = ("0.0.0.0", 8000)
    # server_address = ("127.0.0.1", 8000)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd...\nListening to {server_address}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')


if __name__ == '__main__':
    run()
