import pickle
import numpy as np

with open('btc.pkl','rb') as f:
    df = pickle.load(f)

timedelay = 60

X = df
y = np.random.choice([0,0],size=len(df)-timedelay)
for i in range(y):
    y = df[i+timedelay][0][0]/df[i][0][0] - 1
        
from tensorflow.keras import models, layers


batchsize = 60
epochs = 60
n_features = 401

model = models.Sequential(name="DeepNN", layers=[
    ### hidden layer 1
    layers.Dense(name="h1", input_dim=n_features,
                 units=int(round((n_features+1)/2)), 
                 activation='relu'),
    layers.Dropout(name="drop1", rate=0.2),
    
    ### hidden layer 2
    layers.Dense(name="h2", units=int(round((n_features+1)/4)), 
                 activation='relu'),
    layers.Dropout(name="drop2", rate=0.2),
    
    ### layer output
    layers.Dense(name="output", units=1, activation='sigmoid')
])
# model.summary()

# Perceptron
inputs = layers.Input(name="input", shape=(3,))
outputs = layers.Dense(name="output", units=1, activation='linear')(inputs)
model = models.Model(inputs=inputs, outputs=outputs, name="Perceptron")

# DeepNN
### layer input
inputs = layers.Input(name="input", shape=(n_features,))
### hidden layer 1
h1 = layers.Dense(name="h1", units=int(round((n_features+1)/2)), activation='relu')(inputs)
h1 = layers.Dropout(name="drop1", rate=0.2)(h1)
### hidden layer 2
h2 = layers.Dense(name="h2", units=int(round((n_features+1)/4)), activation='relu')(h1)
h2 = layers.Dropout(name="drop2", rate=0.2)(h2)
### layer output
outputs = layers.Dense(name="output", units=1, activation='sigmoid')(h2)
model = models.Model(inputs=inputs, outputs=outputs, name="DeepNN")

# compile the neural network
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics='accuracy')
eval = model.evaluate(X,y)
print("Total Number of Profitable Opportunities: " + str(sum(x for x in y if x > 0) - sum(x for x in y if x < 0)) + ".")
print("Time Delay: " + str(timedelay) + ". Batch Size: " + str(batchsize) + ". Epochs: " + str(epochs) + ".")
print("Number of Predictions: " + str(sum(x for x in model.predict(X) if x > 0) - sum(x for x in model.predict(X) if x < 0)) + ".")
print("Accuracy: " + str(100*round(eval[1],2)) + "%")