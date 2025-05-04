import json, posixpath, re
from urllib import request

from lib import app, feed

def get_version_from_release(release):
    version = release['tag_name'].removeprefix('openmw-')

    # Fix 0.49.0-rc* versions
    match = re.fullmatch('49-rc([0-9]+)', version)
    if match:
        version = f'0.49.0-rc{match.group(1)}'

    return version

def get_extract_from_archive_url(archive_url):
    extract = posixpath.basename(archive_url).removesuffix('.tar.gz')

    if extract == 'openmw-0.49.0-Linux-64BitRC2':
        extract = 'openmw-0.49.0-Linux-64BitRC2-qt6'

    return extract
    

class OpenMW(app.App):
    name = 'OpenMW'
    summary = 'open-source open-world RPG game engine that supports playing Morrowind'

    def versions(self):
        releases = json.loads(request.urlopen(request.Request('https://api.github.com/repos/OpenMW/openmw/releases')).read())

        return [{
            'version': get_version_from_release(release),
            'released': release['published_at'][0:10],
            'stability': 'testing' if release['prerelease'] else 'stable',
            'files': {
                'Linux-x86_64': next((asset['browser_download_url'] for asset in release['assets'] if '-Linux-' in asset['name']), None),
            },
        } for release in releases]

    @property
    def archs(self):
        yield 'Linux-x86_64'

    def commands(self, arch):
        if arch == 'Linux-x86_64':
            yield feed.Command(name='run', path='openmw')
            yield feed.Command(name='cs', path='openmw-cs')
            yield feed.Command(name='launcher', path='openmw-launcher')

    def archive(self, arch, version):
        if version['files'][arch] is None:
            return None

        return version['files'][arch], get_extract_from_archive_url(version['files'][arch])

if __name__ == "__main__":
    OpenMW().update()
