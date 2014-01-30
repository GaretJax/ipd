
from twisted.conch.client.knownhosts import PlainEntry
from twisted.conch.error import HostKeyChanged, UserRejectedKey
from twisted.internet import protocol, defer
from twisted.conch.ssh.keys import Key
from twisted.conch.endpoints import SSHCommandClientEndpoint


class CommandsProtocol(protocol.Protocol):
    def connectionMade(self):
        self.disconnected = None

    def exec_command(self, command):
        conn = self.transport.conn
        factory = protocol.Factory()
        factory.protocol = SingleCommandProtocol

        e = SSHCommandClientEndpoint.existingConnection(conn, command)
        d = e.connect(factory)
        d.addCallback(lambda p: p.finished)
        return d

    def disconnect(self):
        d = self.disconnected = defer.Deferred()
        self.transport.loseConnection()
        return d

    def connectionLost(self, reason):
        if self.disconnected:
            self.disconnected.callback(None)


class SingleCommandProtocol(protocol.Protocol):
    def connectionMade(self):
        self.data = []
        self.finished = defer.Deferred()

    def dataReceived(self, data):
        self.data.append(data)

    def connectionLost(self, reason):
        self.finished.callback(''.join(self.data))


class MultipleCommandsFactory(protocol.Factory):
    protocol = CommandsProtocol


class MultipleCommandsClientEndpoint(SSHCommandClientEndpoint):
    @classmethod
    def newConnection(cls, reactor, username, hostname, port=None, keys=None,
                      password=None, agentEndpoint=None, knownHosts=None,
                      ui=None):
        return super(MultipleCommandsClientEndpoint, cls).newConnection(
            reactor, '/bin/cat', username, hostname, port, keys, password, agentEndpoint,
            knownHosts, ui
        )


class KnownHostsLists(object):
    def __init__(self, known_hosts):
        self._entries = []
        for hostname, key in known_hosts:
            self.addHostKey(hostname, key)

    def addHostKey(self, hostname, key):
        key_type = 'ssh-' + key.type().lower()
        entry = PlainEntry([hostname], key_type, key, None)
        self._entries.append(entry)
        return entry

    def hasHostKey(self, hostname, key):
        for entry in self._entries:
            if entry.matchesHost(hostname):
                if entry.matchesKey(key):
                    return True
                else:
                    raise HostKeyChanged(entry, 'memory', 0)
        return False

    def verifyHostKey(self, ui, hostname, ip, key):
        match = self.hasHostKey(hostname, key)
        if match:
            if not self.hasHostKey(ip, key):
                ui.warn("Warning: Permanently added the %s host key for "
                        "IP address '%s' to the list of known hosts." %
                        (key.type(), ip))
                self.addHostKey(ip, key)
            return defer.succeed(match)
        else:
            def promptResponse(response):
                if response:
                    self.addHostKey(hostname, key)
                    self.addHostKey(ip, key)
                    return response
                else:
                    raise UserRejectedKey()
            proceed = ui.prompt(
                "The authenticity of host '%s (%s)' "
                "can't be established.\n"
                "RSA key fingerprint is %s.\n"
                "Are you sure you want to continue connecting (yes/no)? " %
                (hostname, ip, key.fingerprint()))
            return proceed.addCallback(promptResponse)

    def iterentries(self):
        for entry in self._entries:
            yield entry
