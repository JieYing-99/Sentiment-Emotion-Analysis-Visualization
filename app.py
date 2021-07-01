########################################################################################################################
#                                  > IMPORTS

import math
from math import pi
import numpy as np
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from bokeh.embed import components
from bokeh.layouts import column, gridplot, layout, row
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, Panel, Tabs, LinearColorMapper
from bokeh.models.tickers import SingleIntervalTicker
from bokeh.models.ranges import Range1d
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, cumsum
from bokeh.palettes import Bokeh5, Bokeh6, Bokeh8, Blues256

from PIL import Image
import base64
import io
import os

from flask import Flask, render_template, request

from retrieve_data import get_language_count, get_sentiment_count, get_emotions_count, get_frequency, get_tokenized_text

########################################################################################################################
#                               > CONSTANT VALUES

palette = Bokeh6

chart_font = 'Helvetica'
chart_title_font_size = '16pt'
chart_title_alignment = 'center'
axis_label_size = '14pt'
axis_ticks_size = '12pt'
default_padding = 30
chart_inner_left_padding = 0.015
chart_font_style_title = 'bold italic'

########################################################################################################################
#                             > HELPER FUNCTIONS

def palette_generator(length, palette):
    int_div = length // len(palette)
    remainder = length % len(palette)
    return (palette * int_div) + palette[:remainder]


def plot_styler(p):
    p.title.text_font_size = chart_title_font_size
    p.title.text_font  = chart_font
    p.title.align = chart_title_alignment
    p.title.text_font_style = chart_font_style_title
    p.y_range.start = 0
    p.x_range.range_padding = chart_inner_left_padding
    p.xaxis.axis_label_text_font = chart_font
    p.xaxis.major_label_text_font = chart_font
    p.xaxis.axis_label_standoff = default_padding
    p.xaxis.axis_label_text_font_size = axis_label_size
    p.xaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_text_font = chart_font
    p.yaxis.major_label_text_font = chart_font
    p.yaxis.axis_label_text_font_size = axis_label_size
    p.yaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_standoff = default_padding
    p.toolbar.logo = None
    p.toolbar_location = None


def redraw():

    # Frequency Line Graph
    eng_df = get_frequency('english')
    chi_df = get_frequency('chinese')
    mal_df = get_frequency('malay')
    frequency_line_graph = plot_frequency_line_graph(eng_df, chi_df, mal_df)

    # Test
    lang = pd.read_csv('data/frequency.csv')
    test_frequency_line_graph = test_plot_frequency_line_graph(lang, lang, lang)

    lang = pd.read_csv('data/sentiment.csv')
    sentiment_line_graph = plot_sentiment_line_graph(lang, lang, lang, lang)

    # Word Cloud
    eng_text, chi_text, mal_text = get_tokenized_text()
    img_data_eng = plot_each_word_cloud(eng_text)
    img_data_chi = plot_each_word_cloud(chi_text)
    img_data_mal = plot_each_word_cloud(mal_text)

    # lang1 = pd.read_csv('data/words.csv')
    #ngram_frequency_bar_chart = plot_ngram_frequency_bar_chart(lang1, lang1, lang1)

    # Language Pie Chart
    eng_count, chi_count, mal_count = get_language_count()
    language_pie_chart = plot_language_pie_chart(eng_count, chi_count, mal_count)

    # Sentiment Pie Chart
    eng_pos_count, eng_neg_count, chi_pos_count, chi_neg_count, mal_pos_count, mal_neg_count = get_sentiment_count()
    sentiment_pie_chart = plot_sentiment_pie_chart(eng_pos_count, eng_neg_count, chi_pos_count, chi_neg_count, mal_pos_count, mal_neg_count)

    # Emotions Frequency Bar Chart
    eng_emodf, chi_emodf, mal_emodf = get_emotions_count()
    emotion_frequency_bar_chart = plot_emotion_frequency_bar_chart(eng_emodf, chi_emodf, mal_emodf)

    lang2 = pd.read_csv('data/day_sentiment.csv')
    sentiment_by_day_bar_chart = plot_sentiment_by_day_bar_chart(lang2, lang2, lang2, lang2)

    emotions_day = pd.read_csv('data/day_emotions.csv')
    emotion_over_time_bar_chart = plot_emotion_over_time_bar_chart(emotions_day, emotions_day, emotions_day, emotions_day)

    return (
        frequency_line_graph,
        test_frequency_line_graph,
        sentiment_line_graph,
        img_data_eng, img_data_chi, img_data_mal,
        #ngram_frequency_bar_chart,
        language_pie_chart,
        sentiment_pie_chart,
        emotion_frequency_bar_chart,
        sentiment_by_day_bar_chart,
        emotion_over_time_bar_chart
    )

########################################################################################################################
#                               > MAIN ROUTE

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chart():

    frequency_line_graph, test_frequency_line_graph, sentiment_line_graph, img_data_eng, img_data_chi, img_data_mal, language_pie_chart, sentiment_pie_chart, emotion_frequency_bar_chart, sentiment_by_day_bar_chart, emotion_over_time_bar_chart = redraw()
    
    script_frequency_line_graph, div_frequency_line_graph = components(frequency_line_graph)
    script_test_frequency_line_graph, div_test_frequency_line_graph = components(test_frequency_line_graph)
    script_sentiment_line_graph, div_sentiment_line_graph = components(sentiment_line_graph)
    # script_ngram_frequency_bar_chart, div_ngram_frequency_bar_chart = components(ngram_frequency_bar_chart)
    script_language_pie_chart, div_language_pie_chart = components(language_pie_chart)
    script_sentiment_pie_chart, div_sentiment_pie_chart = components(sentiment_pie_chart)
    script_emotion_frequency_bar_chart, div_emotion_frequency_bar_chart = components(emotion_frequency_bar_chart)
    script_sentiment_by_day_bar_chart, div_sentiment_by_day_bar_chart = components(sentiment_by_day_bar_chart)
    script_emotion_over_time_bar_chart, div_emotion_over_time_bar_chart = components(emotion_over_time_bar_chart)

    return render_template(
        'index.html',
        div_frequency_line_graph=div_frequency_line_graph,
        script_frequency_line_graph=script_frequency_line_graph,
        div_test_frequency_line_graph=div_test_frequency_line_graph,
        script_test_frequency_line_graph=script_test_frequency_line_graph,
        div_sentiment_line_graph=div_sentiment_line_graph,
        script_sentiment_line_graph=script_sentiment_line_graph,
        img_data_eng=img_data_eng,
        img_data_chi=img_data_chi, 
        img_data_mal=img_data_mal, 
        #div_ngram_frequency_bar_chart=div_ngram_frequency_bar_chart,
        #script_ngram_frequency_bar_chart=script_ngram_frequency_bar_chart,
        div_language_pie_chart=div_language_pie_chart,
        script_language_pie_chart=script_language_pie_chart,
        div_sentiment_pie_chart=div_sentiment_pie_chart,
        script_sentiment_pie_chart=script_sentiment_pie_chart,
        div_emotion_frequency_bar_chart=div_emotion_frequency_bar_chart,
        script_emotion_frequency_bar_chart=script_emotion_frequency_bar_chart,
        div_sentiment_by_day_bar_chart=div_sentiment_by_day_bar_chart,
        script_sentiment_by_day_bar_chart=script_sentiment_by_day_bar_chart,
        div_emotion_over_time_bar_chart=div_emotion_over_time_bar_chart,
        script_emotion_over_time_bar_chart=script_emotion_over_time_bar_chart
    )

########################################################################################################################
#                        > CHART GENERATION FUNCTIONS

def test_plot_each_frequency_line_graph(dataset, cpalette=None):

    p = figure(plot_width=800, plot_height=450, x_axis_type="datetime")
    p.left[0].formatter.use_scientific = False
    p.title.text = 'Click on legend entries to hide the corresponding lines'

    data = dataset

    vdate = pd.to_datetime(data['date'])

    for name, color in zip(['ntweets', 'nreplies', 'nlikes', 'nretweets', 'nvideos'], Bokeh5):
        
        p.line(x=vdate, y=data[name], line_width=3, color=color, alpha=0.8, legend_label=name)

        p.legend.location = "top_left"
        p.legend.click_policy="hide"

    return p

def test_plot_frequency_line_graph(lang1, lang2, lang3): 

    lang1 = lang1
    lang2 = lang2
    lang3 = lang3

    p1 = test_plot_each_frequency_line_graph(lang1)
    tab1 = Panel(child=p1, title="English")

    p2 = test_plot_each_frequency_line_graph(lang2)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = test_plot_each_frequency_line_graph(lang3)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab1, tab2, tab3])
  
    return all_tabs

def plot_each_frequency_line_graph(dataset, cpalette=None):

    p = figure(plot_width=800, plot_height=450, x_axis_type="datetime")
    p.left[0].formatter.use_scientific = False
    p.title.text = 'Click on legend entries to hide the corresponding lines'

    data = dataset.sort_values(by=b'time_dimension:date')

    vdate = pd.to_datetime(data[b'time_dimension:date'])
    #vdate = data[b'time_dimension:date']

    for name, color in zip([b'count:nlikes', b'count:nreplies', b'count:nretweets', b'count:ntweets', b'count:videos'], Bokeh5):
        
        p.line(x=vdate, y=data[name], line_width=3, color=color, alpha=0.8, legend_label=name.decode('UTF-8'))

        p.legend.location = "top_left"
        p.legend.click_policy="hide"

    return p

def plot_frequency_line_graph(eng_df, chi_df, mal_df): 

    eng_df = eng_df
    chi_df = chi_df
    mal_df = mal_df
    
    # p = plot_each_frequency_line_graph(lang)
    # tab0 = Panel(child=p, title="All")

    p1 = plot_each_frequency_line_graph(eng_df)
    tab1 = Panel(child=p1, title="English")

    p2 = plot_each_frequency_line_graph(chi_df)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = plot_each_frequency_line_graph(mal_df)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab1, tab2, tab3])
  
    return all_tabs

def plot_each_sentiment_line_graph(dataset, cpalette=None):

    p = figure(plot_width=800, plot_height=450, x_axis_type="datetime")
    p.left[0].formatter.use_scientific = False
    p.title.text = 'Click on legend entries to hide the corresponding lines'

    data = dataset
    
    cpalette = ['#FC766AFF', '#5B84B1FF']

    vdate = pd.to_datetime(data['date'])

    for name, color in zip(['positive','negative'], cpalette):
        
        p.line(x=vdate, y=data[name], line_width=3, color=color, alpha=0.8, legend_label=name)

        p.legend.location = "top_left"
        p.legend.click_policy="hide"

    return p
    
def plot_sentiment_line_graph(lang, lang1, lang2, lang3): 

    lang = lang
    lang1 = lang
    lang2 = lang
    lang3 = lang
    
    p = plot_each_sentiment_line_graph(lang)
    tab0 = Panel(child=p, title="All")

    p1 = plot_each_sentiment_line_graph(lang1)
    tab1 = Panel(child=p1, title="English")

    p2 = plot_each_sentiment_line_graph(lang2)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = plot_each_sentiment_line_graph(lang3)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab0, tab1, tab2, tab3])
  
    return all_tabs

def plot_each_word_cloud(text):

    text=text

    font_path = 'static/font_style/AaXinHuaShuangJianTi.ttf'

    #plt.figure(figsize=(5, 4))
    wordcloud = WordCloud(font_path=font_path, max_font_size=120, max_words=100, background_color="white", width=800, height=500).generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    img_data = save_figure(plt)

    return img_data

def save_figure(plot):

    plt.savefig('static/images/word_cloud.png')
    img = Image.open("static/images/word_cloud.png") 
    data = io.BytesIO()
    img.save(data, "PNG") 
    encoded_img = base64.b64encode(data.getvalue())
    decoded_img = encoded_img.decode('utf-8')
    img_data = f"data:image/png;base64,{decoded_img}"
    #os.remove('static/images/word_cloud.png')

    return img_data

# def plot_each_language_word_cloud():

#     positive=positive
#     negative=negative

#     img_data1 = plot_each_word_cloud(positive)
#     img_data2 = plot_each_word_cloud(negative)

#     return img_data1, img_data2

# def plot_each_ngram_frequency_bar_chart(dataset): #number of words to show

#     data = dataset

#     y = data['words']
#     right = data['frequency']

#     sorted_y = sorted(y, key=lambda x: right[list(y).index(x)])

#     source = ColumnDataSource(data={
#         'words': data['words'],
#         'frequency': data['frequency']
#     })
      
#     p = figure(y_range=sorted_y, title = "English Unigram Frequency Ranking", tools="hover", tooltips="@words: @frequency",
#                plot_width=500, plot_height=600)

#     p.hbar(y='words',
#            right = 'frequency',
#            height = 0.5,
#            source=source,
#            fill_color=factor_cmap('words', palette=palette_generator(len(source.data['words']), palette),
#                                   factors=source.data['words']))

#     return p

# def plot_ngram_frequency_bar_chart(lang1, lang2, lang3):

#     lang1 = lang1
#     lang2 = lang2
#     lang3 = lang3

#     p1 = plot_each_ngram_frequency_bar_chart(lang1)
#     tab1 = Panel(child=p1, title="English")

#     p2 = plot_each_ngram_frequency_bar_chart(lang2)
#     tab2 = Panel(child=p2, title="Chinese")

#     p3 = plot_each_ngram_frequency_bar_chart(lang3)
#     tab3 = Panel(child=p3, title="Malay")

#     all_tabs = Tabs(tabs=[tab1, tab2, tab3])
  
#     return all_tabs

def plot_language_pie_chart(eng, chi, mal):

    cpalette = ['#2EB5D0', '#FFDF3D', '#2BAE66FF']

    eng = eng
    chi = chi
    mal = mal

    total = eng+chi+mal

    lang_count = [eng, chi, mal]

    x = {
        'English': eng/total*100, 
        'Chinese': chi/total*100,
        'Malay': mal/total*100
    }

    tooltips = [
        ('Language', '@language'),
        ('Count', '@count'),
        ('Percentage', '@value%')
    ]

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'language'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['count'] = lang_count

    p = figure(plot_height=350, plot_width=500, title="",
               tools="hover", tooltips=tooltips, x_range=(-0.5, 1.0)) 

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color=factor_cmap('language', palette=palette_generator(3, cpalette),
                                      factors=data['language']), legend_field='language', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    return p

def plot_each_sentiment_pie_chart(pos, neg):
    
    cpalette = ['#FC766AFF', '#5B84B1FF']

    pos = pos
    neg = neg

    total = pos+neg

    sentiment_count = [pos, neg]

    x = {
        'Positive': pos/total*100, 
        'Negative': neg/total*100
    }

    tooltips = [
        ('Sentiment', '@sentiment'),
        ('Count', '@count'),
        ('Percentage', '@value%')
    ]

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'sentiment'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['count'] = sentiment_count

    p = figure(plot_height=350, plot_width=500, title="",
               tools="hover", tooltips=tooltips, x_range=(-0.5, 1.0)) 

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color=factor_cmap('sentiment', palette=palette_generator(2, cpalette),
                                      factors=data['sentiment']), legend_field='sentiment', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    return p

def plot_sentiment_pie_chart(eng_pos_count, eng_neg_count, chi_pos_count, chi_neg_count, mal_pos_count, mal_neg_count):
    
    eng_pos_count = eng_pos_count
    eng_neg_count = eng_neg_count
    chi_pos_count = chi_pos_count
    chi_neg_count = chi_neg_count
    mal_pos_count = mal_pos_count
    mal_neg_count =  mal_neg_count
    total_pos_count = eng_pos_count + chi_pos_count + mal_pos_count
    total_neg_count = eng_neg_count + chi_neg_count + mal_neg_count
    
    p = plot_each_sentiment_pie_chart(total_pos_count, total_neg_count)
    tab0 = Panel(child=p, title="All")

    p1 = plot_each_sentiment_pie_chart(eng_pos_count, eng_neg_count)
    tab1 = Panel(child=p1, title="English")

    p2 = plot_each_sentiment_pie_chart(chi_pos_count, chi_neg_count)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = plot_each_sentiment_pie_chart(mal_pos_count, mal_neg_count)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab0, tab1, tab2, tab3])
  
    return(all_tabs)

def plot_each_emotion_frequency_bar_chart(dataset):

    palette = Bokeh5
    
    data = dataset
    
    x = data['emotion']
    top = data['frequency']

    #sorted_x = sorted(x, key=lambda y: top[[list(x).index(y)]])

    source = ColumnDataSource(data={
             'emotion': data['emotion'],
             'frequency': data['frequency']
    })

    p = figure(x_range=list(x), title = "", tools="hover", tooltips="@emotion: @frequency",
               plot_width=600, plot_height=400)

    p.vbar(x = 'emotion',
           top = 'frequency',
           width = 0.7,
           source=source,
           fill_color=factor_cmap('emotion', palette=palette_generator(len(source.data['emotion']), palette), factors=source.data['emotion']))
    
    return p

def plot_emotion_frequency_bar_chart(eng, chi, mal):
    
    eng = eng
    chi = chi
    mal = mal
    
    # p = plot_each_emotion_frequency_bar_chart(lang)
    # tab0 = Panel(child=p, title="All")

    p1 = plot_each_emotion_frequency_bar_chart(eng)
    tab1 = Panel(child=p1, title="English")

    p2 = plot_each_emotion_frequency_bar_chart(chi)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = plot_each_emotion_frequency_bar_chart(mal)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab1, tab2, tab3])
  
    return all_tabs

def plot_each_sentiment_by_day_bar_chart(dataset):
    
    colors = ["#e84d60", "#718dbf"]

    data = dataset

    data['day'].replace({1: "Monday", 2: "Tuesday", 3: "Wednesday", 
                             4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}, inplace=True)

    day = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    y = ['positive','negative']

    data_source = {'day' : data['day'],
                   'positive'   : data['positive'],
                   'negative'   : data['negative'],
                   'pos_pct'    : data['pos_pct'],
                   'neg_pct'    : data['neg_pct']}

    tooltips = [
        ('Day', '@day'),
        ('Positive', '@pos_pct%'),
        ('Negative', '@neg_pct%')
    ]

    p = figure(x_range=day, plot_height=400, title="", tools="hover", tooltips=tooltips)

    p.vbar_stack(y, x='day', width=0.7, color=colors, source=data_source,
                 legend_label=['positive','negative'])

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "vertical"

    return p

def plot_sentiment_by_day_bar_chart(lang, lang1, lang2, lang3):
    
    lang = lang
    lang1 = lang1
    lang2 = lang2
    lang3 = lang3
    
    p = plot_each_sentiment_by_day_bar_chart(lang)
    tab0 = Panel(child=p, title="All")

    p1 = plot_each_sentiment_by_day_bar_chart(lang1)
    tab1 = Panel(child=p1, title="English")

    p2 = plot_each_sentiment_by_day_bar_chart(lang2)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = plot_each_sentiment_by_day_bar_chart(lang3)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab0, tab1, tab2, tab3])
  
    return all_tabs

def plot_each_emotion_over_time_bar_chart(dataset, emotion):
    
    palette=Blues256
    
    data = dataset
    
    x = data['date']
    y = data[emotion]
    adj_y = np.array(y)/2

    data_source = {'day' : x,
                   'frequency': y,
                   'adj_f': adj_y}

    colormapper = LinearColorMapper(palette=palette, low=max(y), high=min(y))

    p = figure(x_range=list(x), plot_width=600, plot_height=400, tools="hover", tooltips="@day: @frequency")

    # add bar renderer
    p.rect(x='day', y='adj_f', width=0.6, height='frequency', source=data_source,
               fill_color={'field': 'frequency', 'transform': colormapper})

    # add a line renderer
    p.line(x, y, line_width=2)

    # Setting the y  axis range   
    p.y_range = Range1d(0, max(y)*1.1)

    return p

def plot_each_language_emotion_over_time_bar_chart(dataset):
    
    data = dataset
    
    p = plot_each_emotion_over_time_bar_chart(data, 'anger')
    tab1 = Panel(child=p, title="Anger")

    p = plot_each_emotion_over_time_bar_chart(data, 'anticipation')
    tab2 = Panel(child=p, title="Anticipation")
    
    p = plot_each_emotion_over_time_bar_chart(data, 'disgust')
    tab3 = Panel(child=p, title="Disgust")
    
    p = plot_each_emotion_over_time_bar_chart(data, 'fear')
    tab4 = Panel(child=p, title="Fear")
    
    p = plot_each_emotion_over_time_bar_chart(data, 'joy')
    tab5 = Panel(child=p, title="Joy")

    p = plot_each_emotion_over_time_bar_chart(data, 'sadness')
    tab6 = Panel(child=p, title="Sadness")
    
    p = plot_each_emotion_over_time_bar_chart(data, 'surprise')
    tab7 = Panel(child=p, title="Surprise")
    
    p = plot_each_emotion_over_time_bar_chart(data, 'trust')
    tab8 = Panel(child=p, title="Trust")

    all_tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8])
  
    return all_tabs

def plot_emotion_over_time_bar_chart(lang, lang1, lang2, lang3):
    
    lang=lang
    lang1=lang1
    lang2=lang2
    lang3=lang3
    
    p = plot_each_language_emotion_over_time_bar_chart(lang)
    tab0 = Panel(child=p, title="All")

    p1 = plot_each_language_emotion_over_time_bar_chart(lang1)
    tab1 = Panel(child=p1, title="English")

    p2 = plot_each_language_emotion_over_time_bar_chart(lang2)
    tab2 = Panel(child=p2, title="Chinese")

    p3 = plot_each_language_emotion_over_time_bar_chart(lang3)
    tab3 = Panel(child=p3, title="Malay")

    all_tabs = Tabs(tabs=[tab0, tab1, tab2, tab3])
  
    return all_tabs

if __name__ == '__main__':
    app.run(host="10.123.30.4", debug=True)


