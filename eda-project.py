import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import side_functions as sf

def filling_data(df):
    """
    this function fills the missing values in the dataset with "Unknown"
    Args:
        df (_type_): dataset
    """
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['date_added'] = df['date_added'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unknown')
    df['duration'] = df['duration'].fillna('Unknown')
    
    return df

# Plot the distribution of the different types of genres
def plot_genre_distribution(df):
    """
    this function plots the distribution of different types of genres in the dataset
    1. By movies only
    2. By tv shows only
    Args:
        df (_type_): dataset
    """
    
    # Filter the DataFrame for movies only
    movies_df = df[df['type'] == 'Movie'].copy()
    # Filter the dataframe for tv shows only
    tv_shows_df = df[df['type'] == 'TV Show'].copy()
    
    # Divide the "listed_in" column into multiple rows with each genre
    movies_df.loc[:, "listed_in"] = movies_df["listed_in"].str.split(",")
    movies_exploded = movies_df.explode("listed_in")
    movies_exploded["listed_in"] = movies_exploded["listed_in"].str.strip() 
    
    # Divide the "listed_in" column into multiple rows with each genre
    tv_shows_df.loc[:, "listed_in"] = tv_shows_df["listed_in"].str.split(",")
    tv_shows_exploded = tv_shows_df.explode("listed_in")
    tv_shows_exploded["listed_in"] = tv_shows_exploded["listed_in"].str.strip() 
    
    # Count the number of ocurrences of each genre
    movies_genre_counts = movies_exploded['listed_in'].value_counts()
    tv_shows_genre_counts = tv_shows_exploded['listed_in'].value_counts()
    
    # Plotting the data
    fig, (ax1, ax2) = plt.subplots(nrows = 1,
                                   ncols = 2,
                                   figsize = (20, 7),
                                   facecolor = "#000000")
    
    # Plotting for movies
    movies_genre_counts.plot(kind="bar", ax=ax1, color="#ad1d3c")
    ax1.set_facecolor("#15130d")
    ax1.set_title("Distribution of Genres in Movies", color = "white")
    ax1.set_xlabel("Genres", color = "white")
    ax1.set_ylabel("Number of Movies", color = "white")
    ax1.tick_params(colors = "white")
    for spine in ax1.spines.values():
        spine.set_color("white")
    ax1.grid(True, axis='y', color='white', alpha=0.4)
    
    # Plotting for tv shows
    tv_shows_genre_counts.plot(kind="bar", ax=ax2, color="#ad1d3c")
    ax2.set_facecolor("#15130d")
    ax2.set_title("Distribution of Genres in TV Shows", color = "white")
    ax2.set_xlabel("Genres", color = "white")
    ax2.set_ylabel("Number of TV Shows", color = "white")
    ax2.tick_params(colors = "white")
    for spine in ax2.spines.values():
        spine.set_color("white")
    ax2.grid(True, axis='y', color='white', alpha=0.4)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2)
    plt.savefig("figs/genre_distribution.png", dpi = 800)

def plot_distribution_of_years(df):
    """
    this function plots the number of Movies or TV Shows that were uploaded on a certain year
    Args:
        df (_type_): dataframe
    """
    # Divide into movies and tv shows
    movies_df = df[df["type"] == "Movie"].copy()
    tv_shows_df = df[df["type"] == "TV Show"].copy()
    
    # Getting the years of addition of each movie
    movies_df["date_added"] = movies_df["date_added"].str.split(", ")
    year_movies = movies_df["date_added"].str[1]
    
    # Getting the years of addition of each tv show
    tv_shows_df["date_added"] = tv_shows_df["date_added"].str.split(", ")
    year_tv_shows = tv_shows_df["date_added"].str[1]
    
    # Now i get the number of occurrences of each year
    num_movies = year_movies.value_counts()
    num_tv_shows = year_tv_shows.value_counts()

    # Plotting the data
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,10), facecolor = "#000000")
    
    # Plot for movies
    num_movies.plot(kind="barh", ax=ax1, color="#ad1d3c")
    ax1.set_facecolor("#15130d")
    ax1.invert_yaxis()
    ax1.set_ylabel("Year", color="white")
    ax1.set_xlabel("Number of Additions", color="white")
    ax1.set_title("Number of Movies Added on Certain Years", color="white")
    ax1.tick_params(colors = "white")
    for spine in ax1.spines.values():
        spine.set_color("white")
    ax1.grid(True, axis='x', color='white', alpha=0.4)
    
    # Plot for tv shows
    num_tv_shows.plot(kind="barh", ax=ax2, color="#ad1d3c")
    ax2.set_facecolor("#15130d")
    ax2.invert_yaxis()
    ax2.set_ylabel("Year", color = "white")
    ax2.set_xlabel("Number of Additions", color = "white")
    ax2.set_title("Number of TV Shows Added on Certain Years", color = "white")
    ax2.tick_params(colors = "white")
    for spine in ax2.spines.values():
        spine.set_color("white")
    ax2.grid(True, axis='x', color='white', alpha=0.4)
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3)
    plt.savefig("figs/year_distribution.png", dpi = 800) 

def plot_countries_vs_genres(df):
    """
    this function plots the countries that dominate in certain genres
    1. In movies
    2. In TV Shows
    Args:
        df (_type_): dataset
    """
    # Divide into movies and tv shows
    movies_df = df[df["type"] == "Movie"].copy()
    tv_shows_df = df[df["type"] == "TV Show"].copy()
    
    # Getting every country separated (MOVIES)
    movies_df.loc[:, "country"] = movies_df["country"].str.split(",")
    movies_exploded = movies_df.explode("country")
    movies_exploded["country"] = movies_exploded["country"].str.strip()
    
    # Getting the top ten countries with the most occurrences for movies
    movies_top_ten = movies_exploded["country"].value_counts()
    # Delete the "Unknown" from the top ten
    movies_top_ten = movies_top_ten[movies_top_ten.index != "Unknown"].head(10)
    
    # Getting every country separated (TV SHOWS)
    tv_shows_df.loc[:, "country"] = tv_shows_df["country"].str.split(",")
    tv_shows_exploded = tv_shows_df.explode("country")
    tv_shows_exploded["country"] = tv_shows_exploded["country"].str.strip()
    
    # Getting the top ten countries with the most occurrences for tv shows
    tv_shows_top_ten = tv_shows_exploded["country"].value_counts()
    # Delete the "Unknown" from the top ten
    tv_shows_top_ten = tv_shows_top_ten[tv_shows_top_ten.index != "Unknown"].head(10)
    
    sf.make_pie(movies_top_ten, "Top 10 Countries by Movies", "Countries", "pie_chart_top_ten_countries_(MOVIES)")
    sf.make_pie(tv_shows_top_ten, "Top 10 Countries by TV Shows", "Country", "pie_chart_top_ten_countries_(TVSHOWS)")
    
    return movies_top_ten, tv_shows_top_ten
    
def domination_of_genres(df, movies_top_ten, tv_shows_top_ten):
    """
    this function takes the top 3 countries and makes a tree map about
    which genres are most common on that specific country

    Args:
        df (_type_): dataset
        movies_top_ten (_type_): dataframe with the ten countries with the most appereances on movies
        tv_shows_top_ten (_type_): dataframe with the ten countries with the most appereances on tv shows
    """
    
    # Get the top three countries
    movies_top_three = movies_top_ten.head(3).copy()
    tv_shows_top_three = tv_shows_top_ten.head(3).copy()
    
# Load the dataset
df = pd.read_csv("data/netflix_titles.csv")

# Fill the null data and store it in the same variable
df = filling_data(df)

plot_genre_distribution(df)
plot_distribution_of_years(df)
movies_top_ten, tv_shows_top_ten = plot_countries_vs_genres(df)
domination_of_genres(df, movies_top_ten, tv_shows_top_ten)
