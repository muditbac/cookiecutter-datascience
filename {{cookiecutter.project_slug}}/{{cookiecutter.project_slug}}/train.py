import time

import tensorflow as tf
from easydict import EasyDict as edict

from . import net, metrics
from .dataset import build_dataset
from .utils import get_sacred_experiment

ex = get_sacred_experiment('train_experiment', observer='file')


class Trainer:

    def __init__(self, args, run, log):
        args = edict(args)

        self.env_args = args.pop('env')
        self.args = args
        self.log = log

    def get_train_dataset(self):
        return build_dataset(split='train', train=True)

    def get_validation_dataset(self):
        return build_dataset(split='test', train=False)

    def get_model(self):
        return getattr(net, self.args.model_name)(**self.args.model_params)

    def get_loss(self):
        return getattr(metrics, self.args.loss_name)(**self.args.loss_params)

    def get_metrics(self):
        return ['accuracy']

    def get_callbacks(self):
        model_key = '%s' % self.args.run_id
        tensorboard_callback = tf.keras.callbacks.TensorBoard('data/logs/%s' % model_key,
                                                              histogram_freq=0,
                                                              write_graph=True,
                                                              write_images=False,
                                                              update_freq=2,
                                                              profile_batch=0)  # https://github.com/tensorflow/tensorboard/issues/2911

        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            'data/checkpoints/%s/%s.epoch{epoch:02d}' % (model_key, model_key), monitor='loss')

        callbacks = [tensorboard_callback, model_checkpoint_callback]
        return callbacks

    def train(self):
        train_ds = self.get_train_dataset()
        val_ds = self.get_validation_dataset()
        model = self.get_model()
        model.compile(loss=self.get_loss(), metrics=self.get_metrics())

        model.fit(train_ds, validation_data=val_ds, epochs=self.args.epochs, callbacks=self.get_callbacks())


@ex.config
def config():
    model_name = 'build_model'
    model_params = {}

    loss_name = 'ce'
    loss_params = {}

    env = edict()

    run_name = None
    run_id = f'{run_name}_{int(time.time())}'

    epochs = 1


@ex.main
def main(_config, _log, _run):
    _log.info(_run._id)
    trainer = Trainer(_config, _run, _log)

    trainer.train()


if __name__ == '__main__':
    ex.run_commandline()
