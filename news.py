import streamlit as st
import requests, sys, time
import datetime as dt

# Put your API Key here.
APIkey = 'REDACTED'

time = dt.datetime.today().strftime("%I:%M:%S%p, %d-%m-%Y")
st.title(f"""Top news headlines at the moment.""")
st.info(f"""This is a simple app that shows you the top news headlines from various sources.\n
 _Last refresh was at {time}_""")
st.write("\n" + "---" + "\n")

st.sidebar.title("News options")
category = st.sidebar.selectbox("Select a category", ["All", "business", "entertainment", "general", "health", "science", "sports", "technology"])
query = st.sidebar.text_input("Enter a search query")
nNews = st.sidebar.slider("Number of news to show", 1, 20)
button = st.sidebar.button("Show news")

params = {
    'country':'',  # This is the country you want to get news from (us, uk, fr, de, it, etc.)
    'category':'', # This is the category you want to get news from (business, entertainment, general, health, science, sports, technology)
    'q':'',   # This is the search term you want to search for [Keyword] (e.g. coronavirus, covid, covid-19, Ukraine, etc.)
    'language':'en', # This is the language you want to get news in (en, ar, fr, de, it, etc.)
    'pageSize':'10', # This is the number of news you want to get (max 100)
    'page':'1', # This is the page you want to get (max 100)
    'sortBy':'top', # This is the sort order you want to get news in (top, latest, popular)
}


### CORE
# Visualize the news function

url = 'https://newsapi.org/v2/top-headlines?'

if button:
    params = {
        'country': '',
        'category': category if category != "All" else '',
        'q': query,
        'language': 'en',
        'pageSize': str(nNews),
        'page':'1',
        'sortBy':'top'
    }

for key, value in params.items():
    if value != '':
        url += key + '=' + value + '&'

url += 'apiKey=' + APIkey

response = requests.get(url)
data = response.json()

if data['status'] == 'error':
    print('Error: ' + data['message'])
    sys.exit(1)

nResults = data['totalResults']
results = data['articles']

print("Found " + str(nResults) + " results")

# Visualize the news function

def show_news(results):
    for new in results:

        try:
            st.image(new['urlToImage'])
        except Exception:
            st.write("No image found")
        st.write("### " + new['title'])
        st.write(new['description'])
        st.write(new['url'])
        st.write(f"\nBy {new['author']} - {new['source']['name']} at {new['publishedAt']}\n")
        st.write("\n" + "---" + "\n")

show_news(results)
st.success(f"""Found {nResults} results""")
