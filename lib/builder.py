import os
import tempfile

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
