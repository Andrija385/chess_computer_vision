import tensorflow as tf
import os

class_names = ['white king','white queen','white rook','white bishop','white knight','white pawn',
               'black king','black queen','black rook','black bishop','black knight','black pawn','tile']
def create_model1(saved,name=''):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(32,32,1)),
        tf.keras.layers.Rescaling(1./255),
        #tf.keras.layers.RandomTranslation(height_factor=0.15,width_factor=0.15,fill_mode='reflect'),
        #tf.keras.layers.RandomRotation(factor=0.1,fill_mode='reflect'),
        tf.keras.layers.Conv2D(32,4,activation='relu'),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128,activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(13,activation='softmax')
    ])
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    if saved:
        model.load_weights('../models/prvidobar.keras')
    return model
def create_model100(saved,name='model100_novi_weights'):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(32, 32, 1)),
        tf.keras.layers.Rescaling(1. / 255),
        # tf.keras.layers.RandomRotation(factor=0.05,fill_mode='reflect'),
        tf.keras.layers.RandomTranslation(height_factor=0.1, width_factor=0.1, fill_mode='reflect'),
        # tf.keras.layers.RandomContrast(0.1),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(13, activation='softmax')
    ])
    if saved:
        model.load_weights(os.path.join('../models',name))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
