from time import sleep
from os import path
from multiprocessing import Process

from bottle import Bottle, route, run, template


PRESETS_DIR = path.join(path.dirname(__file__), 'presets')


def template_response(func):
    def wrapper(*args, **kwargs):
        filename = func(*args, **kwargs)
        with open(path.join(PRESETS_DIR, filename)) as f:
            content = f.read()
        return template(content)
    return wrapper


class TPBApp(Bottle):

    def __init__(self, host='localhost', port=8000):
        super(TPBApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None

    def run(self):
        run(self, host=self.host, port=self.port, debug=False, quiet=True)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        sleep(1)

    def stop(self):
        self.process.terminate()
        self.process = None

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)

tpb = TPBApp()


@tpb.route('/search/<query>/<page>/<ordering>/<category>')
@template_response
def search(**kwargs):
    return 'search.html'


@tpb.route('/recent/<page>')
@template_response
def recent(**kwargs):
    return 'recent.html'


@tpb.route('/top/<category>')
@template_response
def top(**kwargs):
    return 'top.html'


@tpb.route('/torrent/<id>/<name>')
@template_response
def torrent(**kwargs):
    return 'torrent.html'


@tpb.route('/ajax_details_filelist.php')
@template_response
def files(**kwargs):
    return 'files.html'

if __name__ == '__main__':
    tpb.run()
