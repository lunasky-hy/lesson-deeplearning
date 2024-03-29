import numpy as np
from ActivationFunction import sigmoid
from LossFunction import cross_entropy_error
from collections import OrderedDict
from GraphLayer import *
from NumericalMethods import numerical_gradient

class TwoLayerNetwork(object):
    def __init__(self, input_size, hidden_size, output_size, weight = 0.01):
        self.params = {}
        self.params['W1'] = weight * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

        self.layers = OrderedDict()
        self.layers['Affine1'] = AffineLayer(self.params['W1'], self.params['b1'])
        self.layers['Relu'] = ReluLayer()
        self.layers['Affine2'] = AffineLayer(self.params['W2'], self.params['b2'])
        self.lastLayer = SoftmaxWithLossLayer()
        return

    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)

        return x
    
    def loss(self, x, t):
        y = self.predict(x)
        return self.lastLayer.forward(y, t)

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis = 1)
        if t.ndim != 1:
           t = np.argmax(t, axis = 1)
        acc = np.sum(y == t) / float(x.shape[0])
        return acc

    def gradient(self, x, t):
        # forward
        self.loss(x, t)

        # backward
        dout = self.lastLayer.backward(1)
        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        grads = {}
        grads['W1'] = self.layers['Affine1'].dW
        grads['b1'] = self.layers['Affine1'].db
        grads['W2'] = self.layers['Affine2'].dW
        grads['b2'] = self.layers['Affine2'].db

        return grads