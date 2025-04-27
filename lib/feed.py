import xml.dom.minidom

class Interface:
    def __init__(self, *content):
        self.content = list(content)

    def append(self, element):
        self.content.append(element)

    def to_xml(self, indent, encoding):
        xmlns = 'http://zero-install.sourceforge.net/2004/injector/interface'

        implementation = xml.dom.minidom.getDOMImplementation()
        document = implementation.createDocument(xmlns, 'interface', None)

        document.documentElement.setAttribute('xmlns', xmlns)

        for element in self.content:
            document.documentElement.appendChild(element.as_node(document))

        return document.documentElement.toprettyxml(indent=indent, encoding=encoding)

class Archive:
    def __init__(self, *, href: str, size: int, extract: str = None):
        self.href = href
        self.size = size
        self.extract = extract

    def as_node(self, document):
        node = document.createElement('archive')
        node.setAttribute('href', self.href)
        node.setAttribute('size', str(self.size))
        if self.extract is not None:
            node.setAttribute('extract', self.extract)

        return node

class Command:
    def __init__(self, *, name, path):
        self.name = name
        self.path = path

    def as_node(self, document):
        node = document.createElement('command')
        node.setAttribute('name', self.name)
        node.setAttribute('path', self.path)

        return node

class FeedFor:
    def __init__(self, *, interface):
        self.interface = interface

    def as_node(self, document):
        node = document.createElement('feed-for')
        node.setAttribute('interface', self.interface)

        return node

class Implementation:
    def __init__(self, *content, id, released, version):
        self.content = content
        self.id = id
        self.released = released
        self.version = version

    def as_node(self, document):
        node = document.createElement('implementation')
        node.setAttribute('id', self.id)
        node.setAttribute('released', self.released)
        node.setAttribute('version', self.version)

        for element in self.content:
            node.appendChild(element.as_node(document))

        return node

class ManifestDigest:
    def __init__(self, *, sha256new):
        self.sha256new = sha256new

    def as_node(self, document):
        node = document.createElement('manifest-digest')
        node.setAttribute('sha256new', self.sha256new)

        return node

class Group:
    def __init__(self, *content, arch):
        self.content = list(content)
        self.arch = arch

    def append(self, element):
        self.content.append(element)

    def as_node(self, document):
        node = document.createElement('group')
        node.setAttribute('arch', self.arch)

        for element in self.content:
            node.appendChild(element.as_node(document))

        return node

class Name:
    def __init__(self, content):
        self.content = content

    def as_node(self, document):
        node = document.createElement('name')
        node.appendChild(document.createTextNode(self.content))

        return node

class Summary:
    def __init__(self, content):
        self.content = content

    def as_node(self, document):
        node = document.createElement('summary')
        node.appendChild(document.createTextNode(self.content))

        return node
