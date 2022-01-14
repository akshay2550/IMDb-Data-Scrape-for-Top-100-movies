from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc'

movie_name = []
year = []
rating = []
time = []
votes = []
gross_revenue = []

response1 = requests.get(url)
response2 = requests.get(url+'&start=51&ref_=adv_nxt')

soup1 = BeautifulSoup(response1.content,"lxml")
soup2 = BeautifulSoup(response2.content,'lxml')

movie_data1 = soup1.find_all('div',attrs={'class':'lister-item mode-advanced'})
movie_data2 = soup2.find_all('div',attrs={'class':'lister-item mode-advanced'})

def fill_data(movie_data):
  for data in movie_data:
    movie_name.append(data.h3.a.text)
    year.append(data.find('span',attrs={'class':'lister-item-year'}).text.replace('(','').replace(')','').replace('I ',''))
    rating.append(data.find('div',attrs={'class':'ratings-imdb-rating'}).strong.text)
    time.append(data.find('span',attrs={'class':'runtime'}).text.replace(' min',''))

    value = data.find_all('span',attrs={'name':'nv'})
    votes.append(value[0].text)
    gross_revenue.append(value[1].text if len(value)>1 else 'Not Available')

fill_data(movie_data1)
fill_data(movie_data2)

movies = pd.DataFrame({'Name of Movie':movie_name,'Year of Release':year,'Rating':rating,'Runtime (in mins)':time,'Votes':votes,'Gross Collection':gross_revenue})

movies.to_csv('IMDb Top 100 Movies.csv')