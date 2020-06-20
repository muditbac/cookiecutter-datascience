import tensorflow as tf
import tensorflow_datasets as tfds

AUTO = tf.data.experimental.AUTOTUNE
float32 = lambda x: tf.cast(x, tf.float32)


def build_dataset(split='train',
                  train=True,
                  dataset_name='mnist',
                  shuffle_buffer=60_000,
                  batch_size=32):
    dataset = tfds.load(dataset_name, as_supervised=True, split=split)

    if train:
        dataset = dataset.shuffle(shuffle_buffer)
    dataset = dataset.map(lambda x, y: (float32(x), y), num_parallel_calls=AUTO)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(AUTO)
    return dataset
