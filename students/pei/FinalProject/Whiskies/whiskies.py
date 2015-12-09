import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn import tree
from sklearn.cross_validation import cross_val_score

# load the training whiskies dataset
x = pd.read_csv('TrainWhiskies_Original_Label.csv', sep=',', header = 0).as_matrix()

# make dictionary to store ID and distillery info for the training set
#d ={}
#for i in x:
#    d[i[0]] = i[1]
dTrain = {i[0]: i[1] for i in x}

# set the column header (Label) in the csv as my target - which is what I want to predict later
y= pd.read_csv('TrainWhiskies_Label.csv', delimiter=',', dtype = 'int')
target = pd.DataFrame.as_matrix(y['Label'])

# decided not to use Latitude and Longitude as features, seems to be too noisy
# data are the data for the features I want to use to train my model
data = pd.DataFrame.as_matrix(y[['Body','Sweetness','Smoky','Medicinal','Tobacco','Honey','Spicy','Winey','Nutty','Malty','Fruity','Floral']])

print ('Training Data:')
for position, label in enumerate(target):
    #print(position+1)
    if label == 1:
        print(dTrain[position+1], 'yes')
    else:
        print(dTrain[position+1], 'no')

# traingin the model using selected data and the target
model= tree.DecisionTreeClassifier()
model= model.fit(data, target)
print("Here is the details of my model:")
print(model)

# check the model accuracy by cross validation: 4 folds
scores = cross_val_score(model, data, target, cv = 4)
print("Model Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# Prediction 
a = pd.read_csv('PredictWhiskies_Original.csv', sep=',', header = 0).as_matrix()
# make dictionary to store ID and distillery info for dataset to be predicted
dPredict= {i[0]: i[1] for i in a}

# load the dataset to be predicted
b = np.genfromtxt('PredictWhiskies.csv', skip_header =1, delimiter=',', dtype = 'int')

# predict labels on the dataset b
r = model.predict(b)

#print out the result 
print('Predicted Results:')
for position, label in enumerate(r):
    #print(position+1)
    if label == 1:
        print(dPredict[position+1], 'yes')
    else:
        print(dPredict[position+1], 'no')

#to save tree in a document
with open("whiskieModel.dot", 'w') as f:
    f = tree.export_graphviz(model, out_file=f)

#to delete the file
#os.unlink('whiskieModel.dot')

