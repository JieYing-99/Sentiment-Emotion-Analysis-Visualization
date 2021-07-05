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
    
def calculate_total(language):

    table = connection.table(language)
    df = pd.DataFrame(get_data_from_hbase(table))

    for index, row in df.iterrows():

        row[1] = int(float(row[1].decode('UTF-8'))) #nlikes
        row[2] = int(float(row[2].decode('UTF-8'))) #nreplies
        row[3] = int(float(row[3].decode('UTF-8'))) #nretweets
        row[6] = row[6].decode('UTF-8') #date
        row[10] = int(float(row[10].decode('UTF-8'))) #video

    sDate = pd.Series(df[b'time_dimension:date'].unique())
    sTweets = df.groupby([b'time_dimension:date'])[b'text:tweet'].agg('count')
    sLikes = df.groupby([b'time_dimension:date'])[b'numcount:nlikes'].agg('sum')
    sReplies = df.groupby([b'time_dimension:date'])[b'numcount:nreplies'].agg('sum')
    sRetweets = df.groupby([b'time_dimension:date'])[b'numcount:nretweets'].agg('sum')
    sVideo = df.groupby([b'time_dimension:date'])[b'video:video'].agg('sum')

    dfFrequency = pd.concat([sDate.reset_index(drop=True), sTweets.reset_index(drop=True), sLikes.reset_index(drop=True), sReplies.reset_index(drop=True), sRetweets.reset_index(drop=True), sVideo.reset_index(drop=True)], axis=1) 
    
    return dfFrequency


# Create tables
if b"eng_frequency" in connection.tables():

    connection.delete_table("eng_frequency", disable=True)
    
connection.create_table(
    'eng_frequency',
    {
    'time_dimension': dict(),
    'count': dict()
    }
)

if b"chi_frequency" in connection.tables():

    connection.delete_table("chi_frequency", disable=True)
    
connection.create_table(
    'chi_frequency',
    {
    'time_dimension': dict(),
    'count': dict()
    }
)

if b"mal_frequency" in connection.tables():

    connection.delete_table("mal_frequency", disable=True)
    
connection.create_table(
    'mal_frequency',
    {
    'time_dimension': dict(),
    'count': dict()
    }
)

def insert_row(table, row, row_num):
    
    table.put(str(row_num), {'time_dimension:date': str(row[0]),
                             'count:ntweets': str(row[b'text:tweet']),
                             'count:nlikes': str(row[b'numcount:nlikes']), 
                             'count:nreplies': str(row[b'numcount:nreplies']), 
                             'count:nretweets': str(row[b'numcount:nretweets']),
                             'count:videos': str(row[b'video:video'])}) 

# English
eng_table = connection.table('eng_frequency')
eng_df = calculate_total('english')

row_num = 1
for index, row in eng_df.iterrows():
    insert_row(eng_table, row, row_num)     
    row_num += 1    

# Chinese
chi_table = connection.table('chi_frequency')
chi_df = calculate_total('chineseNew')

row_num = 1
for index, row in chi_df.iterrows():
    insert_row(chi_table, row, row_num)  
    row_num += 1     

# Malay
mal_table = connection.table('mal_frequency')  
mal_df = calculate_total('malay')

row_num = 1
for index, row in mal_df.iterrows():
    insert_row(mal_table, row, row_num) 
    row_num += 1    

print("Frequency data inserted into HBase")