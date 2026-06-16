from jvasseur.packaging.feed import Command, Runner
from jvasseur.packaging.app.github import ArchiveGitHubApp, FileGitHubApp, GitHubApp
from config import base_url

class Dusklight(GitHubApp):
    uri = base_url + 'dusklight.xml'
    repo = 'TwilitRealm/dusklight'

    def version(self, tag_name):
        return tag_name.removeprefix('v').replace('rc.', 'rc')

    def assets(self, assets):
        for asset in assets:
            if asset['name'].endswith('-linux-x86_64.AppImage'):
                yield 'Linux-x86_64', asset
            if asset['name'].endswith('-win32-x86_64.zip'):
                yield 'Windows-x86_64', asset

    def manifest_digest(self, data):
        match data['arch']:
            case 'Linux-x86_64':
                return FileGitHubApp.manifest_digest(self, data)
            case 'Windows-x86_64':
                return ArchiveGitHubApp.manifest_digest(self, data)

    def retrieval(self, data):
        match data['arch']:
            case 'Linux-x86_64':
                return FileGitHubApp.retrieval(self, data)
            case 'Windows-x86_64':
                return ArchiveGitHubApp.retrieval(self, data)

    def commands(self, data):
        match data['arch']:
            case 'Linux-x86_64':
                yield Command(name='run', path=self.file_name(data))
            case 'Windows-x86_64':
                yield Command(name='run', path='dusklight.exe')

    def file_name(self, data):
        return 'Dusklight.AppImage'

    def file_executable(self, data):
        return True

    def extract(self, data):
        return None

if __name__ == '__main__':
    Dusklight().main()
