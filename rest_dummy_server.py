#!/usr/bin/env python
import web, json

urls = (
    '/service1', 'service1_class'
)

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class service1_class:
    def POST(self):
        return json.dumps({'status':'ok'})

if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run(port=8081)
