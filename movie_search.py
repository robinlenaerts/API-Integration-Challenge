import requests
import json
from os import system, name
import time
from prettytable import PrettyTable

# Clear screen
def clear_screen():
    # For windows
    if name == 'nt':
        _ = system('cls')
    # For mac and linux, here os.name is 'posix'
    else:
        _ = system('clear')

# Exit with an error description
def exit_error(description):
    clear_screen()
    print("The following error occured: " + str(description))
    input("Enter to exit...")
    exit()

# Use API to search for movies based on user input
def search_movies(movie_title):
    # API url for searching movies
    url = "https://api.themoviedb.org/3/search/movie?query=" + movie_title

    # API headers with authentication
    headers = {
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json;charset=utf-8"
    }

    try:
        # Send get request to API
        response = requests.get(url, headers=headers)
        # If request fails, wait and try again for max 5 times
        retries = 0
        max_retriess = 5
        while response.status_code != 200 and retries <= max_retriess:
            retries += 1
            time.sleep(0.5)
            response = requests.get(url, headers=headers)
        # If the status code is still not 200 after 5 retries, exit with an error description
        if response.status_code !=  200:
            exit_error("Can't connect with API")
    except Exception as ex:
        exit_error(ex)

    return response.json()

# get all genres with the given genre ids
def get_genres(genre_ids):
    # API url for retrieving all genres
    url = "https://api.themoviedb.org/3/genre/movie/list"

    # API headers with authentication
    headers = {
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json;charset=utf-8"
    }

    try:
        # Send get request to API
        response = requests.get(url, headers=headers)
        # If request fails, wait and try again for max 5 times
        retries = 0
        max_retriess = 5
        while response.status_code != 200 and retries <= max_retriess:
            retries += 1
            time.sleep(0.5)
            response = requests.get(url, headers=headers)
        # If the status code is still not 200 after 5 retries, exit with an error description
        if response.status_code !=  200:
            exit_error("Can't connect with API")
    except Exception as ex:
        exit_error(ex)
    
    all_genres = response.json()["genres"]
    # Return all genre names matching the genre ids of the movie
    return [genre["name"] for genre in all_genres if genre["id"] in genre_ids]

# Get all necessary info of movies in the search result
def get_movie_info(movies):
    # Array to store all the necessary info and details the movies
    movie_info = []
    movie_details = []
    counter = 0
    # Create arrays with all information needed to display later
    for movie in movies["results"]:
        counter += 1
        movie_info.append([counter, (movie["original_title"] if "original_title" in movie else ""), (movie["release_date"] if "release_date" in movie else "")])
        movie_details.append([(movie["original_title"] if "original_title" in movie else ""), (movie["release_date"] if "release_date" in movie else ""), (movie["genre_ids"] if "genre_ids" in movie else ""), (movie["overview"] if "overview" in movie else ""), (movie["original_language"] if "original_language" in movie else ""), (movie["adult"] if "adult" in movie else ""), (movie["popularity"] if "popularity" in movie else ""), (movie["vote_average"] if "release_date" in movie else ""), (movie["vote_count"] if "vote_count" in movie else "")])
    return movie_info, movie_details

# Print info of found movies in a table format
def print_table(movie_info):
    clear_screen()

    print("Search results for '" + movie_search_title + "':")

    # Create a table
    movie_table = PrettyTable()
    movie_table.field_names = [str(len(movie_info)) + " Results", "Title", "Release date"]
    movie_table.add_rows(movie_info)

    print(movie_table)

# Print details of selected movie
def print_details(number):
    clear_screen()

    # Assign the selected movie to a variable
    selected_movie = movie_details[number]

    title ="Details for movie '" + selected_movie[0] + "':"
    print(title + "\n" + ("-" * len(title)))

    # Format text in lines
    overview = selected_movie[3]
    text_width = 60
    position = 0
    # Check if the text is long enough to put another newline character in the back
    while not len(overview) < position + text_width:
        position += text_width
        while True:
            # Search for space character to replace with a newline character
            if overview[position] == " ":
                overview = overview[:position] + "\n" + overview[position + 1:]
                break
            else:
                position -= 1
    
    print(overview)

    # Get all genre names and join them together in a string
    genres = ", ".join(get_genres(selected_movie[2]))

    # create a table
    movie_details_table = PrettyTable()
    movie_details_table.field_names = ["", "Details"]
    movie_details_table.add_row(["Title", selected_movie[0]])
    movie_details_table.add_row(["Release date", selected_movie[1]])
    movie_details_table.add_row(["Genres", genres])
    movie_details_table.add_row(["Original language", selected_movie[4]])
    movie_details_table.add_row(["Adult content", "Yes" if selected_movie[5] == "true" else "No"])
    movie_details_table.add_row(["Popularity", round(selected_movie[6])])
    movie_details_table.add_row(["Vote average", selected_movie[7]])
    movie_details_table.add_row(["Vote count", selected_movie[8]])

    print(movie_details_table)


banner = """  __  __            _                                _     
 |  \/  |          (_)                              | |    
 | \  / | _____   ___  ___   ___  ___  __ _ _ __ ___| |__  
 | |\/| |/ _ \ \ / / |/ _ \ / __|/ _ \/ _` | '__/ __| '_ \ 
 | |  | | (_) \ V /| |  __/ \__ \  __/ (_| | | | (__| | | |
 |_|  |_|\___/ \_/ |_|\___| |___/\___|\__,_|_|  \___|_| |_|"""

# Read Bearer Token from bearer_token.txt file
bearer_token = open("bearer_token.txt", "r").readline()
# Bearer Token in code
#bearer_token = "<bearer_token>"

clear_screen()
print(banner + "\n")
# Ask user for name of movie to search
movie_search_title = input("Movie title: ")

movies = search_movies(movie_search_title)
movie_info, movie_details = get_movie_info(movies)
print_table(movie_info)

# DEBUG: Get raw output from request
#print(json.dumps(movies, indent=4))

# While loop for user interaction with search results
exit_words = ["exit", "quit", "stop", "back"]
while True:
    choice = input("Give number to view details or type 'exit' to quit: ")
    if choice in exit_words:
        exit()
    elif choice.isdecimal() and 0 < int(choice) <= len (movie_info):
        print_details(int(choice) - 1)
        # While loop for user interaction with movie details
        go_back = False
        while not go_back:
            choice = input("Type 'back' to go back: ")
            if choice in exit_words:
                go_back = True
                print_table(movie_info)
            else:
                print("Bad input...")
    else:
        print("Bad input...")
