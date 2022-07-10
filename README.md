<p align="center">
  <h2 align="center">Sentiment and Emotion Analysis Visualization</h2>

  <p align="center">
    This project involves crawling English, Malay and Chinese tweets related to the topic of “Online Learning” from Twitter, cleaning the crawled data, performing sentiment and emotion analysis and lastly, visualizing the result.
  </p>
</p>

<details open="open">
  <summary><h3 style="display: inline-block">Table of Contents</h3></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#demo">Demo</a>
    </li>
    <li>
      <a href="#setup">Installation</a>
    </li>
    <li>
      <a href="#run">Running the Project</a>
    </li>
  </ol>
</details>


<h3 id="about-the-project">About The Project</h3>

Due to the COVID-19 pandemic, many countries including Malaysia are under lockdown to contain the spread of the virus. 
As a result, teaching and learning activities are shifted online. As students, we are interested to find out what people think and feel about online learning.
Therefore, this project is carried out to analyse the sentiments and emotions towards online learning on Twitter.
This project was done in a group of 4 and I was responsible for visualizing the result of the sentiment and emotion analysis.

<b>This project was built with:</b>
<br>
* [HappyBase](https://happybase.readthedocs.io/en/latest/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Bootstrap](https://getbootstrap.com/)
* [Bokeh](https://docs.bokeh.org/en/latest/index.html)
* [Matplotlib](https://matplotlib.org/)
* [Wordcloud](https://amueller.github.io/word_cloud/)


<h3 id="demo">Demo</h3>

<div align="center">
  <p style="text-align:center;">Language Proportion Pie Chart</p>
  <img src="screenshots/language_proportion_pie_chart.PNG" alt="Language Proportion Pie Chart">
</div><br>
<div align="center">
  <p style="text-align:center;">Sentiment Proportion Pie Chart</p>
  <img src="screenshots/sentiment_proportion_pie_chart.PNG" alt="Sentiment Proportion Pie Chart">
</div><br>
<div align="center">
  <p style="text-align:center;">Frequency over Time Line Graph</p>
  <img src="screenshots/frequency_over_time_line_graph.png" alt="Frequency over Time Line Graph">
</div><br><br>
<div align="center">
  <p style="text-align:center;">English Word Cloud</p>
  <img src="screenshots/english_word_cloud.png" alt="English Word Cloud">
</div><br>
<div align="center">
  <p style="text-align:center;">Sentiment by Day Stacked Bar Chart</p>
  <img src="screenshots/sentiment_by_day_stacked_bar_chart.PNG" alt="Sentiment by Day Stacked Bar Chart">
</div><br>
<div align="center">
  <p style="text-align:center;">Sentiment over Time Line Graph</p>
  <img src="screenshots/sentiment_over_time_line_graph.png" alt="Sentiment over Time Line Graph">
</div><br>
<div align="center">
  <p style="text-align:center;">Emotion Frequency Bar Chart</p>
  <img src="screenshots/emotion_frequency_bar_chart.PNG" alt="Emotion Frequency Bar Chart">
</div><br>
<div align="center">
  <p style="text-align:center;">Emotion over Time Line Bar Chart</p>
  <img src="screenshots/emotion_over_time_line_bar_chart.PNG" alt="Emotion over Time Line Bar Chart">
</div>

<h3 id="setup">Installation</h3>

1. Download the Visualization folder.
2. At your Anaconda Prompt, create a virtual environment and run the following command: <br>
   ```sh
   pip install -r requirements.txt
   ```

<h3 id="run">Running the Project</h3>

1. Open the app.py file, at the last line of the file, replace the host ip address with your own ip address.
2. At your Anaconda Prompt, activate your virtual environment and change the directory to the project folder.
3. Run the following commands:
   ```sh
   set FLASK_APP=app.py
   set FLASK_ENV=development
   flask run
   ```
4. Access the webpage at localhost:5000 in your browser.

