import settings
import numpy as np
import copy

def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))

class hidden_layer:
    """
    One hidden layer in the bug_brain NN
    """
    def __init__(self, layer_size, input_size, random=True):
        # input size is one greater for the bias term
        # layer size is the number of nodes
        self.weights = 2 * np.random.random((input_size+1, layer_size)) - 1

    def fwd_prop(self, lprev):
        # one is appended for the bias term
        return sigmoid(np.dot(np.append(lprev, 1), self.weights))

    def __str__(self):
        return str(self.weights)

class bug_brain:
    """
    manages the nueralnetwork for the bug's brain

    network_depth[]
    layer_sizes[]
    """

    def __init__(self, layer_sizes=[4,3,4], input_size=4, output_size=4):
        """
        initialize a bug brain

        layer_sizes: list of positive integers indicating the number of neurons
            per hidden layer between inputs and outputs

        inputs: list of NeuralInput objects that will be queried for running
            information
        """
        self.network_depth = len(layer_sizes)

        self.input_size = input_size
        self.network = []

        # first layer takes direct inputs
        self.network.append(hidden_layer(
            layer_size=layer_sizes[0],
            input_size=input_size))

        # each layer inputs from the previous layer
        for x in range(len(layer_sizes) - 1):
            self.network.append(hidden_layer(
                layer_size=layer_sizes[x],
                input_size=layer_sizes[x-1]))

        # format for output vector
        self.network.append(hidden_layer(
                layer_size=output_size,
                input_size=layer_sizes[len(layer_sizes) - 1]))

    def process(self, inputs):
        synapse = copy.deepcopy(inputs)
        for layer in self.network:
            synapse = layer.fwd_prop(synapse)
        return synapse




    def __str__(self):
        toReturn = "Brain Depth: {} Size: {}\n[\n"
        for layer in self.network:
            toReturn += str(layer)+ "\n"
        toReturn += "]"
        return toReturn.format(self.network_depth, self.input_size)
