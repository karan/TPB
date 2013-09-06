from os import path
from multiprocessing import Process

from bottle import Bottle, run, template


PRESETS_DIR = 'presets'


class TPBApp(Bottle):
    presets = {
            '/search/<query>/<page>/<ordering>/<category>': 'search.html',
            '/recent/<page>': 'recent.html',
            '/top/<category>': 'top.html',
            }

    def __init__(self, host='localhost', port=8000):
        super(TPBApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.build_routes()

    def build_routes(self):
        for url, preset in self.presets.items():
            with open(path.join(PRESETS_DIR, preset)) as preset:
                content = preset.read()
                self.route(url)(lambda **kwargs: template(content))

    def run(self):
        run(self, host=self.host, port=self.port)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process = None
        

if __name__ == '__main__':
    TPBApp('localhost', 8000).run()
