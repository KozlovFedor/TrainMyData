import numpy as np
import pandas as pd
import os

"""
Описание общих колонок:
idBP - ID торговой точки, которая закупает товар.
idFilial - ID филиала, в котором совершена покупка. Филиалом считается регион - набор городов.
KanalDB - ID канала дистрибьюции, по которому торговая точка совершает покупку.
idGrp - ID группы товаров, например, “обои”, “клей” и т.д.
idSubGrp - ID подгруппы товаров.
idItem - конкретный ID товара.
idTypeItem - тип товара.
value - количество проданных товаров. Отрицательное значение может означать возврат товара
"""
"""
train_set_days.csv
Файл, где продажи приведены для каждого дня.
Дополнительные колонки:
Date - дата продаж.
idSlp - ID менеджера.
City - город.

train_set_weeks.csv
Файл, где продажи приведены для каждой недели года.
wk - номер недели, представляющий собой строку вида “<год><порядковый номер недели в этом году>”.
N wk - сквозной номер недели по порядку.

train_set_sfa.csv
Данные по клиентской активности, соответствующие train_set.
visit_date - дата записи посещения точки idBP филиала idFilial.
visits_count - количество посещений данной точки в дату visit_date.
calls_count - количество звонков, поступивших на данную точку в дату visit_date в филиал idFilial.
calc_share - доля выкладки данного бренда на полки.

info_business_points.csv
Размеры тогровых точек.
size - Категория размера точки idBP (малый, средний, большой)
size_value - Поянение категории (фактическое диапазонное значение размера точки)

info_groups.csv
Информация об отношениях между idGrp, idSubGrp и idTypeItem. 
Различные комбинации этих параметров, встречающихся в датасетах.

info_items.csv
Информация о связи между параметрами idGrp, idSubGrp, idTypeItem и idItem. 
В этом файле отражено к каким группам, подгруппам и типам относятся товары с различными idItem, встречающимися в данных.

test_set_weeks.csv
Файл, где продажи приведены для каждой недели года за последние 10 недель. 
Аналогично файлу train_set_weeks с отсутствующей колонкой value, которую необходимо предсказать.

sample_submission.csv
Пример решения, которое необходимо отправить. 
В отправляемом файле обязательно должны присутствовать колонки id и value, предсказанное для каждой строки.
"""


data_path = "data"

file_data_dictionary = {}
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        file_data_dictionary[os.path.splitext(file)[0]] = pd.read_csv("{}/{}".format(data_path, file))
#%%
"""
Преобразование категореальных признаков
"""
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack

enc = OneHotEncoder(dtype=np.int64)
X_train_cat = enc.fit_transform(file_data_dictionary['train_set_weeks'][['idFilial', 'KanalDB', 'idSubGrp']])
X = file_data_dictionary['train_set_weeks']['N wk'].to_frame()
y = file_data_dictionary['train_set_weeks']['value']

X = hstack([X, X_train_cat])
#%%
from sklearn.linear_model import Ridge
model = Ridge(alpha=1)
model.fit(X, y)

X_test = file_data_dictionary['test_set_weeks']['N wk'].to_frame()
X_test_cat = enc.transform(file_data_dictionary['test_set_weeks'][['idFilial', 'KanalDB', 'idSubGrp']])
X_test = hstack([X_test, X_test_cat])
y_test = model.predict(X_test)
#%%
