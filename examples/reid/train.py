import numpy as np
from keras.optimizers import RMSprop, SGD
from keras.callbacks import ModelCheckpoint
from keras.models import Model
from utils import image_quintuple_generator as iqg
import reid_net
import utils
from sklearn.preprocessing import LabelBinarizer as LB


input_shape = (256,256,3,)
crop_shape = (224,224,3,)
epochs = 15
steps_per_epoch = 1500
base_model = 'xception'
batch_size = 8
lst_file = '../data/train.lst.npz'


gen = iqg(lst_file,batch_size=batch_size,
        input_shape=input_shape, crop_shape=crop_shape)
model = reid_net.reid_net(input_shape=crop_shape,base_model=base_model)
#model.load_weights('../models/resnet50.weight.14.hdf5')
#rms = RMSprop()
#sgd = SGD()
sgd = SGD(lr=0.01, momentum=0.9, decay=0.0005)
model.compile(loss='categorical_crossentropy', optimizer=sgd,loss_weights=[1,0.5,0.5],metrics=['accuracy'])
check_pointer = ModelCheckpoint(filepath='../models/'+base_model+'.weight.{epoch:02d}.hdf5',
        verbose=1,save_best_only=False,save_weights_only=True)

model.fit_generator(gen,steps_per_epoch=steps_per_epoch,epochs=epochs,callbacks=[check_pointer])



