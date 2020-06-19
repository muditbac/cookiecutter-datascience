import sacred
from sacred import SETTINGS
from sacred.observers import MongoObserver, FileStorageObserver

SETTINGS.DISCOVER_SOURCES = 'dir'


def get_sacred_experiment(name, observer='mongo'):
    ex = sacred.Experiment(name)
    if observer == 'mongo':
        ex.observers.append(MongoObserver(url='mongodb://{{cookiecutter.mongo_user}}:'
                                              '{{cookiecutter.mongo_password}}@127.0.0.1:27017',
                                          db_name='sacred'))
    else:
        ex.observers.append(FileStorageObserver('data/sacred/'))

    return ex


def quick_parse(*args):
    pass
