import web
import config

urls = (
    '/', 'index',
    '/api', 'api'
)

class index:
    def GET(self):
        return "Telemetry Server - https://github.com/Tragnarion/kinectchallenge2013/tree/master/ToolsInGames/TelemetryServer"

class api:
    def POST(self):
        data = web.data() # you can get data use this method

        return data

    def GET(self):
        return "Telemetry Server - https://github.com/Tragnarion/kinectchallenge2013/tree/master/ToolsInGames/TelemetryServer"
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()