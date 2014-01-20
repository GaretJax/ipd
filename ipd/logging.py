import structlog

from structlog import get_logger
from twisted.python import log


__all__ = ['setup_logging', 'get_logger']


class FailureConverter(object):
    def __call__(self, logger, method_name, event_dict):
        if event_dict.get('why', None):
            if 'event' not in event_dict:
                event_dict['event'] = event_dict.pop('why')
        else:
            event_dict.pop('why', None)

        if event_dict.pop('isError', None):
            failure = event_dict.pop('failure', None)
            if failure:
                event_dict['exception'] = failure.getTraceback().strip()

        return event_dict


class EmptyEventFilter(object):
    def __init__(self, ignored_keys=None):
        self._keys = set(ignored_keys or [])

    def __call__(self, logger, method_name, event_dict):
        if set(event_dict).issubset(self._keys):
            raise structlog.DropEvent()
        return event_dict


class StructlogObserver(object):
    def __init__(self, logger):
        self._logger = logger

    def __call__(self, event_dict):
        message = event_dict.pop('message')
        if message:
            message = ' '.join([str(s) for s in message])
        if event_dict.get('system', None) == '-':
            del event_dict['system']
        return self._logger.msg(message, **event_dict)


class KeysRemover(object):
    def __init__(self, keys):
        self._keys = keys

    def __call__(self, logger, method_name, event_dict):
        for k in self._keys:
            event_dict.pop(k, None)
        return event_dict


def start_logging(logger=None, capture_stdout=False):
    if logger is None:
        logger = structlog.get_logger()
    log_observer = StructlogObserver(logger)
    log.startLoggingWithObserver(log_observer, setStdout=capture_stdout)


def setup_logging():
    structlog.configure(
        processors=[
            KeysRemover(['time']),
            FailureConverter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionPrettyPrinter(),
            EmptyEventFilter(['time', 'system']),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    start_logging()
