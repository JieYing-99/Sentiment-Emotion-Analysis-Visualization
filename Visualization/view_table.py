import happybase as hb
import pandas as pd

connection = hb.Connection(host="sandbox-hdp.hortonworks.com",port=9097,transport="buffered",protocol="binary")
connection.open()

def get_data_from_hbase(table):

    data = table.scan()
    datalist = []
    
    for row in data:
        datalist.append(row[1])
        
    return datalist


table = connection.table('emotions_count')
df = pd.DataFrame(get_data_from_hbase(table))
# print((df[b'numcount:nlikes']=='').any())
# print(df[b'numcount:nlikes'].unique())
# pd.to_datetime(df[b'time_dimension:date'])
# print(df.sort_values(by=b'time_dimension:date') )
print(df)