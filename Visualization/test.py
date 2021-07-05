import happybase as hb
import pandas as pd

conn = hb.Connection(host="sandbox-hdp.hortonworks.com",port=9097,transport="buffered",protocol="binary")
conn.open()

df = pd.DataFrame(conn.tables())
print(df)

for index, row in df.iterrows():
   row[0] = row[0].decode('UTF-8')

print(df)
print(len(df.index))
