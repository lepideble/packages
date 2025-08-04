import json, urllib.request

from lib import app, feed

class Archipelago(app.App):
    name = 'Archipelago'
    summary = 'Archipelago Multi-Game Randomizer and Server'

    def versions(self):
        releases = json.loads(urllib.request.urlopen('https://api.github.com/repos/ArchipelagoMW/Archipelago/releases').read())

        return [{
            'version': release['tag_name'],
            'released': release['published_at'][0:10],
            'stability': 'testing' if release['prerelease'] else 'stable',
            'files': {
                'Linux-x86_64': next((asset['browser_download_url'] for asset in release['assets'] if asset['name'].endswith('linux-x86_64.tar.gz')), None),
            },
        } for release in releases]

    @property
    def archs(self):
        yield 'Linux-x86_64'

    def commands(self, arch):
        if arch == 'Linux-x86_64':
            yield feed.Command(name='run', path='ArchipelagoLauncher')
            yield feed.Command(name='adventure-client', path='ArchipelagoAdventureClient')
            yield feed.Command(name='ahit-client', path='ArchipelagoAHITClient')
            yield feed.Command(name='biz-hawk-client', path='ArchipelagoBizHawkClient')
            yield feed.Command(name='checks-finder-client', path='ArchipelagoChecksFinderClient')
            yield feed.Command(name='kh1-client', path='ArchipelagoKH1Client')
            yield feed.Command(name='kh2-client', path='ArchipelagoKH2Client')
            yield feed.Command(name='links-awakening-client', path='ArchipelagoLinksAwakeningClient')
            yield feed.Command(name='lttp-adjuster', path='ArchipelagoLttPAdjuster')
            yield feed.Command(name='mmbn3-client', path='ArchipelagoMMBN3Client')
            yield feed.Command(name='oot-adjuster', path='ArchipelagoOoTAdjuster')
            yield feed.Command(name='oot-client', path='ArchipelagoOoTClient')
            yield feed.Command(name='server', path='ArchipelagoServer')
            yield feed.Command(name='sni-client', path='ArchipelagoSNIClient')
            yield feed.Command(name='starcraft2-Client', path='ArchipelagoStarcraft2Client')
            yield feed.Command(name='text-client', path='ArchipelagoTextClient')
            yield feed.Command(name='undertale-client', path='ArchipelagoUndertaleClient')
            yield feed.Command(name='zelda1-client', path='ArchipelagoZelda1Client')
            yield feed.Command(name='zillion-client', path='ArchipelagoZillionClient')

    def archive(self, arch, version):
        if version['files'][arch] is None:
            return None

        return version['files'][arch], 'Archipelago'

if __name__ == "__main__":
    Archipelago().update()
