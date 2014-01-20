import socket
from uuid import UUID
from urllib import quote as urlquote

from twisted.web import proxy, server


class LibvirtMetaReverseProxyResource(proxy.ReverseProxyResource, object):

    def __init__(self, resolver, *args, **kwargs):
        super(LibvirtMetaReverseProxyResource, self).__init__(*args, **kwargs)
        self._resolver = resolver

    def getChild(self, path, request):
        return LibvirtMetaReverseProxyResource(
            self._resolver, self.host, self.port,
            self.path + '/' + urlquote(path, safe=''), self.reactor)

    def render(self, request):
        ip_address = request.getClientIP()
        ip_address = '169.254.169.15'
        d = self._resolver.get_domain_by_ip(ip_address)
        d.addCallback(self._proxy_request, request)
        d.addErrback(self._render_error, request)
        return server.NOT_DONE_YET

    def _proxy_request(self, domain, request):
        uuid = UUID(bytes=domain.uuid)
        hostname = socket.gethostname()
        ip_address = request.getClientIP()

        request.requestHeaders.setRawHeaders('X-Instance-ID', [str(uuid)])
        request.requestHeaders.setRawHeaders('X-Tenant-ID', [hostname])
        request.requestHeaders.setRawHeaders('X-Forwarded-For', [ip_address])

        super(LibvirtMetaReverseProxyResource, self).render(request)

    def _render_error(self, failure, request):
        failure.trap(self._resolver.DomainNotFound)
        request.setResponseCode(404)
        request.write('Domain not found\n')
        request.finish()
