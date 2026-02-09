from jvasseur.packaging.feed import Command, Runner
from jvasseur.packaging.app.github import ArchiveGitHubApp
from config import base_url

class APProxy(ArchiveGitHubApp):
    uri = base_url + 'ap-proxy.xml'
    repo = 'lepideble/ap-proxy'

    def assets(self, assets):
        for asset in assets:
            if asset['name'] == 'APProxy.tar.gz':
                yield None, asset

    def commands(self, data):
        yield Command(
            Runner(interface='https://apps.0install.net/javascript/node.xml', version='22.18.0..'),
            name='run',
            path='index.ts',
        );

if __name__ == '__main__':
    APProxy().main()
