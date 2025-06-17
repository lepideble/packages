import json
from urllib import request

from lib import app, feed

project = 'modding-openmw%2Fmomw-post-processing-pack'

class MOMWPostProcessingPack(app.App):
    name = 'MOMW Post Processing Pack'
    summary = 'A collection of post-processing shaders for OpenMW'

    def versions(self):
        tags = json.loads(request.urlopen(request.Request(f'https://gitlab.com/api/v4/projects/{project}/repository/tags')).read())
        packages = json.loads(request.urlopen(request.Request(f'https://gitlab.com/api/v4/projects/{project}/packages?sort=desc')).read())

        for tag in tags:
            version = tag['name']
            released = tag['created_at'][0:10] if tag['created_at'] else None

            package = next((package for package in packages if package['version'] == version))
    
            package_files = json.loads(request.urlopen(request.Request(f"https://gitlab.com/api/v4/projects/{project}/packages/{package['id']}/package_files")).read())
            package_file = next((package_file for package_file in package_files if package_file['file_name'] == 'momw-post-processing-pack.zip'))

            if released is None:
                released = package_file['created_at'][0:10]

            yield {
                'version': version,
                'released': released,
                'file': f"https://gitlab.com/modding-openmw/momw-post-processing-pack/-/package_files/{package_file['id']}/download",
            }

    @property
    def archs(self):
        yield '*-*'

    def commands(self, arch):
        return []

    def archive(self, arch, version):
        return version['file'], None

if __name__ == '__main__':
    MOMWPostProcessingPack().update()
