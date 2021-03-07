import pandas as pd
import os
import math


def get_groups(line):
    table = pd.read_excel(line, header=1)
    S = pd.Series(table.columns.tolist())
    groups = [key for i, key in enumerate(S.str.findall('....-[0-9][0-9]-[0-9][0-9]'))]
    groups = pd.Series(groups).dropna()
    groups = [key[0] for key in groups if len(key) == 1]
    return groups


def get_dataframe(line, length, groups):
    table = pd.read_excel(line, header=2, nrows=72)
    cols_empty = 0
    cols_empty_realy_empty= 0
    for i in range(length+3):
        columns = ['Предмет', 'Вид\nзанятий', 'ФИО преподавателя', '№ \nауд.']
        if i >= 1:
            columns = [f'Предмет.{cols_empty-cols_empty_realy_empty}', 'Вид\nзанятий', 'ФИО преподавателя', '№ \nауд.']
            columns[1:4] = list(map(lambda x: x+f".{cols_empty}", columns[1:4]))
            if table[columns[1]].isnull().sum()>70:
                cols_empty_realy_empty += 1
                cols_empty += 1
        pd.DataFrame({'idAndDayOfWeek': [i // 12 + 1 for i in range(6 * 12)],
                      "idAndNumOfLesson": [math.floor((i % 12) * 0.5) + 1 for i in range(6 * 12)],
                      'idAndParityOfWeek': [i % 2 + 1 for i in range(6 * 12)],
                      'idAndTitleOfLessons': table[columns[0]],
                      'idAndTypeOfLesson': table[columns[1]],
                      'idAndTeacher': table[columns[2]],
                      'idAndRoom': table[columns[3]]
                      }).to_json(f'json/{groups[i]}.json')
        cols_empty += 1

os.makedirs('json')
for link in os.listdir("files/"):
    group = get_groups('files/'+link)
    try:
        get_dataframe('files/'+link, len(group), group)
    except:
        pass
