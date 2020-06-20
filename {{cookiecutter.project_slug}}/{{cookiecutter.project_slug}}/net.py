import tensorflow as tf


def build_model(params=None):
    layers = tf.keras.layers
    model = tf.keras.Sequential([
        tf.keras.Input([28, 28, 1]),
        layers.Conv2D(16, [3, 3], strides=2),
        layers.BatchNormalization(),
        layers.ReLU(),
        layers.Conv2D(32, [3, 3], strides=2),
        layers.BatchNormalization(),
        layers.ReLU(),
        layers.Conv2D(64, [3, 3], strides=2),
        layers.BatchNormalization(),
        layers.ReLU(),
        layers.GlobalAveragePooling2D(),
        layers.Dense(10)
    ])
    return model
