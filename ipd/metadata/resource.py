import json
from uuid import UUID

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


class MetadataMixin(object):
    def __init__(self, server):
        super(MetadataMixin, self).__init__()
        self.meta_server = server

    def get_metadata_from_request(self, request):
        h = request.requestHeaders
        hypervisor = h.getRawHeaders('X-Tenant-ID')[0]
        domain_uuid = UUID(hex=h.getRawHeaders('X-Instance-ID')[0])
        #domain_ip = h.getRawHeaders('X-Forwarded-For')[0]

        return self.meta_server.get_metadata_for_uuid(hypervisor, domain_uuid)


class UserdataResource(resource.Resource, object):
    isLeaf = True
    def __init__(self, server):
        super(UserdataResource, self).__init__()
        self.meta_server = server

    def get_userdata_from_request(self, request):
        h = request.requestHeaders
        hypervisor = h.getRawHeaders('X-Tenant-ID')[0]
        domain_uuid = UUID(hex=h.getRawHeaders('X-Instance-ID')[0])
        #domain_ip = h.getRawHeaders('X-Forwarded-For')[0]

        return self.meta_server.get_userdata_for_uuid(hypervisor, domain_uuid)

    @defer.inlineCallbacks
    def _delayed_renderer(self, request):
        userdata = yield self.get_userdata_from_request(request)
        request.write(userdata)
        request.finish()

    def render_GET(self, request):
        self._delayed_renderer(request)
        return server.NOT_DONE_YET


class AtomResource(MetadataMixin, resource.Resource, object):
    @defer.inlineCallbacks
    def _delayed_renderer(self, request):
        metadata = yield self.get_metadata_from_request(request)
        atom = self.get_value(metadata)
        request.write(atom)
        request.write('\n')
        request.finish()

    def render_GET(self, request):
        self._delayed_renderer(request)
        return server.NOT_DONE_YET

    def get_value(self, metadata):
        raise NotImplementedError()


class KeyedAtomResource(AtomResource):
    isLeaf = True

    def __init__(self, server, key):
        super(KeyedAtomResource, self).__init__(server)
        self._key = key

    def get_value(self, metadata):
        val = metadata
        for k in self._key:
            val = val[k]
        return str(val)


class KeysResource(AtomResource):
    isLeaf = False

    formats = {
        'openssh-key': 'OPENSSH'
    }

    def get_value(self, metadata):
        keys = ('{}={}'.format(i, k[0])
                for i, k in enumerate(metadata['public_keys']))
        return '\n'.join(keys)

    def getChild(self, name, request):
        if not name:
            return self
        key = int(name)
        fmt = self.formats[request.postpath[0]]
        return KeyRenderer(self.meta_server, key, fmt)


class KeyRenderer(KeyedAtomResource):
    def __init__(self, server, key, fmt):
        super(KeyedAtomResource, self).__init__(server)
        self._key = key
        self._format = fmt

    def get_value(self, metadata):
        key = metadata['public_keys'][self._key][1]
        return key.toString(self._format)


class IndexResource(RecursiveResource):
    isleaf = False

    def render_GET(self, request):
        for k, v in sorted(self.children.items()):
            request.write(k)
            if not v.isLeaf:
                request.write('/\n')
            else:
                request.write('\n')
        request.finish()
        return server.NOT_DONE_YET


class EC2MetadataAPI(IndexResource):

    isLeaf = False
    version = '2009-04-04'

    def __init__(self, server):
        super(EC2MetadataAPI, self).__init__()
        meta = IndexResource()
        meta.putChild('hostname', KeyedAtomResource(server, ['hostname']))
        meta.putChild('instance-id', KeyedAtomResource(server, ['uuid']))
        meta.putChild('public-keys', KeysResource(server))
        self.putChild('meta-data', meta)
        self.putChild('user-data', UserdataResource(server))


class OpenstackMetadataAPI(IndexResource):

    version = '2012-08-10'

    def __init__(self, server):
        super(OpenstackMetadataAPI, self).__init__()
        self.putChild('meta_data.json', OpenstackMetadata(server))
        self.putChild('user_data', UserdataResource(server))


class OpenstackMetadata(MetadataMixin, resource.Resource, object):
    isLeaf = True

    @defer.inlineCallbacks
    def _delayed_renderer(self, request):
        metadata = yield self.get_metadata_from_request(request)
        metadata['uuid'] = str(metadata['uuid'])
        metadata['public_keys'] = {
            k: v.toString('OPENSSH')
            for k, v in metadata['public_keys']
        }

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
