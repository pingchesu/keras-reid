import reid_net
import numpy as np
import copy
import utils
from utils import image_quintuple_generator as iqg
from keras.models import Model
from sklearn.preprocessing import LabelBinarizer as LB
from keras.optimizers import SGD
from utils import image_base_generator as ibg
import model



def sel_idx(score, ratio, y):
    add_indices = np.zeros(score.shape[0])
    clss = np.unique(y)
    kmap = {v:k for k,v in enumerate(clss)}
    y_ture = np.array([kmap[i] for i in y])
    count_per_class = [sum(y==c) for c in clss]
    pred_y = np.argmax(score,axis=1)
    for cls in range(score.shape[1]):
        indices = np.where(pred_y == cls)[0]
        cls_score = score[indices,cls]
        idx_sort = np.argmax(score)
        add_num = np.min(np.ceil(count_per_class[cls] * ratio), indices.shape[0])
        add_indices[indices[idx_sort[:add_num]]] = 1


    return add_indices.astype('bool')




def cotrain(train_lst,untrain_lst,mname1,mname2,params):
    train_data = np.load(train_lst)
    untrain_data = np.load(untrain_lst)
    model1 = model.get_model(model_name=mname1)
    model2 = model.get_model(model_name=mname2)
    optimizer=SGD(lr=0.001,momentum=0.9,decay=0.005)
    model.train_model(model1,train_data,optimizer,params)
    model.train_model(model2,train_data,optimizer,params)
    clss = np.unique(train_data['label'])
    kmap = {v:k for k,v in enumerate(clss)}
    X_untrain = utils.extract_data_from_lst(untrain_data['lst'])
    lst1,lst2 = copy.deepcopy(train_data['lst']),cooy.deepcopy(train_data['lst'])
    y_train1,y_train2 = copy.deepcopy(train_data['label']),cppy.deepcopy(train_data['label'])
    for step in range(5):

        # select unlabel data# feature_model1 = Model()
        # feature_model2 = Model()
        prob1 = model1.predict(X_untrain)
        prob2 = model2.predict(X_untrain)
        pred_y = np.argmax(prob1 + prob2, axis=1)
        add_idx1 = sel_idx(prob2, add_ratio, train_data['label'])
        add_idx2 = sel_idx(prob1, add_ratio, train_data['label'])

        #add unlabel data and train
        lst1.extend(lst_untrain[add_idx1])
        lst2.extend(lst_untrain[add_idx2])
        add_y1 = clss(kmap[pred_y[add_idx1]])
        add_y2 = clss(kmap[pred_y[add_idx2]])
        y_train1 = np.vstack((y_train1,add_y1))
        y_train2 = np.vstack((y_train2,add_y2))

        train1 = {'lst':lst1, 'label':y_train1}
        train2 = {'lst':lst2, 'label':y_trian2}

        model.train_model(model1,train1,optimizer,params)
        model.train_model(model2,train2,optimizer,params)

        # remove add untrain lst
        add_idx = add_idx1 + add_idx2
        lst_untrain = lst_untrain[~add_idx]
        y_untrain = y_untrain[~add_idx]
        print('Add train size view 1: {}, view 2:{}'
              .format(add_y1.shape[0], add_y2.shape[0]))
    return model1,model2



def spaco(train_lst,untrain_lst,mname1,mname2,params):
    train_data = np.load(train_lst)
    untrain_data = np.load(untrain_lst)
    model1 = model.get_model(model_name=mname1)
    model2 = model.get_model(model_name=mname2)
    optimizer=SGD(lr=0.001,momentum=0.9,decay=0.005)
    model.train_model(model1,train_data,optimizer,params)
    model.train_model(model2,train_data,optimizer,params)
    clss = np.unique(train_data['label'])
    kmap = {v:k for k,v in enumerate(clss)}
    X_untrain = utils.extract_data_from_lst(untrain_data['lst'])
    lst1,lst2 = copy.deepcopy(train_data['lst']),cooy.deepcopy(train_data['lst'])
    y_train1,y_train2 = copy.deepcopy(train_data['label']),cppy.deepcopy(train_data['label'])
    for step in range(5):

        # select unlabel data# feature_model1 = Model()
        # feature_model2 = Model()
        prob1 = model1.predict(X_untrain)
        prob2 = model2.predict(X_untrain)
        pred_y = np.argmax(prob1 + prob2, axis=1)
        add_idx1 = sel_idx(prob2, add_ratio)
        add_idx2 = sel_idx(prob1, add_ratio)

        #add unlabel data and train
        lst1.extend(lst_untrain[add_idx1])
        lst2.extend(lst_untrain[add_idx2])
        add_y1 = clss(kmap[pred_y[add_idx1]])
        add_y2 = clss(kmap[pred_y[add_idx2]])
        y_train1 = np.vstack((y_train1,add_y1))
        y_train2 = np.vstack((y_train2,add_y2))

        train1 = {'lst':lst1, 'label':y_train1}
        train2 = {'lst':lst2, 'label':y_trian2}

        model.train_model(model1,train1,optimizer,params)
        model.train_model(model2,train2,optimizer,params)

        # remove add untrain lst
        add_idx = add_idx1 + add_idx2
        lst_untrain = lst_untrain[~add_idx]
        y_untrain = y_untrain[~add_idx]
        print('Add train size view 1: {}, view 2:{}'
              .format(add_y1.shape[0], add_y2.shape[0]))
    return model1,model2
