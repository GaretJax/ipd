from git import Repo

from collections import OrderedDict

from twisted.internet import threads, defer, task, reactor
from twisted.python import threadpool

from structlog import get_logger
logger = get_logger()


class NoSuchBranch(KeyError):
    def __init__(self, repo, branch):
        self.repo = repo
        self.branch = branch


class GitRepository(object):
    def __init__(self, repo_path):
        self.path = repo_path
        self._pool = threadpool.ThreadPool(1, 2)
        self._pool.start()
        reactor.addSystemEventTrigger('before', 'shutdown', self._pool.stop)
        self._repo = Repo(repo_path)

    def _deferToThread(self, func, *args, **kwargs):
       return threads.deferToThreadPool(reactor, self._pool,
                                        func, *args, **kwargs)

    @classmethod
    @defer.inlineCallbacks
    def clone(cls, url, dest):
        yield threads.deferToThread(Repo.clone_from, url, dest, mirror=True)
        defer.returnValue(cls(dest))

    @defer.inlineCallbacks
    def update(self):
        remote = self._repo.remote('origin')
        yield self._deferToThread(remote.fetch)
        defer.returnValue(None)

    def last_commit(self, branch):
        for head in self._repo.heads:
            if head.name == branch:
                return head.commit
        else:
            raise NoSuchBranch(self, branch)


class ObservableMixin(object):
    def __init__(self, *args, **kwargs):
        super(ObservableMixin, self).__init__(*args, **kwargs)
        self._callbacks = OrderedDict()

    def _fire_event(self, *args, **kwargs):
        for f in self._callbacks:
            f(*args, **kwargs)

    def subscribe(self, func):
        def unsubscribe():
            del self._callbacks[func]
        self._callbacks[func] = None
        return unsubscribe


class RepositoryPoller(ObservableMixin, object):
    polling_interval = 5

    def __init__(self, repository, branch='master'):
        super(RepositoryPoller, self).__init__()
        self._repo = repository
        self._current_commit = repository.last_commit(branch)
        self._poller_call = task.LoopingCall(self._poll)
        self._log = logger.new(
            repo=repository.path,
            branch=branch,
        ).msg
        self._branch = branch

    def start_polling(self, interval=None):
        if interval is None:
            interval = self.polling_interval
        self._poller_call.start(interval)

    def stop_polling(self):
        self._poller_call.stop()

    @defer.inlineCallbacks
    def _poll(self):
        self._log('poller.polling')
        yield self._repo.update()
        old_commit = self._current_commit
        new_commit = self._repo.last_commit(self._branch)

        if new_commit.binsha != old_commit.binsha:
            self._log('poller.new_commit', new_commit=new_commit.hexsha,
                      old_commit=old_commit.hexsha)
            self._current_commit = new_commit
            self._fire_event(self._repo, self._branch, new_commit, old_commit)
