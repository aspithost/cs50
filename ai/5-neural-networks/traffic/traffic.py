import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network perfmormance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    for i in range(NUM_CATEGORIES):
        folderpath = os.path.join(data_dir, str(i))
        for filename in os.listdir(folderpath):
            filepath = os.path.join(folderpath, filename)
            img = cv2.imread(filepath)
            img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
            images.append(np.array(img))
            labels.append(i)
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(
        8, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ))
    model.add(tf.keras.layers.Conv2D(
        8, (3, 3), activation="relu"
    ))
    model.add(tf.keras.layers.Conv2D(
        8, (3, 3), activation="relu"
    ))
    model.add(tf.keras.layers.Conv2D(
        8, (3, 3), activation="relu"
    ))
    model.add(tf.keras.layers.Conv2D(
        8, (3, 3), activation="relu"
    ))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Conv2D(
        16, (3, 3), activation="relu"
    ))

    model.add(tf.keras.layers.Dropout(0.25))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.4))

    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    # 8,8,8,8,8,pool,16,0.25,128,0.4
    # loss: 0.0695 - accuracy: 0.9820
    # loss: 0.0674 - accuracy: 0.9840
    # loss: 0.0861 - accuracy: 0.9773
    # loss: 0.0668 - accuracy: 0.9844

    # 8,8,8,16,32,pool,64,0.25,128,0.4
    # loss: 0.0586 - accuracy: 0.9855
    # loss: 0.0599 - accuracy: 0.9903
    # loss: 0.0492 - accuracy: 0.9873
    # loss: 0.0499 - accuracy: 0.9891

    # 8,8,8,8,16,pool,32,0.25,128,0.4
    # loss: 0.0691 - accuracy: 0.9849
    # loss: 0.0521 - accuracy: 0.9856
    # loss: 0.0543 - accuracy: 0.9883

    # 32, .25, 256, .25
    # loss: 0.0607 - accuracy: 0.9879
    # loss: 0.0783 - accuracy: 0.9827

    # 32, .25, 128, .25
    # loss: 0.0644 - accuracy: 0.9848
    # loss: 0.0849 - accuracy: 0.9832

    # 32, .25, 128, .3
    # loss: 0.0616 - accuracy: 0.9870
    # loss: 0.0761 - accuracy: 0.9841

    # 32, .25, 128, .4
    # loss: 0.0657 - accuracy: 0.9853
    # loss: 0.0602 - accuracy: 0.9858
    # loss: 0.0628 - accuracy: 0.9868

    # 32, .25, 128, .5
    # loss: 0.0613 - accuracy: 0.9849
    # loss: 0.0589 - accuracy: 0.9851

    # 32, .4, 128, .4
    # loss: 0.0524 - accuracy: 0.9870
    # loss: 0.0900 - accuracy: 0.9784

    # 2x 8, Pool, 32, .25, 128, .4
    # loss: 0.0651 - accuracy: 0.9843
    # loss: 0.0521 - accuracy: 0.9847
    # loss: 0.0862 - accuracy: 0.9775

    # 2x 8, pool, 2x 32, pool, .25, 128, .4
    # loss: 0.0777 - accuracy: 0.9784
    # loss: 0.0579 - accuracy: 0.9849

    # 8, 32, pool, 64, pool, 64, .25, 128, .4
    # loss: 0.0839 - accuracy: 0.9809
    # loss: 0.0710 - accuracy: 0.9818

    # 8, 32, pool, 8, 32, pool, .25, 128, .4
    # loss: 0.0754 - accuracy: 0.9821
    # loss: 0.1136 - accuracy: 0.9732

    # 8, 8, pool, 8, 16, 32, 0.25, 128, 0.4
    # loss: 0.0980 - accuracy: 0.9753
    # loss: 0.0807 - accuracy: 0.9795

    # 8, 8, pool, 8, 16, 32, pool, 0.25, 128, 0.4
    # loss: 0.0914 - accuracy: 0.9755

    # 8, 8, 8, pool, 16, 32, pool 0.25, 128, 0.4
    # loss: 0.0677 - accuracy: 0.9829
    # loss: 0.0618 - accuracy: 0.9837
    # loss: 0.0742 - accuracy: 0.9807
    # loss: 0.0885 - accuracy: 0.9778

    model.summary()

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
