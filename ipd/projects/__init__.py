from twisted.internet import defer, protocol
from ipd import repository
from structlog import get_logger
from twisted.application import service

from .builder import Builder, BuildspecNotFound

logger = get_logger()


class ProjectAlreadyExists(Exception):
    def __init__(self, key):
        self.key = key


class ProjectNotFound(Exception):
    def __init__(self, key):
        self.key = key


class ProjectsManager(service.Service, object):
    def __init__(self, workdir, redis_connector, key):
        super(ProjectsManager, self).__init__()
        self._redis = redis_connector
        self._workdir = workdir
        self._pollers = {}
        self._key = key

    def startService(self):
        logger.msg('projects.starting_service')
        super(ProjectsManager, self).startService()
        self.start_polling()

    def stopService(self):
        logger.msg('projects.stopping_service')
        self.stop_polling()
        return super(ProjectsManager, self).stopService()

    def get_projects(self):
        d = self._redis()
        d.addCallback(lambda r: r.smembers('projects'))
        return d

    @defer.inlineCallbacks
    def get_project(self, key):
        redis = yield self._redis()
        prj = yield redis.get('project:' + key)
        if not prj:
            raise ProjectNotFound(key)
        defer.returnValue({
            'repo': prj
        })

    @defer.inlineCallbacks
    def start_polling(self):
        projects = yield self.get_projects()
        dl = [self.start_polling_project(prj) for prj in projects]
        yield defer.DeferredList(dl)
        logger.msg('projects.polling_started', projects_count=len(projects))

    def stop_polling(self):
        for poller in self._pollers.keys():
            self.stop_polling_project(poller)
        logger.msg('projects.polling_stopped')

    @defer.inlineCallbacks
    def register_project(self, key, repository):
        redis = yield self._redis()
        res = yield redis.sadd('projects', key)
        if not res:
            raise ProjectAlreadyExists(key)

        yield redis.set('project:' + key, repository)
        logger.msg('projects.registered', key=key, repo=repository)
        self.start_polling_project(key)

    @defer.inlineCallbacks
    def start_polling_project(self, key):
        workdir = self._workdir.child('poller').child(key)

        if workdir.exists():
            repo = repository.GitRepository(workdir.path)
        else:
            workdir.makedirs()
            prj = yield self.get_project(key)
            repo = yield repository.GitRepository.clone(prj['repo'], workdir.path)

        poller = repository.RepositoryPoller(repo)
        self._pollers[key] = poller
        def t(repo, branch, new, old):
            logger.msg('up', key=key, repo=repo, branch=branch, new=new, old=old)
        poller.subscribe(t)
        poller.start_polling()

    def stop_polling_project(self, key):
        try:
            poller = self._pollers.pop(key)
        except KeyError:
            pass
        else:
            poller.stop_polling()

    @defer.inlineCallbacks
    def unregister_project(self, key):
        redis = yield self._redis()
        yield redis.multi()
        yield redis.delete('project:' + key)
        yield redis.srem('projects', key)
        yield redis.execute()
        self.stop_polling_project(key)
        workdir = self._workdir.child('poller').child(key)
        if workdir.exists():
            workdir.remove()
