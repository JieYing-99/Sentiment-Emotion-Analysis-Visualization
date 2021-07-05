import happybase as hb
import pandas as pd

connection = hb.Connection(host="sandbox-hdp.hortonworks.com",port=9097,transport="buffered",protocol="binary")
connection.open()

# English
eng_happy = 1000
eng_angry = 2000
eng_surprise = 3000
eng_sad = 4000
eng_fear = 5000

# Chinese
chi_happy = 1000
chi_angry = 2000
chi_surprise = 3000
chi_sad = 4000
chi_fear = 5000

# Malay
mal_happy = 1000
mal_angry = 2000
mal_surprise = 3000
mal_sad = 4000
mal_fear = 5000

if b"emotions_count" in connection.tables():

    connection.delete_table("emotions_count", disable=True)
    
connection.create_table(
    'emotions_count',
    {
    'language': dict(),
    'count': dict()
    }
)

table = connection.table('emotions_count')
print(table)

table.put('1', {'language:language': 'english',
                'count:happy': str(eng_happy),
                'count:angry': str(eng_angry),
                'count:surprise': str(eng_surprise),
                'count:sad': str(eng_sad),
                'count:fear': str(eng_fear)})
table.put('2', {'language:language': 'chinese',
                'count:happy': str(chi_happy),
                'count:angry': str(chi_angry),
                'count:surprise': str(chi_surprise),
                'count:sad': str(chi_sad),
                'count:fear': str(chi_fear)})
table.put('3', {'language:language': 'malay',
                'count:happy': str(mal_happy),
                'count:angry': str(mal_angry),
                'count:surprise': str(mal_surprise),
                'count:sad': str(mal_sad),
                'count:fear': str(mal_fear)})

print("Emotions count inserted into HBase")