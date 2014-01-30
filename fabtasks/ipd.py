import os
import socket
from cStringIO import StringIO

from fabric.api import run, env, task, sudo, put, parallel, local, runs_once, hide


env.hosts = [
    'ipd1.tic.hefr.ch',
    'ipd2.tic.hefr.ch',
    'ipd3.tic.hefr.ch',
    'ipd4.tic.hefr.ch',
]

env.user = 'ipd'


@task
def ping():
    run('hostname')
    run('hostname -f')
    run('dig $(hostname -f)')
    run('cat /etc/resolv.conf')


@task
def crossping():
    for h in env.hosts:
        run('ping -c 1 {}'.format(h))
        h = h.split('.', 1)[0]
        run('ping -c 1 {}'.format(h))

@task
@parallel
def restartlibvirt():
    sudo('service libvirt-bin restart')


@task
@parallel
def addkey(key):
    """
    You may need to set the password through the environment if this is the
    first time you add a key.
    """
    run('mkdir -p ~/.ssh')
    run('chmod 0700 ~/.ssh')
    put(key, '~/key.tmp')
    run('cat ~/key.tmp >> ~/.ssh/authorized_keys')
    run('chmod 0600 ~/.ssh/authorized_keys')
    run('rm -f ~/key.tmp')


@task
@runs_once
def gencacert(path='workdir/pki'):
    keyfile = os.path.join(path, 'ca.key.pem')
    infofile = os.path.join(path, 'ca.info')
    certfile = os.path.join(path, 'ca.crt.pem')

    with open(infofile, 'w') as fh:
        fh.write('cn = Integrated Projects Deployer\n'
                 'ca\n'
                 'cert_signing_key\n')

    local('mkdir -p {}'.format(path))
    local('certtool --generate-privkey > {}'.format(keyfile))
    with hide('output'):
        local((
            'certtool '
            '--generate-self-signed '
            '--load-privkey {} '
            '--template {} '
            '--outfile {}'
        ).format(keyfile, infofile, certfile))


@task
@parallel
def instcacert(path='workdir/pki/ca.crt.pem'):
    remote_path = '/etc/pki/libvirt/ca.pem'
    sudo('mkdir -p /etc/pki/libvirt')
    put(path, remote_path, use_sudo=True)
    sudo('chown root:root {}'.format(remote_path))


@task
@parallel
def gencerts(path='workdir/pki'):
    keyfile = os.path.join(path, '{}.key.pem'.format(env.host))
    infofile = os.path.join(path, '{}.info'.format(env.host))
    certfile = os.path.join(path, '{}.crt.pem'.format(env.host))
    cacert = 'workdir/pki/ca.crt.pem'
    cakey = 'workdir/pki/ca.key.pem'

    local('mkdir -p {}'.format(path))
    local('certtool --generate-privkey > {}'.format(keyfile))

    with open(infofile, 'w') as fh:
        fh.write((
            'organization = Integrated Projects Deployer\n'
            'cn = {}\n'
            'tls_www_server\n'
            'encryption_key\n'
            'signing_key\n'
        ).format(env.host))

    with hide('output'):
        local((
            'certtool '
            '--generate-certificate '
            '--load-privkey {} '
            '--load-ca-certificate {} '
            '--load-ca-privkey {} '
            '--template {} '
            '--outfile {}'
        ).format(keyfile, cacert, cakey, infofile, certfile))


@task
@parallel
def instcerts(path='workdir/pki'):
    keyfile = os.path.join(path, '{}.key.pem'.format(env.host))
    certfile = os.path.join(path, '{}.crt.pem'.format(env.host))

    sudo('mkdir -p /etc/pki/libvirt/private')

    put(keyfile, '/etc/pki/libvirt/private/serverkey.pem', use_sudo=True)
    put(certfile, '/etc/pki/libvirt/servercert.pem', use_sudo=True)

    sudo('chown root:root '
         '/etc/pki/libvirt/private/serverkey.pem '
         '/etc/pki/libvirt/servercert.pem')


@task
@runs_once
def genclientcert(path='workdir/pki'):
    keyfile = os.path.join(path, 'client.key.pem')
    infofile = os.path.join(path, 'client.info')
    certfile = os.path.join(path, 'client.crt.pem')
    cacert = 'workdir/pki/ca.crt.pem'
    cakey = 'workdir/pki/ca.key.pem'

    local('mkdir -p {}'.format(path))
    local('certtool --generate-privkey > {}'.format(keyfile))

    with open(infofile, 'w') as fh:
        fh.write(
            'country = CH\n'
            'state = Fribourg\n'
            'locality = Fribourg\n'
            'organization = Integrated Project Deployer\n'
            'cn = ipd_client1\n'
            'tls_www_client\n'
            'encryption_key\n'
            'signing_key\n'
        )

    with hide('output'):
        local((
            'certtool '
            '--generate-certificate '
            '--load-privkey {} '
            '--load-ca-certificate {} '
            '--load-ca-privkey {} '
            '--template {} '
            '--outfile {}'
        ).format(keyfile, cacert, cakey, infofile, certfile))


@task
def setuppki():
    gencacert()
    gencerts()
    instcacert()
    instcerts()
    genclientcert()
    localpki()


@task
@runs_once
def localpki():
    local('sudo mkdir -p  /etc/pki/CA/')
    local('sudo cp workdir/pki/ca.crt.pem /etc/pki/CA/cacert.pem')


@task
@parallel
def conflibvirt():
    put('workdir/libvirtd.conf', '/etc/libvirt/libvirtd.conf', use_sudo=True)
    put('workdir/qemu.conf', '/etc/libvirt/qemu.conf', use_sudo=True)
    sudo('chown root:root /etc/libvirt/*.conf')
    restartlibvirt()


@task
@parallel
def bootstrap():
    ip = socket.gethostbyname(env.host)

    # Setup network interface
    with open('workdir/config/network.conf') as fh:
        conf = fh.read()
    conf = StringIO(conf.format(ip_address=ip))
    put(conf, '/etc/network/interfaces', use_sudo=True)
    sudo('chown root:root /etc/network/interfaces')
    sudo('service networking restart')

    # Setup rc.local
    with open('workdir/config/rc.local') as fh:
        conf = fh.read()
    conf = StringIO(conf.format(ip_address=ip))
    put(conf, '/etc/rc.local', use_sudo=True, mode=0755)
    sudo('chown root:root /etc/rc.local')

    # Get ubuntu base image
    sudo('mkdir -p /var/lib/ipd/images /var/lib/ipd/cd')
    sudo('wget -O /var/lib/ipd/cd/ubuntu.iso \'http://www.ubuntu.com/start-download?distro=server&bits=64&release=latest\'')

    # Correct apparmor config for libvirt
    # https://help.ubuntu.com/community/AppArmor
    # https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/1204616

    # Install base disk images
    # - windows
    # - ubuntu


@task
@parallel
def reboot():
    sudo('shutdown -r now   ')


@task
@runs_once
def redis():
    local('docker run -d -p 6379:6379 -volumes-from ipd-redis-data harbor.wsfcomp.com/redis')


@task
@parallel
def installipd():
    version = local('python setup.py --version', capture=True)
    name = local('python setup.py --name', capture=True)

    sudo('apt-get install -y python-pip python-dev libxml2-dev libxslt-dev zlib1g-dev')
    sudo('pip install {}=={}'.format(name, version))
