import csv
import glob
import pandas as pd

path = './corona_data_time_province/'
merge_path = './TimeProvince.csv'

# merge대상 파일을 확인
file_list = glob.glob(path + '*')
print(file_list)

with open(merge_path, 'w', encoding='utf-8') as f :
    for i, file in enumerate(file_list) :
        if i == 0 :
            with open(file, 'r', encoding='utf-8') as f2 :
                while True :
                    line = f2.readline()

                    if not line :
                        break

                    f.write(line)
        else :
            with open(file, 'r', encoding='utf-8') as f2 :
                n = 0
                while True :
                    line = f2.readline()
                    if n != 0 :
                        f.write(line)

                    if not line :
                        break
                    n += 1

