import happybase as hb
import pandas as pd

connection = hb.Connection(host="sandbox-hdp.hortonworks.com",port=9097,transport="buffered",protocol="binary")
connection.open()

eng_pos_count = round(267241*0.7)
eng_neg_count = round(267241*0.3)
chi_pos_count = round(95693*0.65)
chi_neg_count = round(95693*0.35)
mal_pos_count = round(174824*0.68)
mal_neg_count = round(174824*0.32)

if b"sentiment_count" in connection.tables():

    connection.delete_table("sentiment_count", disable=True)
    
connection.create_table(
    'sentiment_count',
    {
    'language': dict(),
    'count': dict()
    }
)

table = connection.table('sentiment_count')
print(table)

table.put('1', {'language:language': 'english',
                'count:positive': str(eng_pos_count),
                'count:negative': str(eng_neg_count)})
table.put('2', {'language:language': 'chinese',
                'count:positive': str(chi_pos_count),
                'count:negative': str(chi_neg_count)})
table.put('3', {'language:language': 'malay',
                'count:positive': str(mal_pos_count),
                'count:negative': str(mal_neg_count)})

print("Sentiment count inserted into HBase")