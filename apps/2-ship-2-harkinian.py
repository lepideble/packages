import json
from urllib import request

from lib import app, feed

class TwoShipTwoHarkinian(app.App):
    name = '2 Ship 2 Harkinian'
    summary = 'port of the 2000 Nintendo 64 video game The Legend of Zelda: Majora\'s Mask'

    def versions(self):
        releases = json.loads(request.urlopen(request.Request('https://api.github.com/repos/HarbourMasters/2ship2harkinian/releases')).read())

        return [{
            'version': release['tag_name'],
            'released': release['published_at'][0:10],
            'files': {
                'Linux-x86_64': next(asset['browser_download_url'] for asset in release['assets'] if asset['name'].endswith('-Linux.zip')),
                'Windows-x86_64': next(asset['browser_download_url'] for asset in release['assets'] if asset['name'].endswith('-Win64.zip')),
            },
        } for release in releases]

    @property
    def archs(self):
        yield 'Linux-x86_64'
        yield 'Windows-x86_64'

    def commands(self, arch):
        if arch == 'Linux-x86_64':
            yield feed.Command(name='run', path='2ship.appimage')
        if arch == 'Windows-x86_64':
            yield feed.Command(name='run', path='2ship.exe')

    def archive(self, arch, version):
        return version['files'][arch], None

if __name__ == "__main__":
    TwoShipTwoHarkinian().update()
