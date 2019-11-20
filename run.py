




import time
import json
import pickle
import xgboost as xgb
from sklearn.externals import joblib


import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import collections

import numpy

def read_file(filepath,):
    with open(filepath) as fr:
        lines = fr.readlines()
        lines = [_.strip().split(",", 1) for _ in lines if _.strip()]
        check_list = [_ for _ in lines if len(_) < 2]
        print("for error check", check_list[:2])
        lines = [line for line in lines if len(line) > 1 and line[0]]
        print("for check", lines[:2])
        x,y = ([_[1] for _ in lines], [_[0] for _ in lines])
        for index in range(10):
            print("y:%s, x:%s" % (y[index], x[index]))
        return x,y

def get_vectorizer(train_x):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(analyzer="char_wb", min_df=0.0001)
    vectorizer.fit(train_x)
    return vectorizer
    
def translate_x(mini_list, vectorizer):
    import tensorflow as tf
    from extract import obj as bv
    
        
    # print(bv.encode(['今天天气不错'])[0][:30])
    # print(bv.encode(['今天天气'])[0][:30])
    
    print(">" * 20,"try translate by bert")
    train_x_new = bv.encode(mini_list)
    train_x_onehot = vectorizer.transform(mini_list).toarray()
    train_x = numpy.hstack([train_x_onehot, train_x_new])
    print(">" * 20,"train x get bert done")
    return train_x, vectorizer

def get_y_label_dict(train_y):
    return dict([_[::-1] for _ in list(enumerate(set(train_y)))])
    
def translate_y(train_y, label_dict=None):
    return [label_dict[_] for _ in train_y], label_dict

def construct_line( label, line ):
    new_line = []
    if float( label ) == 0.0:
        label = "0"
    new_line.append( str(int(label)))

    for i, item in enumerate( line ):
        if item == '' or float( item ) == 0.0:
            continue
        new_item = "%s:%s" % ( i + 1, item )
        new_line.append( new_item )
    new_line = " ".join( new_line )
    new_line += "\n"
    return new_line

def read_one_file(train_file, label_dict=None, vectorizer=None, return_original=0):
    train_x, train_y = read_file(train_file)
    if vectorizer:
        print("\n\n\nuse exists vectorizer\n\n\n")
    else:
        print("\n\n\ncreate vectorizer\n\n\n")
        vectorizer = get_vectorizer(train_x)

    if label_dict:
        pass
    else:
        label_dict = get_y_label_dict(train_y)

    batch_size = 10000
    train_x_new = []
    train_y_new = []
    count = 0
    new_train_file = train_file + ".libsvm"
    """
    with open(new_train_file, "wb") as fw:
        for x_mini_list,y_mini_list in [
                (train_x[index : index + batch_size], train_y[index : index + batch_size]) \
                for index in range(0, len(train_x), batch_size)]:
    """
    x_mini_list = train_x
    y_mini_list = train_y 
    count += len(x_mini_list)
    train_x_new, vectorizer = translate_x(x_mini_list, vectorizer)
    train_y_new, label_dict = translate_y(y_mini_list, label_dict)
    # train_x_new.append(list(train_x_new_.toarray()))
    # train_y_new.append(list(train_y_new_))
    """
    print("count:%s" % (count,))
    for index in range(len(train_x_new_)):
        data = train_x_new_[index]
        label = train_y_new_[index]
        train_x_new.append(list(data))
        train_y_new.append(label)
                line = construct_line(label, data)
                fw.write(line.encode())
    """
    if return_original:
        return train_x, train_y, train_x_new, train_y_new, label_dict
    return train_x_new, train_y_new, label_dict, vectorizer

if __name__ == "__main__":
    train_data_bin_path = "./train"
    read_one_file(train_data_bin_path)
    train_data_bin_path = "./test"
    read_one_file(train_data_bin_path)
    
"""
x_shape = len(train_x_new[0])
k = 10

w0=tf.Variable(0.1)  
w1=tf.Variable(tf.truncated_normal([x_shape]))  
w2=tf.Variable(tf.truncated_normal([x_shape,k]))  
  
x_=tf.placeholder(tf.float32,[None,x_shape])  
y_=tf.placeholder(tf.float32,[None])  
batch=tf.placeholder(tf.int32)  
  
w2_new=tf.reshape(tf.tile(w2,[batch,1]),[-1,x_shape,k])  
board_x=tf.reshape(tf.tile(x_,[1,k]),[-1,x_shape,k])  
board_x2=tf.square(board_x)  
  
q=tf.square(tf.reduce_sum(tf.multiply(w2_new,board_x),axis=1))  
h=tf.reduce_sum(tf.multiply(tf.square(w2_new),board_x),axis=1)  
  
  
  
y_fm=w0+tf.reduce_sum(tf.multiply(x_,w1),axis=1)+1/2*tf.reduce_sum(q-h,axis=1)  
  
cost=tf.reduce_sum(0.5*tf.square(y_fm-y_)) + tf.contrib.layers.l2_regularizer(0.1)(w0) + tf.contrib.layers.l2_regularizer(0.1)(w1)+tf.contrib.layers.l2_regularizer(0.1)(w2)  
batch_fl=tf.cast(batch,tf.float32)  
accury=(batch_fl+tf.reduce_sum(tf.sign(tf.multiply(y_fm,y_))))/(batch_fl*2)  
train_op=tf.train.AdamOptimizer(learning_rate=0.1).minimize(cost)  
  
with tf.Session() as sess:  
    sess.run(tf.global_variables_initializer())  
    for i in range(2000):  
        sess.run(train_op,feed_dict={x_:train_x_new,y_:train_y,batch:70})  
        print(sess.run(cost,feed_dict={x_:train_x,y_:train_y,batch:70})) 
    print(sess.run(accury,feed_dict={x_:test_x,y_:test_y,batch:30}))

"""
"""

"""
