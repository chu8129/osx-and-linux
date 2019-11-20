#coding:utf8




import time
import json
import pickle
import xgboost as xgb
from run import read_one_file
from sklearn.externals import joblib

train_data_bin_path = "train.matrix.libsvm"
test_data_bin_path = "test.matrix.libsvm"
PARAM_PATH = "./parameter.json"
Vectorizer_PATH = "./vectorizer"
import sys
TASK = sys.argv[1]

if TASK == "pre":
    print("read train")
    train_x, train_y, label_dict, vectorizer = read_one_file("./train")
    print("read test")
    test_x, test_y, label_dict, vectorizer = read_one_file("./test", label_dict=label_dict, vectorizer=vectorizer)
    x_shape = len(train_x[0])
    y_shape = len(label_dict)
    dtrain = xgb.DMatrix(train_x, label=train_y)
    dtrain.save_binary(train_data_bin_path)
    dtest = xgb.DMatrix(test_x, label=test_y)
    dtest.save_binary(test_data_bin_path)
    with open(PARAM_PATH, "w") as fw:
        fw.write(json.dumps({"x_shape":x_shape, "y_shape":y_shape, "y_label_dict":label_dict,}))
    joblib.dump(vectorizer, Vectorizer_PATH, compress=9)
    print("generate data done")



# Leave most parameters as default
"""
objective[default=reg:linear]:定义最小化损失函数类型，常用参数：
binary:logistic –二元分类的逻辑回归模型，返回预测概率(p(y=1|x,w))
multi:softmax –使用softmax objective的多类分类模型，返回预测的分类。这里需要设置一个额外的num_class参数，表示类的个数。
multi:softprob –与softmax相同，但是返回每个数据点属于每个类的预测概率。
eval_metric[default according to objective]:用于衡量验证数据的参数，即是各评价标准，常用参数如下:
rmse – root mean square error
mae – mean absolute error
logloss – negative log-likelihood
error – Binary classification error rate (0.5 threshold)
merror – Multiclass classification error rate
mlogloss – Multiclass logloss
auc: Area under the curve
seed[default=0]:随机种子，用于产生可复现的结果。
这里，xgboost与sklearn的命名风格有点区别，如：
eta->learning_rate
lambda->reg_lambda
alpha->reg_alpha
"""
MODEL_PATH = 'xgboost.model'
params = json.loads(open(PARAM_PATH).read())
x_shape = params["x_shape"]
y_shape = params["y_shape"]
label_dict = params["y_label_dict"]
vectorizer = joblib.load(Vectorizer_PATH)

if TASK == "train":
    dtrain = xgb.DMatrix(data = train_data_bin_path)# + "#train_cache")
    dtest = xgb.DMatrix(data = test_data_bin_path)# + "#test_cache")
    
    # xgboost
    num_round = 2
    param = {
    	'objective': 'multi:softmax', # Specify multiclass classification
            'num_class': y_shape, # Number of possible output classes
            'tree_method': "gpu_hist",#'gpu_hist', # Use GPU accelerated algorithm
            "gpu_id":0, # Use 2th GPU
            "nthread":10,
    	"max_delta_step":1, # [default=0]:该参数可以使得更新更加平缓，如果取0表示没有约束，如果取正值则使得更新步骤更加保守，防止更新时迈的步子太大。
            "lambda":1, # [default=1]:模型的L2正则化参数，参数越大，越不容易过拟合
            "alpha":1, # [default=0]:模型的L1正则化参数，参数越大，越不容易过拟合
            "gamma":0, # [default=0]:后剪枝时，用于控制是否后剪枝
            "max_depth":6, #[default=6]:每棵树的最大深度，该参数设置越大，越容易过拟合
            "learning_rate":0.1, # default=0.3, eta
            "n_estimator":500, # num_boosting_rounds,这是生成的最大树的数目，也是最大的迭代次数 
             }
    gpu_res = {}
    
    tmp = time.time()
    print("start train")
    model = xgb.train(param, dtrain, num_round, evals=[(dtest, 'test')], evals_result=gpu_res)
    print("GPU Training Time: %s seconds" % (str(time.time() - tmp)))
    model.save_model(MODEL_PATH)
    print("model done")

if TASK == "test":
    num = 10
    model = xgb.Booster({'nthread':4})
    model.load_model(MODEL_PATH)
    original_x, original_y, test_x, test_y, label_dict = read_one_file("./test", label_dict=label_dict, return_original=1, vectorizer=vectorizer)
    label_dict = dict([_[::-1] for _ in label_dict.items()])
    test_y = [label_dict[_] for _ in test_y]
    print("test_y", test_y[:num])
    print("original_y", original_y[:num])
    ypred = model.predict(xgb.DMatrix(test_x))
    y_pred = [label_dict[_] for _ in ypred]
    print("y_pred", y_pred[:num])
    for index in range(num):
        print("original_y:%s" % original_y[index], "test_y:%s" % test_y[index], "y_pred:%s" % y_pred[index], "line:%s" % original_x[index], )
    from sklearn import metrics
    print(metrics.classification_report(original_y, y_pred))

