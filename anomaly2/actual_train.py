import tensorflow as tf
import numpy as np

# create random data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.5

# Find values for W that compute y_data = W * x_data 
W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
y = W * x_data

# Minimize the mean squared errors.
print('cal')
loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)
print('cal2')
# Before starting, initialize the variables
init = tf.global_variables_initializer()

# Launch the graph.
sess = tf.Session()
sess.run(init)

# Fit the line.
for step in xrange(2001):
    sess.run(train)
    if step % 200 == 0:
        print(step, sess.run(W))