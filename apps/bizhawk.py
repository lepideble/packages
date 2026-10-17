import posixpath
import re

from jvasseur.packaging.feed import Arg, Command, Environment, Runner
from jvasseur.packaging.app.github import ArchiveGitHubApp

from config import base_url

class BizHawk(ArchiveGitHubApp):
    uri = base_url + 'bizhawk.xml'
    repo = 'TASEmulators/BizHawk'

    def assets(self, assets):
        for asset in assets:
            if re.match(r"BizHawk-(.+)-linux-x64.tar.gz", asset['name']) or re.match(r"BizHawk-(.+)-linux.tar.gz", asset['name']):
                yield 'Linux-x86_64', asset
            if re.match(r"BizHawk-(.+)-win-x64.zip", asset['name']):
                yield 'Windows-x86_64', asset

    def extract(self, data):
        if data['arch'] == 'Linux-x86_64':
            if data['version'] in ('2.6.3', '2.8-rc1', '2.8', '2.9-rc1', '2.9-rc2', '2.9-rc3', '2.9.1', '2.10-rc1', '2.10'):
                return None
            else:
                return posixpath.basename(data['asset']['name']).removesuffix('.tar.gz')
        else:
            return None

    def commands(self, data):
        if data['arch'] == 'Windows-x86_64':
            yield Command(name='run', path='EmuHawk.exe')
        else:
            yield Command(
                Environment(name='LD_LIBRARY_PATH', insert='dll', mode='append'),
                Environment(name='LD_LIBRARY_PATH', insert='', mode='append'),
                Environment(name='MONO_CRASH_NOFILE', value='1', mode='replace'),
                Environment(name='MONO_WINFORMS_XIM_STYLE', value='disabled', mode='replace'),
                Runner(interface='https://apps.0install.net/dotnet/mono.xml'),
                Arg('--config=${HOME}/.config/bizhawk.json'),
                name='run',
                path='EmuHawk.exe'
            )

if __name__ == '__main__':
    BizHawk().main()
