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

def get_language_count():

    table = connection.table('language_count')
    df = pd.DataFrame(get_data_from_hbase(table))

    for index, row in df.iterrows():
        row[0] = row[0].decode('UTF-8')
        row[1] = row[1].decode('UTF-8')

    eng_count = int(df[b'count:ntweets'][0])
    chi_count = int(df[b'count:ntweets'][1])
    mal_count = int(df[b'count:ntweets'][2])

    # print(eng_count)
    # print(chi_count)
    # print(mal_count)

    return eng_count, chi_count, mal_count

def get_sentiment_count():

    table = connection.table('sentiment_count')
    df = pd.DataFrame(get_data_from_hbase(table))

    for index, row in df.iterrows():
        row[0] = row[0].decode('UTF-8')
        row[1] = row[1].decode('UTF-8')
        row[2] = row[2].decode('UTF-8')

    # Positive
    eng_pos_count = int(df[b'count:positive'][0])
    chi_pos_count = int(df[b'count:positive'][1])
    mal_pos_count = int(df[b'count:positive'][2])

    # Negative
    eng_neg_count = int(df[b'count:negative'][0])
    chi_neg_count = int(df[b'count:negative'][1])
    mal_neg_count = int(df[b'count:negative'][2])

    # print(eng_pos_count, eng_neg_count)
    # print(chi_pos_count, chi_neg_count)
    # print(mal_neg_count, mal_neg_count)

    return eng_pos_count, eng_neg_count, chi_pos_count, chi_neg_count, mal_pos_count, mal_neg_count

def get_emotions_count():

    table = connection.table('emotions_count')
    df = pd.DataFrame(get_data_from_hbase(table))

    for index, row in df.iterrows():
        row[0] = row[0].decode('UTF-8')
        row[1] = row[1].decode('UTF-8')
        row[2] = row[2].decode('UTF-8')
        row[3] = row[3].decode('UTF-8')
        row[4] = row[4].decode('UTF-8')
        
    # English
    eng_angry = df[b'count:angry'][0]
    eng_fear = df[b'count:fear'][0]
    eng_happy = df[b'count:happy'][0]
    eng_sad = df[b'count:sad'][0]
    eng_surprise = df[b'count:surprise'][0]

    # Chinese
    chi_angry = df[b'count:angry'][1]
    chi_fear = df[b'count:fear'][1]
    chi_happy = df[b'count:happy'][1]
    chi_sad = df[b'count:sad'][1]
    chi_surprise = df[b'count:surprise'][1]

    # Malay
    mal_angry = df[b'count:angry'][2]
    mal_fear = df[b'count:fear'][2]
    mal_happy = df[b'count:happy'][2]
    mal_sad = df[b'count:sad'][2]
    mal_surprise = df[b'count:surprise'][2]

    eng_dict = {'emotion': ['angry', 'fear', 'happy', 'sad', 'surprise'], 'frequency': [eng_angry, eng_fear, eng_happy, eng_sad, eng_surprise]} 
    eng_df = pd.DataFrame(eng_dict)  
    
    chi_dict = {'emotion': ['angry', 'fear', 'happy', 'sad', 'surprise'], 'frequency': [chi_angry, chi_fear, chi_happy, chi_sad, chi_surprise]} 
    chi_df = pd.DataFrame(chi_dict)  
    
    mal_dict = {'emotion': ['angry', 'fear', 'happy', 'sad', 'surprise'], 'frequency': [mal_angry, mal_fear, mal_happy, mal_sad, mal_surprise]}
    mal_df = pd.DataFrame(mal_dict)    

    return eng_df, chi_df, mal_df

def get_frequency(language):

    language = language

    if (language == 'english'):
        table = connection.table('eng_frequency')
    elif (language == 'chinese'):
        table = connection.table('chi_frequency')
    else:
        table = connection.table('mal_frequency')
    
    df = pd.DataFrame(get_data_from_hbase(table))

    for index, row in df.iterrows():
        row[0] = int(row[0].decode('UTF-8'))
        row[1] = int(row[1].decode('UTF-8'))
        row[2] = int(row[2].decode('UTF-8'))
        row[3] = int(row[3].decode('UTF-8'))
        row[4] = int(row[4].decode('UTF-8'))
        row[5] = row[5].decode('UTF-8')

    return df

def get_each_lang_tokenized_text(language):

    language = language

    table = connection.table(language)
    df = pd.DataFrame(get_data_from_hbase(table))

    tokenized = pd.DataFrame(df[b'text:tokenized'])

    for index, row in tokenized.iterrows():
        row[0] = row[0].decode('UTF-8')

    return tokenized

def get_tokenized_text():

    eng_tokenized = get_each_lang_tokenized_text('english')
    chi_tokenized = get_each_lang_tokenized_text('chineseNew') ##chinese
    mal_tokenized = get_each_lang_tokenized_text('malay')

    eng_words = ' '.join([text for text in eng_tokenized[b'text:tokenized']]).replace("'","")
    chi_words = ' '.join([text for text in chi_tokenized[b'text:tokenized']]).replace("'","")
    mal_words = ' '.join([text for text in mal_tokenized[b'text:tokenized']]).replace("'","")

    return eng_words, chi_words, mal_words



