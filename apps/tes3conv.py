from jvasseur.packaging.feed import Command
from jvasseur.packaging.app.github import ArchiveGitHubApp
from config import base_url

class TES3Conv(ArchiveGitHubApp):
    uri = base_url + 'tes3conv.xml'
    repo = 'Greatness7/tes3conv'

    def version(self, tag_name):
        if tag_name == 'v0.1.0':
            return None

        return super().version(tag_name)

    def assets(self, assets):
        for asset in assets:
            if asset['name'] == 'ubuntu-latest.zip':
                yield 'Linux-x86_64', asset
            if asset['name'] == 'windows-latest.zip':
                yield 'Windows-x86_64', asset
            if asset['name'] == 'macos-13-x86_64.zip':
                yield 'MacOSX-x86_64', asset
            if asset['name'] == 'macos-latest-arm64.zip':
                yield 'MacOSX-aarch64', asset

    def commands(self, data):
        if data['arch'] == 'Windows-x86_64':
            yield Command(name='run', path='tes3conv.exe')
        else:
            yield Command(name='run', path='tes3conv')

if __name__ == '__main__':
    TES3Conv().main()
