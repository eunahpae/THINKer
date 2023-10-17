import pymysql
import pandas as pd

conn = pymysql.connect(host='thinkerIn.mysql.pythonanywhere-services.com', user='thinkerIn', db='thinkerIn$thinker', password='pyflask9', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)
sql = 'SELECT * FROM info;'

df = pd.read_sql(sql, conn)

sql = 'SELECT * FROM result;'
df1 = pd.read_sql(sql, conn)

df1['total'] = df1.sum(axis=1)

print(df1)

sql_ans = "select answer from quiz;"
df2 = pd.read_sql(sql_ans,conn)


print(df2)


df['age_int'] = pd.to_numeric(df['age'])

def age_categorize(age_int):
    age_int = (age_int//10)*10

    return age_int

age_category = df.age_int.apply(age_categorize)

print(age_category)






