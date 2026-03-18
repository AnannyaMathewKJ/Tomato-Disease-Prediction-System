# -*- coding: utf-8 -*-


# Part 1 : Building a CNN

# Import Keras packages from TensorFlow
import numpy as np
from tensorflow.keras.models import Sequential  
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import plot_model


# Initializing the CNN

np.random.seed(1337)
classifier = Sequential()

# Layer 1: Convolution and Pooling
# Corrected: Convolution2D -> Conv2D, kernel size (3, 3)
classifier.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Layer 2: Convolution and Pooling
classifier.add(Conv2D(16, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Layer 3: Convolution and Pooling
classifier.add(Conv2D(8, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))


# Flattening
classifier.add(Flatten())

# Hidden Layer
# Corrected: Dropout parameter is 'rate', not 'p'
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dropout(rate = 0.5)) 

# Output Layer
classifier.add(Dense(units = 10, activation = 'softmax'))

# Compile the CNN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
print(classifier.summary())
# plot_model(classifier, show_shapes=True, to_file='PlantVillage_CNN.png') # Uncomment if you have pydot/graphviz installed

# Part 2 - Fitting the Data Set

# Data Augmentation and Scaling
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

# Prepare Training Data Generator
training_set = train_datagen.flow_from_directory(
        'train',
        target_size=(128, 128),
        batch_size=64,
        class_mode='categorical')

label_map = (training_set.class_indices)
print(label_map)

# Prepare Validation/Test Data Generator
test_set = test_datagen.flow_from_directory(
        'val',
        target_size=(128, 128),
        batch_size=64,
        class_mode='categorical')


# Calculate steps based on dataset size (assuming 10 epochs for example)
# This prevents generator errors if the number of samples isn't perfectly divisible by batch_size
steps_per_epoch = training_set.n // training_set.batch_size
validation_steps = test_set.n // test_set.batch_size


# Part 3 - Train the model
# Corrected: fit_generator -> fit
history = classifier.fit(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=10, # Changed from 10000 to a more typical 10 epochs
        validation_data=test_set,
        validation_steps=validation_steps)

print("Training Complete.")