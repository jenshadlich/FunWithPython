import tensorflow as tf

# logical AND

T, F = 1., -1.
bias = 1.
train_in = [
    [T, T, bias],
    [T, F, bias],
    [F, T, bias],
    [F, F, bias],
]

train_out = [
    [T],
    [F],
    [F],
    [F],
]

w = tf.Variable(tf.random_normal([3, 1]))


def step(x):
    is_greater = tf.greater(x, 0)
    as_float = tf.to_float(is_greater)
    doubled = tf.multiply(as_float, 2)
    return tf.subtract(doubled, 1)


output = step(tf.matmul(train_in, w))
error = tf.subtract(train_out, output)
mse = tf.reduce_mean(tf.square(error))

delta = tf.matmul(train_in, error, transpose_a=True)
train = tf.assign(w, tf.add(w, delta))

session = tf.Session()
session.run(tf.global_variables_initializer())

err, target = 1, 0
epoch, max_epochs = 0, 10
while err > target and epoch < max_epochs:
    epoch += 1
    err, _ = session.run([mse, train])
    print('epoch:', epoch, 'mse:', err)
