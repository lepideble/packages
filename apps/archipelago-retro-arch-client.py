import json, urllib.request

from lib import app, feed

class ArchipelagoRetroArchClient(app.App):
    name = 'Archipelago RetroArch client'
    summary = 'client that allows people to play Ocarina of Time on Archipelago using RetroArch'

    def versions(self):
        releases = json.loads(urllib.request.urlopen('https://api.github.com/repos/JoshuaEagles/Archipelago.RetroArchClient/releases').read())

        return [{
            'version': release['tag_name'],
            'released': release['published_at'][0:10],
            'stability': 'testing' if release['prerelease'] else 'stable',
            'files': {
                'Linux-x86_64': next((asset['browser_download_url'] for asset in release['assets'] if asset['name'].endswith('-Linux.zip')), None),
                'Windows-x86_64': next((asset['browser_download_url'] for asset in release['assets'] if asset['name'].endswith('-Windows.zip')), None),
            },
        } for release in releases]

    @property
    def archs(self):
        yield 'Linux-x86_64'
        yield 'Windows-x86_64'

    def commands(self, arch):
        if arch == 'Linux-x86_64':
            yield feed.Command(name='run', path='Archipelago.RetroArchClient')
        if arch == 'Windows-x86_64':
            yield feed.Command(name='run', path='Archipelago.RetroArchClient.exe')

    def archive(self, arch, version):
        if version['files'][arch] is None:
            return None

        return version['files'][arch], None

if __name__ == "__main__":
    ArchipelagoRetroArchClient().update()
