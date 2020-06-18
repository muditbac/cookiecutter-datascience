from .utils import get_sacred_experiment

ex = get_sacred_experiment('train_experiment')


@ex.config
def config():
    c = 1


@ex.main
def main(c, _log):
    _log.info(f'Printing C: {c}')


if __name__ == '__main__':
    ex.run_commandline()
