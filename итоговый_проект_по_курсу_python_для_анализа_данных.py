# -*- coding: utf-8 -*-
"""Итоговый проект по курсу Python для анализа данных

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MfOsiori5kCb9LxofOUci9aJQK5zebma
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""1. Загрузка файла"""

df = pd.read_csv('/content/HR.csv')
df.head(20)

df.info()

df.isnull().any()

"""2. Основные статистики для переменных
(среднее,медиана,мода,мин/макс,сред.отклонение).

Max/min
"""

df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']].max()

df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']].min()

"""Среднеарифметическое"""

df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']].mean()

"""Медиана"""

df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']].median()

"""Сред.отклонение"""

df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']].std()

"""Мода"""

df.mode()

"""3. Рассчитайте и визуализировать корреляционную матрицу для
количественных переменных

   Определите две самые скоррелированные и две наименее
скоррелированные переменные
"""

df_new = df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']]

sns.set(rc={'figure.figsize':(8, 6)})
sns.heatmap(df_new.corr(), annot=True, cmap='crest')

"""Две самые скоррелированные переменные

number_project и average_montly_hours

number_project и last_evaluation

Две наименее скоррелированные переменные

satisfaction_level и last_evaluation

satisfaction_level и average_montly_hours

4. Сколько сотрудников работает в каждом
департаменте.
"""

df.groupby('department')['department'].count()

"""5. Распределение сотрудников по зарплатам"""

df.groupby('salary')['salary'].count().plot(kind="barh")

"""6. Распределение сотрудников по зарплатам в каждом
департаменте по отдельности
"""

df_dep = df.groupby([df['department'],df['salary']])[['salary']].count()
df_dep

pd.crosstab(df.department,df.salary).plot(kind='bar')
 plt.title('Distribution of employees by salary')
 plt.xlabel('Department')

"""7. Гипотеза, сотрудники с высоким окладом
проводят на работе больше времени, чем сотрудники с низким
окладом

"""

df_high = (df.loc[df['salary'] == 'high']['average_montly_hours'])

df_low = (df.loc[df['salary'] == 'low']['average_montly_hours'])

df_high.plot(kind='hist',
                     alpha = 0.5,
                     bins=20,
                     label='high',
                     density = True)
df_low.plot(kind='hist',
                     alpha = 0.5,
                     bins=20,
                     label='low',
                     density = True)
plt.legend(loc='upper left')
plt.title('Сравнение времени проведенного на работе')

"""Вывод

Оклад особо не влият на количество времени проведенного сотрудником на работе

8. Рассчитать следующие показатели среди уволившихся и не
    уволившихся сотрудников (по отдельности):

  ● Доля сотрудников с повышением за последние 5 лет

  ● Средняя степень удовлетворенности
  
  ● Среднее количество проектов
"""

#Количество уволившихся и не уволившихся сотрудников
df['left'].value_counts()

df_left = df.loc[df['left'] == 1]

# доля сотрудников получивших повышение в течении 5 лет среди уволившихся
len(df_left.loc[df_left['promotion_last_5years'] == 1])/len(df_left)*100

# средняя степень удовлетворенности среди уволившихся
df_left['satisfaction_level'].mean()

# среднее количество проектов среди уволившихся
df_left['number_project'].mean()

df_noleft = df.loc[df['left'] == 0]

# доля сотрудников получивших повышение в течении 5 лет среди не уволившихся
len(df_noleft.loc[df_noleft['promotion_last_5years'] == 1])/len(df_noleft)*100

# средняя степень удовлетворенности среди не уволившихся
df_noleft['satisfaction_level'].mean()

# среднее количество проектов среди не уволившихся
df_noleft['number_project'].mean()

# сравнение степени удовлетворенности и кол-ва проектов уволившихся и не уволившихся
# средняя степень удовлетворенности и среднее количество проектов
df.groupby('left')[['satisfaction_level', 'number_project']].mean()

"""9. Разделить данные на тестовую и обучающую выборки

  Построить модель LDA, предсказывающую уволился ли
  сотрудник на основе имеющихся факторов (кроме department и
  salary)

  Оценить качество модели на тестовой выборки
"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df_new= df[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'Work_accident', 'left', 'promotion_last_5years']]
df_new

left = pd.array(df_new['left'])

X_train, X_test, y_train, y_test = train_test_split(df_new[['satisfaction_level','last_evaluation','number_project',
                                                            'average_montly_hours','time_spend_company','Work_accident',
                                                            'promotion_last_5years']], left, test_size=0.20)

lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)

result = pd.DataFrame([y_test, lda.predict(X_test)]).T
result

accuracy_score(y_test, lda.predict(X_test))