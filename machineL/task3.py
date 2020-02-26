import csv
import random
import copy
import numpy as np
import math
import matplotlib.pyplot as plt

def loadLIBSVMfile(s):
    info=[]
    with open(s) as tsvfile:
        reader = csv.reader(tsvfile,delimiter='\t')
        for row in reader:
            info.append(row)
        info = [obs[0].split(' ') for obs in info]
        label = [float(obs[0]) for obs in info]
        f1 = [list(map(float,obs[1].split(':')))[1] for obs in info]
        f2 = [list(map(float,obs[2].split(':')))[1] for obs in info]
        if len(info[0])==4:
            f3 = [list(map(float,obs[3].split(':')))[1] for obs in info]
            f3=normalize(f3)
        else:
            f3=None
        return label,normalize(f1),normalize(f2),f3

def normalize(X):
    return [x/max(X) for x in X]

def indices(X, elem):
    return [ i for i in range(len(X)) if X[i] == elem ]

def predict(row, weights):
    return 1/(1+math.exp(-(np.dot(np.array(row[1:]),np.array(weights[1:])))))

def logisticRegressionTrain(dataset, a, tol): #tol tolerance
    w = [-1+2*random.random() for i in range(len(dataset[0]))] #inits some random weights in interval [-1,1]
    dataset = copy.deepcopy(dataset)
    random.shuffle(dataset)
    iter=0
    while True:
        w_old = copy.deepcopy(w)
        iter+=1
        for row in dataset:
            pred = predict(row,w)
            err = row[0] - pred #y-yj
            w[0] = w[0] + a*err
            for i in range(len(row)-1):
                w[i + 1] = w[i + 1] + a * err * row[i+1]
        if np.linalg.norm(np.array(w)-np.array(w_old)) / np.linalg.norm(np.array(w)) < tol:
            #print("Epoch",iter)
            break
        random.shuffle(dataset)        
    return w

def leave_one_out(dataset,index):
    left_out = dataset[index]
    data=[]
    for i in range(len(dataset)):
        if i != index:
            data.append(dataset[i])

    return data,left_out

if __name__ == "__main__":
    # learning rate alpha and stop_criterion accepted nr 
    # of misclassifications when determining the weights
    learning_rate,tol = .4, 0.0005
    libsvm_input_file = 'machineL/salammbo/salammbo_a_e_binary.libsvm'



    print('Running logistic regression, with leave one out validation')
    print("Learning rate: %f \nTolerance: %f \nUsing data: %s" % (learning_rate, tol, libsvm_input_file))

    label,f1,f2,f3 = loadLIBSVMfile(libsvm_input_file)
    # yes, I'm well aware this is bad but at least the regression trainer takes general input
    if f3 != None:
        dataset = [[label[i],f1[i],f2[i],f3[i]] for i in range(len(label))] #row: normalized label, feature1, feature2
    else:
        dataset = [[label[i],f1[i],f2[i]] for i in range(len(label))]

    # for each row split the data by traning the perceptron on all except one row, 
    # then validate on excluded row and increment var "correct" if classification is correct
    correct = 0
    for i in range(len(dataset)):
        traindata, valdata = leave_one_out(dataset,i)
        weights = logisticRegressionTrain(traindata,learning_rate,tol)
        prediction = predict(valdata, weights)
        #print(prediction)
        if prediction>0.5:
            prediction=1
        else:
            prediction=0
        #print(weights)
        #print("Expected=%d, Predicted=%d" % (valdata[-1], prediction))
        if valdata[0] == prediction:
            correct = correct + 1
            #print("Correct prediction: \nValidation data: %a\nWeights: %a\n" % (valdata,weights))
        #else:
        #    print("Incorrect prediction: \nValidation data: %a\nWeights: %a\n" % (valdata,weights))
    correctly_predicted = 100*(correct/len(label))
    print("Final evaluation: %d%% correct" % (correctly_predicted))
    