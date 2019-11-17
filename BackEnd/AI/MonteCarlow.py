import tensorflow
import keras
from keras import Model
from keras.layers import Input
from keras.layers import Dense


def model():
    input = Input(shape=(27 ,))
    hidden = Dense(128, activation='relu')(input)
    hidden = Dense(256, activation='relu')(hidden)
    hidden = Dense(256, activation='relu')(hidden)
    hidden = Dense(128, activation='relu')(hidden)
    output = Dense(4, activation='softmax')(hidden)
    model = Model(inputs=input, outputs=output)
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model
