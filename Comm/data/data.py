import pandas as pd

def read_excel(file, **kwargs):
    data_dict = []
    try:
        data = pd.read_excel(file, **kwargs)
        data_dict = data.to_dict('records')
    finally:
        return data_dict

sheet1 = read_excel('C:\\Users\\yinghai\\PycharmProjects\\TestFrame\\Comm\\data\\baidu_fanyi.xlsx')
sheet2 = read_excel('C:\\Users\\yinghai\\PycharmProjects\\TestFrame\\Comm\\data\\baidu_fanyi.xlsx', sheet_name='Sheet2')
print(sheet1)
print(sheet2)
