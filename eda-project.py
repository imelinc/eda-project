import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import side_functions as sf

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
    
    # Get the number of ocurrences of each genre
    movies_genre_counts = sf.get_counts_of_certain_column(movies_df, "listed_in")
    tv_shows_genre_counts = sf.get_counts_of_certain_column(tv_shows_df, "listed_in")
    
    # Plotting the data
    fig, (ax1, ax2) = plt.subplots(nrows = 1,
                                   ncols = 2,
                                   figsize = (20, 7),
                                   facecolor = "#000000")
    
    # Plotting for movies
    sf.make_bar_plot(movies_genre_counts,"Distribution of Genres in Movies", "Genres", "Number of Movies", ax1, "bar")
    
    # Plotting for tv shows
    sf.make_bar_plot(tv_shows_genre_counts, "Distribution of Genres in TV Shows", "Genres", "Number of TV Shows", ax2, "bar")

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
    sf.make_bar_plot(num_movies ,"Number of Movies Added on Certain Years", "Number of Additions", "Year", ax1, "barh" )
    
    # Plot for tv shows
    sf.make_bar_plot(num_tv_shows, "Number of TV Shows Added on Certain Years", "Number of Additions", "Year", ax2, "barh")
    
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
    movies_top_ten = sf.get_counts_of_certain_column(movies_df, "country")
    movies_top_ten = movies_top_ten[movies_top_ten.index != "Unknown"].head(10)
    
    # Getting every country separated (TV SHOWS)
    tv_shows_top_ten = sf.get_counts_of_certain_column(tv_shows_df, "country")
    tv_shows_top_ten = tv_shows_top_ten[tv_shows_top_ten.index != "Unknown"].head(10)
    
    sf.make_pie(movies_top_ten, "Top 10 Countries by Movies", "Countries", "pie_chart_top_ten_countries_(MOVIES)")
    sf.make_pie(tv_shows_top_ten, "Top 10 Countries by TV Shows", "Country", "pie_chart_top_ten_countries_(TVSHOWS)")
    
    return movies_top_ten, tv_shows_top_ten
    
def domination_of_genres(df, movies_top_ten, tv_shows_top_ten):
    """
    this function takes the top 3 countries and makes a tree map about
    which genres are most common on that specific country

    Args:
        df (pandas.DataFrame): dataset
        movies_top_ten (pandas.Series): Series with the ten countries with the most appereances on movies
        tv_shows_top_ten (pandas.Series): Series with the ten countries with the most appereances on tv shows
    """
    
    # Get the top three countries
    movies_top_three = movies_top_ten.head(3).index
    tv_shows_top_three = tv_shows_top_ten.head(3).index
    
    # Preprocessing the dataframe
    df = df.copy()
    df['country'] = df['country'].str.split(', ')
    df['listed_in'] = df['listed_in'].str.split(', ')
    df = df.explode('country').explode('listed_in')
    df['country'] = df['country'].str.strip()
    df['listed_in'] = df['listed_in'].str.strip()
    
    # Filter by the top three countries in movies
    movies_df = df[(df["type"] == "Movie") & (df["country"].isin(movies_top_three))]
    # Group by countries and genres
    movies_grouped = movies_df.groupby(["country", "listed_in"]).size().reset_index(name="count")
    
    # Filter by the top three countries in tv shows
    tv_shows_df = df[(df["type"] == "Movie") & (df["country"].isin(tv_shows_top_three))]
    # Group by counries and genres
    tv_shows_grouped = tv_shows_df.groupby(["country", "listed_in"]).size().reset_index(name="count")
    
    # Plotting and customizating the treemaps
    fig_movies = sf.make_treemap(df.copy(), file = movies_grouped, path = ['country','listed_in'], values = 'count', title = 'Top 3 Countries - Genre Domination in Movies', color='country')
    fig_shows = sf.make_treemap(df.copy(), file = movies_grouped, path = ['country','listed_in'], values = 'count', title = 'Top 3 Countries - Genre Domination in Movies', color='country')
    
    fig_movies.write_image("figs/movies_treemap.png", scale = 3)
    fig_shows.write_image("figs/shows_treemap.png", scale = 3)
        
    
# Load the dataset
df = pd.read_csv("data/netflix_titles.csv")

# Fill the null data and store it in the same variable
df = sf.fill_data(df)

plot_genre_distribution(df)
plot_distribution_of_years(df)
movies_top_ten, tv_shows_top_ten = plot_countries_vs_genres(df)
domination_of_genres(df, movies_top_ten, tv_shows_top_ten)
