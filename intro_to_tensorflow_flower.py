import glob
import os
import shutil
import time

import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.python import keras
from keras.preprocessing.image import ImageDataGenerator
import logging
import scipy.integrate

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

start_time = time.time()

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

# Data loading from URL
_URL = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
zip_file = tf.keras.utils.get_file(origin=_URL, fname="flower_photos.tgz", extract=True)
base_dir = os.path.join(os.path.dirname(zip_file), 'flower_photos')

classes = ['roses', 'daisy', 'dandelion', 'sunflowers', 'tulips']

for flower_class in classes:
    img_path = os.path.join(base_dir, flower_class)
    images = glob.glob(img_path + '/*.jpg')
    print(f"{flower_class}: {images} Images")
    train, val = images[:round(len(images) * 0.8)], images[round(len(images) * 0.8):]

    training_dir = os.path.join(base_dir, 'train', flower_class)
    if not os.path.exists(training_dir):
        os.makedirs(training_dir)
        for t in train:
            shutil.move(t, training_dir)


    validation_dir = os.path.join(base_dir, 'val', flower_class)
    if not os.path.exists(validation_dir):
        os.makedirs(validation_dir)
        for v in val:
            shutil.move(v, validation_dir)



train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'val')
print(f'Base directory for downloads {base_dir}')

BATCH_SIZE = 100  # Number of training examples to process before updating our models variables
IMG_SHAPE = 150  # Our training data consists of images with width of 150 pixels and height of 150 pixels

total_val = 0
total_train = 0
for flower in classes:

    train_flower_dir = os.path.join(train_dir, flower)
    val_flower_dir = os.path.join(val_dir, flower)

    # Count training and validation images that were downloaded
    num_flower_train = len(os.listdir(train_flower_dir))
    num_flower_val = len(os.listdir(val_flower_dir))
    total_train += num_flower_train
    total_val += num_flower_val

print(f'total training {flower} images: {total_train}')
print(f'total validation {flower} images:', total_val)

quit()


# Data Preparation
train_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data

# Generators load images from disk, apply rescaling, and resize images
train_data_gen = train_image_generator.flow_from_directory(batch_size=BATCH_SIZE,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_SHAPE, IMG_SHAPE),  # (150,150)
                                                           class_mode='binary')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=BATCH_SIZE,
                                                              directory=validation_dir,
                                                              shuffle=False,
                                                              target_size=(IMG_SHAPE, IMG_SHAPE),  # (150,150)
                                                              class_mode='binary')
# Visualize Training Images
sample_training_images, _ = next(train_data_gen)


# This function will plot images in the form of a grid with 1 row
# and 5 columns where images are placed in each column.
def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20, 20))
    axes = axes.flatten()
    for img, ax in zip(images_arr, axes):
        ax.imshow(img)
    plt.tight_layout()
    plt.show()


image_gen = ImageDataGenerator(rescale=1. / 255, horizontal_flip=True)

train_data_gen = image_gen.flow_from_directory(batch_size=BATCH_SIZE,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=(IMG_SHAPE, IMG_SHAPE))

augmented_images = [train_data_gen[0][0][0] for i in range(5)]
plotImages(augmented_images)

image_gen = ImageDataGenerator(rescale=1. / 255, zoom_range=0.5)

train_data_gen = image_gen.flow_from_directory(batch_size=BATCH_SIZE,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=(IMG_SHAPE, IMG_SHAPE))

augmented_images = [train_data_gen[0][0][0] for i in range(5)]
plotImages(augmented_images)

image_gen_train = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

train_data_gen = image_gen_train.flow_from_directory(batch_size=BATCH_SIZE,
                                                     directory=train_dir,
                                                     shuffle=True,
                                                     target_size=(IMG_SHAPE, IMG_SHAPE),
                                                     class_mode='binary')

image_gen_val = ImageDataGenerator(rescale=1. / 255)

val_data_gen = image_gen_val.flow_from_directory(batch_size=BATCH_SIZE,
                                                 directory=validation_dir,
                                                 target_size=(IMG_SHAPE, IMG_SHAPE),
                                                 class_mode='binary')

plotImages(sample_training_images[:5])  # Plot images 0-4

# Model Creation
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(2)
])

# Compile Model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Prints a text summary of the model
model.summary()

# Train the Model
EPOCHS = 100
history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=int(np.ceil(total_train / float(BATCH_SIZE))),
    epochs=EPOCHS,
    validation_data=val_data_gen,
    validation_steps=int(np.ceil(total_val / float(BATCH_SIZE)))
)

# Visualizing Result of Training
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(EPOCHS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

print(f"Elapsed time: {time.time() - start_time}")
