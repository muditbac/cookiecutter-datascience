import tensorflow as tf


def ce():
    return tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
