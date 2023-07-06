import gzip
import pickle
import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

data = pd.read_csv(".\\stroke.csv")

data.drop('id', axis=1, inplace=True)

data[['hypertension', 'heart_disease', 'stroke']] = data[['hypertension', 'heart_disease', 'stroke']].astype(str)

data.drop(data[data['gender'] == 'Other'].index, inplace=True)

for col in ['avg_glucose_level', 'bmi']:
    data[col] = np.log(data[col])


# Hàm điền dữ liệu rỗng cho bmi
def knn_impute(df, na_target):
    df = df.copy()

    numeric_df = df.select_dtypes(np.number)
    non_na_columns = numeric_df.loc[:, numeric_df.isna().sum() == 0].columns

    y_train = numeric_df.loc[numeric_df[na_target].isna() == False, na_target]
    X_train = numeric_df.loc[numeric_df[na_target].isna() == False, non_na_columns]
    X_test = numeric_df.loc[numeric_df[na_target].isna() == True, non_na_columns]

    knn = KNeighborsRegressor()
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    df.loc[df[na_target].isna() == True, na_target] = y_pred

    return df


data1 = knn_impute(data, 'bmi')

# Tách tập dữ liệu thành nhị phân
data2 = pd.get_dummies(data1, drop_first=True)

# lưu tập dữ liệu để sử dụng cho chuẩn hóa dữ liệu đầu vào
data2[['age','avg_glucose_level','bmi']].to_csv('standardScaler.csv', index=False)

s = StandardScaler()
data2[['bmi', 'avg_glucose_level', 'age']] = s.fit_transform(data2[['bmi', 'avg_glucose_level', 'age']])

data3 = data2.copy()

oversample = RandomOverSampler(sampling_strategy='minority')
X = data3.drop(['stroke_1'], axis=1)
y = data3['stroke_1']
X_over, y_over = oversample.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_over, y_over, test_size=0.1, random_state=42)


SVM = SVC(probability=True, C=1, gamma=1000)
SVM.fit(X_train, y_train)


y_pred_svm = SVM.predict(X_test)
y_pred_prob_svm = SVM.predict_proba(X_test)[:, 1]


print('Accuracy:', accuracy_score(y_test, y_pred_svm))
print('ROC AUC Score:', roc_auc_score(y_test, y_pred_prob_svm))

with gzip.open('.\\Model\\svm_stroke_model.pkl.gz', 'wb') as f:
    pickle.dump(SVM, f)
