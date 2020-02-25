import csv
import random
import copy
import numpy as np
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
        return label,f1,f2

def normalize(X):
    return [x/max(X) for x in X]

def indices(X, elem):
    return [ i for i in range(len(X)) if X[i] == elem ]

def predict(row, weights):
    activation = weights[0]
    for i in range(len(row)-1):
        activation += weights[i+1] * row[i]
    return 1.0 if activation >= 0.0 else 0.0

def perceptronTrain(dataset, a, stop_cond): #stop cond nr of allowed misclassifications
    w = [-1+2*random.random() for i in range(len(dataset[0]))] #inits some random weights in interval [-1,1]
    dataset = copy.deepcopy(dataset)
    random.shuffle(dataset)
    misclass = len(dataset)
    i=0
    while misclass >= stop_cond:
        for row in dataset:
            pred = predict(row,w)
            err = row[-1] - pred #y-yj
            w[0] = w[0] + a*err
            for i in range(len(row)-1):
                w[i + 1] = w[i + 1] + a * err * row[i]
        misclass = 0
        for row in dataset:
            prediction = predict(row,w)
            if prediction != row[-1]:
                misclass = misclass + 1
        i=i+1
    return w

def leave_one_out(dataset,index):
    left_out = dataset[index]
    data=[]
    for i in range(len(dataset)):
        if i != index:
            data.append(dataset[i])

    return data,left_out

if __name__ == "__main__":
    learning_rate,stop_criterion = .5,5 # learning rate alpha and stop_criterion accepted nr of misclassifications when determining the weights
    label,f1,f2 = loadLIBSVMfile('machineL/salammbo/salammbo_a_binary.libsvm')
    nf1=normalize(f1)
    nf2=normalize(f2)
    dataset = [[nf1[i],nf2[i],label[i]] for i in range(len(label))] #row: normalized feature1, feature2, label


    # for each row split the data by traning the perceptron on all except one row, then validate on excluded row and increment var "correct" if classification is correct
    correct = 0
    for i in range(len(dataset)):
        traindata, valdata = leave_one_out(dataset,i)
        weights = perceptronTrain(traindata,learning_rate,stop_criterion)
        prediction = predict(valdata, weights)
        print("Expected=%d, Predicted=%d" % (valdata[-1], prediction))
        if valdata[-1] == prediction:
            correct = correct + 1
            print(correct)
    correctly_predicted = 100*(correct/len(label))
    print("Correct classifications: %d percent" % (correctly_predicted))
    