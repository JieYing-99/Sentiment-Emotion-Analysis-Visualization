import happybase as hb
import pandas as pd

# hbase table name 
table_name = "eng_frequency"

def connect_to_hbase():
    
    conn=hb.Connection(host="sandbox-hdp.hortonworks.com",port=9097,transport="buffered",protocol="binary")
    conn.open()

    table = conn.table(table_name)
    
    return conn, table

def get_data_from_hbase():
    data = table.scan()
    listing = []
    
    for row in data:
        listing.append(row[1])
        
    return listing

conn, table = connect_to_hbase()

tweet_df = pd.DataFrame(get_data_from_hbase())

# to know the column name 
print(tweet_df.columns.values.tolist())
