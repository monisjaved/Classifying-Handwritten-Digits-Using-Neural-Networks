'''
Comparing single layer MLP with deep MLP (using TensorFlow)
'''

import numpy as np
import pickle
from math import sqrt
from scipy.optimize import minimize

# Do not change this
def initializeWeights(n_in,n_out):
    """
    # initializeWeights return the random weights for Neural Network given the
    # number of node in the input layer and output layer

    # Input:
    # n_in: number of nodes of the input layer
    # n_out: number of nodes of the output layer
                            
    # Output: 
    # W: matrix of random initial weights with size (n_out x (n_in + 1))"""
    epsilon = sqrt(6) / sqrt(n_in + n_out + 1);
    W = (np.random.rand(n_out, n_in + 1)*2* epsilon) - epsilon;
    return W

def feedForward(inputs, weight):
    net = np.dot(inputs, weight.T)
    out = sigmoid(net)
    return out

def computeGradient(training_data, out_hidden, w2, out_output, train_label):
    deltaL = out_output - train_label

    # print np.count_nonzero(deltaL)

    # exit(0)

    gradient_out = np.dot(deltaL.T, out_hidden)

    gradient_out *= (training_data.shape[0] ** -1) 

    # print gradient_out.shape

    # print out_hidden.shape
    # print w2.shape
    # print training_data.shape
    # print deltaL.shape

    gradient_hidden = np.dot(training_data.T, np.dot(deltaL, w2) * out_hidden * ( 1 - out_hidden))

    gradient_hidden = gradient_hidden[:,:-1]

    gradient_hidden = gradient_hidden.T

    gradient_hidden *= (training_data.shape[0] ** -1) 



    # print(gradient_hidden.shape,gradient_out.shape)
    # exit(0)

    return gradient_hidden,gradient_out

def addRegularization(training_data, w1, w2, obj_val, gradient_hidden, gradient_out, lambdaval):
    obj_val += (lambdaval/(2*training_data.shape[0])) * (np.sum(w1 * w1) + np.sum(w2 * w2))

    gradient_out += (training_data.shape[0] ** -1) *  (lambdaval * w2)

    gradient_hidden += (training_data.shape[0] ** -1) * (lambdaval * w1)

    # print(gradient_hidden.shape,gradient_out.shape)
    # exit(0)

    return obj_val,gradient_hidden,gradient_out


# Replace this with your sigmoid implementation
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-1.0 * z))
# Replace this with your nnObjFunction implementation
def nnObjFunction(params, *args):
    global obj_val

    n_input, n_hidden, n_class, training_data, training_label, lambdaval = args

    w1 = params[0:n_hidden * (n_input + 1)].reshape((n_hidden, (n_input + 1)))
    w2 = params[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))
    obj_val = 0

    # print w1.shape
    # print w2.shape

    # exit(0)

    train_label = np.zeros((training_label.shape[0],n_class))
    # print train_label.shape
    for i in range(len(training_label)):
        num = int(training_label[i])
        train_label[i][int(num)] = 1.0

    obj_val = 0

    # Your code here
    #
    #
    #
    #


    # print np.ones((training_data.shape[0],1)).shape

    training_data = np.hstack((training_data, np.ones((training_data.shape[0],1))))

    out_hidden = feedForward(training_data, w1)

    out_hidden = np.hstack((out_hidden, np.ones((out_hidden.shape[0],1))))

    out_output = feedForward(out_hidden, w2)

    # print(np.count_nonzero(out_output))

    # exit(0)

    obj_val = (-1.0/training_data.shape[0]) * (np.sum( np.sum( ( train_label * np.log(out_output) ) + ( (1 - train_label) * np.log(1 - out_output) ) ) ) )

    gradient_hidden, gradient_out = computeGradient(training_data, out_hidden, w2, out_output, train_label)

    # print out_hidden.shape

    # print out_output[0]


    # print gradient_hidden.shape , gradient_out.shape

    # exit(0)

    # print training_data.shape[0]



    # print temp.shape

    obj_val, gradient_hidden, gradient_out = addRegularization(training_data, w1, w2, obj_val, gradient_hidden, gradient_out, lambdaval)

    # Your code here
    #
    #
    #
    #
    #

    # print obj_val
    # exit(0)

    # exit(0)



    # Make sure you reshape the gradient matrices to a 1D array. for instance if your gradient matrices are grad_w1 and grad_w2
    # you would use code similar to the one below to create a flat array
    # obj_grad = np.concatenate((grad_w1.flatten(), grad_w2.flatten()),0)
    # obj_grad = np.array([])
    obj_grad = np.concatenate((gradient_hidden.flatten(), gradient_out.flatten()),0)

    return (obj_val, obj_grad)
    
# Replace this with your nnPredict implementation
def nnPredict(w1,w2,data):
    data = np.hstack((data, np.ones((data.shape[0],1))))

    # print training_data.shape

    out_hidden = feedForward(data, w1)
    out_hidden = np.hstack((out_hidden, np.ones((out_hidden.shape[0],1))))

    out_output = feedForward(out_hidden, w2)

    labels = np.argmax(out_output, axis = 1)
    # Your code here

    return labels

def callback(xk):
    global obj_val
    print("Object Value:",obj_val)

# Do not change this
def preprocess():
    pickle_obj = pickle.load(file=open('face_all.pickle', 'rb'))
    features = pickle_obj['Features']
    labels = pickle_obj['Labels']
    train_x = features[0:21100] / 255
    valid_x = features[21100:23765] / 255
    test_x = features[23765:] / 255

    labels = labels[0]
    train_y = labels[0:21100]
    valid_y = labels[21100:23765]
    test_y = labels[23765:]
    return train_x, train_y, valid_x, valid_y, test_x, test_y

"""**************Neural Network Script Starts here********************************"""
train_data, train_label, validation_data, validation_label, test_data, test_label = preprocess()
#  Train Neural Network
# set the number of nodes in input unit (not including bias unit)
n_input = train_data.shape[1]
# set the number of nodes in hidden unit (not including bias unit)
n_hidden = 256
# set the number of nodes in output unit
n_class = 2

# initialize the weights into some random matrices
initial_w1 = initializeWeights(n_input, n_hidden);
initial_w2 = initializeWeights(n_hidden, n_class);
# unroll 2 weight matrices into single column vector
initialWeights = np.concatenate((initial_w1.flatten(), initial_w2.flatten()),0)
# set the regularization hyper-parameter
lambdaval = 10;
args = (n_input, n_hidden, n_class, train_data, train_label, lambdaval)

#Train Neural Network using fmin_cg or minimize from scipy,optimize module. Check documentation for a working example
opts = {'maxiter' :50}    # Preferred value.

nn_params = minimize(nnObjFunction, initialWeights, jac=True, args=args,method='CG', options=opts, callback=callback)
params = nn_params.get('x')
#Reshape nnParams from 1D vector into w1 and w2 matrices
w1 = params[0:n_hidden * (n_input + 1)].reshape( (n_hidden, (n_input + 1)))
w2 = params[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))

#Test the computed parameters
predicted_label = nnPredict(w1,w2,train_data)
#find the accuracy on Training Dataset
print('\n Training set Accuracy:' + str(100*np.mean((predicted_label == train_label).astype(float))) + '%')
predicted_label = nnPredict(w1,w2,validation_data)
#find the accuracy on Validation Dataset
print('\n Validation set Accuracy:' + str(100*np.mean((predicted_label == validation_label).astype(float))) + '%')
predicted_label = nnPredict(w1,w2,test_data)
#find the accuracy on Validation Dataset
print('\n Test set Accuracy:' +  str(100*np.mean((predicted_label == test_label).astype(float))) + '%')
