import sacred
from sacred.observers import MongoObserver, FileStorageObserver


def get_sacred_experiment(name, observer='mongo'):
	ex = sacred.Experiment(name)
	if observer == 'mongo':
		ex.observers.append(MongoObserver())
	else:
		ex.observers.append(FileStorageObserver('data/sacred/'))

	return ex


def quick_parse(*args):
	pass