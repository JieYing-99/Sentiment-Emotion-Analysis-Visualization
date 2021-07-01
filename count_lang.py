import happybase as hb
import pandas as pd

connection = hb.Connection(host="sandbox-hdp.hortonworks.com",port=9097,transport="buffered",protocol="binary")
connection.open()

eng_table = connection.table('english')
chi_table = connection.table('chineseNew')
mal_table = connection.table('malay')

def get_data_from_hbase(table):

    data = table.scan()
    datalist = []
    
    for row in data:
        datalist.append(row[1])
        
    return datalist

eng_df = pd.DataFrame(get_data_from_hbase(eng_table))
chi_df = pd.DataFrame(get_data_from_hbase(chi_table))
mal_df = pd.DataFrame(get_data_from_hbase(mal_table))

eng_count = len(eng_df.index)
chi_count = len(chi_df.index)
mal_count = len(mal_df.index)

if b"language_count" in connection.tables():

    connection.delete_table("language_count", disable=True)
    #connection.tables().remove(b"language_count")
    
connection.create_table(
    'language_count',
    {
    'language': dict(),
    'count': dict()
    }
)

table = connection.table('language_count')
print(table)

table.put('1', {'language:language': 'english',
                'count:ntweets': str(eng_count)})
table.put('2', {'language:language': 'chinese',
                'count:ntweets': str(chi_count)})
table.put('3', {'language:language': 'malay',
                'count:ntweets': str(mal_count)})

print("Language count inserted into HBase")