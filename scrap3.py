from bs4 import BeautifulSoup
import requests
import re

# Function to get the IMDb data
def get_imdb_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# Function to get the highest rated Sci-Fi movie's movieId
def get_highest_rated_scifi_movie_id(url):
    soup = get_imdb_data(url)
    
    movies = soup.select('td.titleColumn')
    ratings = [float(b.attrs.get('data-value')) for b in soup.select('td.posterColumn span[name=ir]')]
    genres = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

    # Create a list of dictionaries containing movie information
    movie_data = []
    for index in range(len(movies)):
        movie_string = movies[index].get_text()
        movie_title = movie_string[len(str(index)) + 1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie_string[:len(str(index)) - (len(movie_string))]
        data = {
            "place": place,
            "movie_title": movie_title,
            "rating": ratings[index],
            "year": year,
            "genre": genres[index]
        }
        movie_data.append(data)

    # Filter Sci-Fi movies
    scifi_movies = [movie for movie in movie_data if 'Sci-Fi' in movie['genre']]

    # Find the highest rated Sci-Fi movie
    highest_rated_scifi_movie = max(scifi_movies, key=lambda x: x['rating'])

    return highest_rated_scifi_movie['place']

# IMDb URL for top 250 movies
url_top_250 = 'http://www.imdb.com/chart/top'

# Get the movieId of the highest rated Sci-Fi movie
highest_rated_scifi_movie_id = get_highest_rated_scifi_movie_id(url_top_250)

print(f"The movieId of the highest rated Sci-Fi movie is: {highest_rated_scifi_movie_id}")
