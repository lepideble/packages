import json
from urllib import request

from lib import app, feed

class ShipOfHarkinian(app.App):
    name = 'Ship of Harkinian'
    summary = 'port of the 1998 Nintendo 64 video game The Legend of Zelda: Ocarina of Time'

    def versions(self):
        releases = json.loads(request.urlopen(request.Request('https://api.github.com/repos/HarbourMasters/Shipwright/releases')).read())

        # Ignore versions before 9.0.0
        releases = [release for release in releases if release['tag_name'].split('.')[0].isnumeric() and int(release['tag_name'].split('.')[0]) >= 9]

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
            yield feed.Command(name='run', path='soh.appimage')
        if arch == 'Windows-x86_64':
            yield feed.Command(name='run', path='soh.exe')

    def archive(self, arch, version):
        return version['files'][arch], None

if __name__ == "__main__":
    ShipOfHarkinian().update()
