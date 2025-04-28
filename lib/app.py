import abc, inspect, io, subprocess, tempfile
from os import path
from xml.dom import minidom

import config
from .builder import Download, WriteFile
from .feed import Archive, FeedFor, ManifestDigest, Group, Implementation, Interface, Name, Summary

def _get_size(archive):
    archive.seek(0, io.SEEK_END)

    return archive.tell()

def _get_digest(archive, extract = None):
    base_args = ['0install', 'digest', '--algorithm=sha256new']
    extract_args = [extract] if extract is not None else []

    if archive.name:
        output = subprocess.check_output(base_args + [archive.name] + extract_args, encoding='utf-8')
    else:
        with WriteFile(archive, suffix='.tar.gz') as archive_name:
            output = subprocess.check_output(base_args + [archive.name] + extract_args, encoding='utf-8')

    return output.removeprefix('sha256new_').removesuffix('\n')

class App(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def summary(self):
        pass

    @property
    @abc.abstractmethod
    def archs(self):
        pass

    @abc.abstractmethod
    def commands(self, arch):
        pass

    @abc.abstractmethod
    def archive(self, arch):
        pass

    def update(self):
        versions = self.versions()

        feed_name = path.basename(inspect.getfile(self.__class__)).removesuffix('.py')
        feed_file = path.join('feeds', f'{feed_name}.xml')

        existing_versions = set()
        try:
            with open(feed_file, 'r') as file:
                dom = minidom.parse(file)

                for implementations in dom.getElementsByTagName('implementation'):
                    existing_versions.add(implementations.getAttribute('version'))
        except FileNotFoundError:
            pass

        versions_to_add = [version for version in versions if version['version'] not in existing_versions]

        if len(versions_to_add) == 0:
            return

        interface = Interface(
            Name(self.name),
            Summary(self.summary),
            FeedFor(interface = f'{config.base_url}{feed_name}.xml'),
        )

        for arch in self.archs:
            group = Group(*self.commands(arch), arch=arch)

            for version in versions_to_add:
                archive_url, extract = self.archive(arch, version)

                with Download(archive_url) as archive:
                    archive_size = _get_size(archive)
                    archive_digest = _get_digest(archive, extract)

                group.append(Implementation(
                    ManifestDigest(sha256new=archive_digest),
                    Archive(href=archive_url, size=archive_size, extract=extract),
                    id=f"{arch}-{version['version']}",
                    released=version['released'],
                    version=version['version'],
                ))

            interface.append(group)

        with tempfile.NamedTemporaryFile(suffix='.xml') as file:
            file.write(b'<?xml version="1.0"?>\n')
            file.write(interface.to_xml(indent='    ', encoding='utf-8'))
            file.flush()

            subprocess.check_output([
                '0install',
                'run',
                'https://apps.0install.net/0install/0publish.xml',
                f'--add-from={file.name}',
                feed_file,
            ])
