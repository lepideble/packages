import json, urllib.request

from lib import app, feed

class APSudoku(app.App):
    name = 'APSudoku'
    summary = 'Sudoku HintGame for Archipelago'

    def versions(self):
        releases = json.loads(urllib.request.urlopen('https://api.github.com/repos/APSudoku/APSudoku/releases').read())

        return [{
            'version': release['tag_name'],
            'released': release['published_at'][0:10],
            'stability': 'testing' if release['prerelease'] else 'stable',
            'files': {
                'Linux-aarch64': next((asset['browser_download_url'] for asset in release['assets'] if asset['name'] == 'APSudoku_Linux_arm64.zip'), None),
                'Linux-x86_64': next((asset['browser_download_url'] for asset in release['assets'] if asset['name'] == 'APSudoku_Linux_x64.zip'), None),
                'Windows-x86_64': next((asset['browser_download_url'] for asset in release['assets'] if asset['name'] == 'APSudoku_Win_x64.zip'), None),
            },
        } for release in releases]

    @property
    def archs(self):
        yield 'Linux-aarch64'
        yield 'Linux-x86_64'
        yield 'Windows-x86_64'

    def commands(self, arch):
        if arch == 'Linux-x86_64'or arch == 'Linux-aarch64':
            yield feed.Command(name='run', path='APSudoku_Linux_x64')
        if arch == 'Windows-x86_64':
            yield feed.Command(name='run', path='APSudoku_Win_x64.exe')

    def archive(self, arch, version):
        if version['files'][arch] is None:
            return None

        return version['files'][arch], None

if __name__ == "__main__":
    APSudoku().update()
