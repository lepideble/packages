from jvasseur.packaging.app.github import ArchiveGitHubApp, FileGitHubApp, GitHubApp
from jvasseur.packaging.feed import Command
from config import base_url

class ShipOfHarkinian(GitHubApp):
    uri = base_url + 'ship-of-harkinian.xml'
    repo = 'HarbourMasters/Shipwright'

    def version(self, tag_name):
        version = tag_name.split('.')
        # Ignore non-numeric versions
        if not version[0].isnumeric() or not version[1].isnumeric():
            return None

        # Ignore versions before 9.3.0
        if (int(version[0]), int(version[1])) < (9, 3):
            return None

        return super().version(tag_name)

    def assets(self, assets):
        for asset in assets:
            if asset['name'].endswith('.appimage'):
                yield 'Linux-x86_64', asset
            if asset['name'].endswith('-Win64.zip'):
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
                yield Command(name='run', path='soh.exe')

    def file_name(self, data):
        return 'soh.appimage'

    def file_executable(self, data):
        return True

    def extract(self, data):
        return None

if __name__ == '__main__':
    ShipOfHarkinian().main()
