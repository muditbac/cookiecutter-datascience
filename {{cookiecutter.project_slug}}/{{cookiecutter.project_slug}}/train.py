import time

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from easydict import EasyDict as edict
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST

from .utils import get_sacred_experiment

ex = get_sacred_experiment('train_experiment', observer='file')


class Model(pl.LightningModule):

    def __init__(self):
        super().__init__()

        self.model = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),

            nn.Conv2d(16, 32, kernel_size=3, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),

            nn.Conv2d(32, 64, kernel_size=3, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),

            nn.AvgPool2d(2),
            nn.Flatten(),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        logs = {'loss': loss}
        return {'loss': loss, 'log': logs}

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        logs = {'val_loss': loss}
        return {'val_loss': loss, 'log': logs}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        loss = {'avg_val_loss': avg_loss}
        return {'log': loss}

    def train_dataloader(self):
        dataset = MNIST('data/', train=True, download=True, transform=transforms.ToTensor())
        return DataLoader(dataset, batch_size=32, shuffle=True, num_workers=0, pin_memory=True)

    def val_dataloader(self):
        dataset = MNIST('data/', train=False, download=True, transform=transforms.ToTensor())
        return DataLoader(dataset, batch_size=32, shuffle=True, num_workers=0, pin_memory=True)

    def configure_optimizers(self):
        return torch.optim.SGD(self.parameters(), lr=0.02)


@ex.config
def config():
    env = edict()

    run_name = None
    run_id = f'{run_name}_{int(time.time())}'

@ex.main
def main(_config, _log, _run):
    model = Model()
    trainer = pl.Trainer(max_epochs=4, min_epochs=1)
    trainer.fit(model)


if __name__ == '__main__':
    ex.run_commandline()
