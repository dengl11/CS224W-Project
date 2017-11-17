################################################
# Backend for Notebook: Community Construction 
################################################

import sys
sys.path.append("../lib")
sys.path.append("..")
from util.plotter import gray, red, blue, purple, green, pink
from GTD_Config import *
from collections import defaultdict 
from itertools import combinations
import pandas as pd
from plotly.graph_objs import *
import numpy as np
import pickle 
from dataframe_preprocessor import DataframePreprocessor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

# param
max_depth = 1

# numeric features
num_cols = [COL_year, COL_month, COL_nkill, COL_nwound, COL_success, COL_suicide]

# categorical features
cat_cols = [COL_attacktype1, COL_targtype1]
# cat_cols = [COL_country, COL_attacktype1, COL_targtype1]

# label column
label_col = COL_gname 

groups_considered = set([GROUP_ISIL, GROUP_Taliban, GROUP_SL, GROUP_FMLN, GROUP_Al, GROUP_IRA, GROUP_FARC, GROUP_NPA, GROUP_PKK, GROUP_BOKO])

preprocessor = get_full_gtd()
preprocessor.remove_cols_unless(num_cols + cat_cols + [label_col])

preprocessor.filter_rows_by_condition(COL_gname, lambda x: x in groups_considered)

# print(len(preprocessor.unique_vals_for_feature(COL_gname)))

preprocessor.encode_categorical_cols(verbose=True)

df = preprocessor.get_dataframe() 

X = df[num_cols + cat_cols]
y = df[label_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

model = XGBClassifier(max_depth = max_depth)
model.fit(X_train, y_train)

pred_train = model.predict(X_train)
pred_test = model.predict(X_test)

train_accuracy = np.round(accuracy_score(y_train, pred_train), 3)
test_accuracy = np.round(accuracy_score(y_test, pred_test), 3)

print("X_train: {}".format(X_train.shape))
print("y_train: {}".format(y_train.shape))

print("X_test: {}".format(X_test.shape))
print("y_test: {}".format(y_test.shape))


print("Train Accuracy: {}".format(train_accuracy))
print("Test Accuracy: {}".format(test_accuracy))
