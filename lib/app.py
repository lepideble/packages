import abc, inspect, io, os, subprocess, tempfile
from os import path
from urllib import request
from xml.dom import minidom

import config
from .builder import WriteFile
from .feed import Archive, FeedFor, ManifestDigest, Group, Implementation, Interface, Name, Summary

EXT_MAPPING = {
    'application/x-compressed-tar': 'tar.gz',
    'application/x-tar': 'tar',
    'application/zip': 'zip',
}

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

        feed_name = path.relpath(inspect.getfile(self.__class__), path.join(os.curdir, 'apps')).removesuffix('.py')
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

        for version in versions_to_add:
            interface = Interface(
                Name(self.name),
                Summary(self.summary),
                FeedFor(interface = f'{config.base_url}{feed_name}.xml'),
            )

            for arch in self.archs:
                group = Group(*self.commands(arch), arch=arch)

                archive = self.archive(arch, version)
                if archive is None:
                    continue

                archive_url, extract = archive

                response = request.urlopen(archive_url)

                content_type = response.headers.get_content_type()

                if content_type == 'application/octet-stream':
                    # Unspecified content type, trying to get type from archive URL
                    for key, value in EXT_MAPPING.items():
                        if archive_url.endswith(f'.{value}'):
                            content_type = key

                            break

                with tempfile.NamedTemporaryFile(suffix=f'.{EXT_MAPPING[content_type]}') as archive:
                    archive.write(response.read())

                    archive_size = _get_size(archive)
                    archive_digest = _get_digest(archive, extract)

                group.append(Implementation(
                    ManifestDigest(sha256new=archive_digest),
                    Archive(href=archive_url, size=archive_size, extract=extract, type=content_type),
                    id=f"{arch}-{version['version']}",
                    released=version['released'],
                    stability=version.get('stability'),
                    version=version['version'],
                ))

                interface.append(group)

            # Add version one by one to the feed to prevent having to restart from the start on error
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

                # Remove xml stylesheet added by 0publish
                subprocess.check_output([
                    'sed',
                    '--in-place',
                    "/<?xml-stylesheet type='text\\/xsl' href='interface.xsl'?>/d",
                    feed_file,
                ])
