import json

from twisted.internet import defer
from twisted.web import resource, server


class RecursiveResource(resource.Resource, object):

    isLeaf = False

    def getChild(self, name, request):
        if name == '':
            child = self
        else:
            try:
                child = self.children[name]
            except KeyError:
                child = super(RecursiveResource, self).getChild(name, request)
        return child


class EC2MetadataAPI(resource.Resource, object):

    isLeaf = True
    version = '2009-04-04'

    def __init__(self, server):
        super(EC2MetadataAPI, self).__init__()
        self.meta_server = server

    def render_GET(self, request):
        if len(request.postpath) > 1 and request.postpath[1]:
            d = self._render_meta(request)
            d.addCallback(lambda _: request.finish())
        else:
            self._render_keys(request)
            request.finish()

        return server.NOT_DONE_YET

    @defer.inlineCallbacks
    def _render_meta(self, request):
        client_ip = request.getClientIP()
        client_ip = '169.254.169.15'
        metadata = yield self.meta_server.get_metadata_for_ip(client_ip)

        path = request.postpath

        if path[1] == 'instance-id':
            request.write(metadata['uuid'])
            request.write('\n')
        elif path[1] == 'hostname':
            request.write(metadata['hostname'])
            request.write('\n')
        elif path[1] == 'public-keys':
            keys = metadata['public_keys'].items()
            if path[2:] and path[2]:
                key = keys[int(path[2])]
                request.write(key[1])
                request.write('\n')
            else:
                for i, (k, v) in enumerate(keys):
                    request.write('{}={}\n'.format(i, k))

    def _render_keys(self, request):
        keys = [

            ('hostname', False),
            ('public-keys', True)
        ]

        for key, isdir in keys:
            request.write(key)
            if isdir:
                request.write('/')
            request.write('\n')


class OpenstackMetadataAPI(resource.Resource, object):

    isLeaf = True
    version = '2012-08-10'

    def __init__(self, server):
        super(OpenstackMetadataAPI, self).__init__()
        self.meta_server = server

    @defer.inlineCallbacks
    def _delayed_renderer(self, request):
        client_ip = request.getClientIP()
        print client_ip
        client_ip = '169.254.169.15'
        metadata = yield self.meta_server.get_metadata_for_ip(client_ip)
        request.write(json.dumps(metadata))
        request.write('\n')
        request.finish()

    def render_GET(self, request):
        self._delayed_renderer(request)
        return server.NOT_DONE_YET


class APIVersionsIndex(RecursiveResource):

    def register_api(self, res):
        self.putChild(res.version, res)
        latest = self.children.get('latest', None)

        if not latest or res.version > latest.version:
            self.putChild('latest', res)

    def render_GET(self, request):
        versions = sorted(self.children)
        if versions:
            return '\n'.join(versions) + '\n'
        else:
            return ''


class MetadataIndex(RecursiveResource):

    isLeaf = False

    def __init__(self, server):
        super(MetadataIndex, self).__init__()

        self.ec2 = APIVersionsIndex()
        self.ec2.register_api(EC2MetadataAPI(server))

        self.openstack = APIVersionsIndex()
        self.openstack.register_api(OpenstackMetadataAPI(server))

    def getChild(self, name, request):
        if name == 'openstack':
            child = self.openstack
        else:
            child = self.ec2.getChild(name, request)
        return child
