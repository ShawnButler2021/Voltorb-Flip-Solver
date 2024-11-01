import os
from PIL import Image
import random
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.model_selection import train_test_split
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import sys


def fluff_dataset():
	path = '.\\pictures'
	for i in range(0,2):
		for folder in os.listdir('.\\pictures'):
			for picture in os.listdir(path+'\\'+folder):
				img = Image.open(path+'\\'+folder+'\\'+picture)
				img = img.rotate(random.randint(5,30)*random.choice([-1,1]))
				img.save(path+'\\'+folder+'\\x-'+picture)


	for folder in os.listdir('.\\pictures'):
		for index,picture in enumerate(os.listdir(path+'\\'+folder)):
			os.rename(path+'\\'+folder+'\\'+picture, path+'\\'+folder+'\\y-'+str(index)+'.png')

	for folder in os.listdir('.\\pictures'):
		for index,picture in enumerate(os.listdir(path+'\\'+folder)):
			os.rename(path+'\\'+folder+'\\'+picture, path+'\\'+folder+'\\'+str(index)+'.png')



def build_and_train_model(acc):
	path = '.\\pictures'
	image_size = (30,30)
	num_classes = 10
	batch_size = 32
	epochs = 10

	images = []
	labels = []
	for label, folder in enumerate(os.listdir(path)):
		fpath = os.path.join(path,folder)
		for filename in os.listdir(fpath):
			filepath = os.path.join(fpath,filename)
			img_array = img_to_array(load_img(filepath, target_size=image_size)) / 255.0
			images.append(img_array)
			labels.append(label)
	x = np.array(images)
	y = np.array(labels)





	model = tf.keras.models.Sequential()
	image_shape = (30,30,3)
	model.add(tf.keras.layers.Conv2D(32,(3,3), activation='relu', input_shape=image_shape))
	model.add(tf.keras.layers.MaxPooling2D(2, 2))
	model.add(tf.keras.layers.Conv2D(64,(3,3), activation='relu'))
	model.add(tf.keras.layers.MaxPooling2D(2, 2))
	model.add(tf.keras.layers.Conv2D(128,(3,3), activation='relu'))
	model.add(tf.keras.layers.MaxPooling2D(2, 2))
	model.add(tf.keras.layers.Flatten())
	model.add(tf.keras.layers.Dense(128,activation='relu'))
	model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))


	model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

	val_acc = 0
	while val_acc < acc:
		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
		model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

		_, val_acc = model.evaluate(x_test,y_test)
		print(f'Validation Accuracy: {val_acc:.4f}')

	model.save('digits.keras')


if __name__ == '__main__':
	build_and_train_model(.985)