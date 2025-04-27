import os
import tempfile
import urllib.parse
import urllib.request

class Download:
    def __init__(self, url):
        path = urllib.parse.urlsplit(url).path
        basename = os.path.basename(path)

        self.url = url
        self.temporary_file = tempfile.NamedTemporaryFile(suffix=basename)

    def __enter__(self):
        file = self.temporary_file.__enter__()

        with urllib.request.urlopen(self.url) as response:
            file.write(response.read())

        return file

    def __exit__(self, exc_type, exc_value, traceback):
        self.temporary_file.__exit__(exc_type, exc_value, traceback)

class WriteFile:
    def __init__(self, data, suffix=None):
        self.temporary_file = tempfile.NamedTemporaryFile(suffix=suffix)
        self.data = data

    def __enter__(self):
        file = self.temporary_file.__enter__()

        self.data.seek(0)
        file.write(self.data.read())

        return file.name

    def __exit__(self, exc_type, exc_value, traceback):
        self.temporary_file.__exit__(exc_type, exc_value, traceback)

class Workdir:
    def __init__(self):
        self.tempdir = tempfile.TemporaryDirectory()

    def __enter__(self):
        path = self.tempdir.__enter__()

        self.previous_path = os.getcwd()
        os.chdir(path)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.previous_path)

        self.tempdir.__exit__(exc_type, exc_value, traceback)
