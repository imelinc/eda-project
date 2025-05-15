import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px 

def fill_data(df):
    """
    this function fills the missing values in the dataset with "Unknown"
    Args:
        df (pandas.DataFrame): dataset
    """
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['date_added'] = df['date_added'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unknown')
    df['duration'] = df['duration'].fillna('Unknown')
    
    return df

def make_pie(top_ten, title, legend_title, file_name):
    """
    This function generates a pie chart using the provided data series and applies custom
    styling.
    Args:
       top_ten (pandas.Series): A pandas Series containing the data to be plotted.
                                The index of the Series will be used as labels in the legend.
        title (str): The title to display above the pie chart.
        legend_title (str): The title to display in the chart legend.
        file_name (str): Name for the saved file (without extension).
                        The file will be saved as PNG in the 'figs' directory.
    
    """
    # colors to be used in the pie chart
    colors = ["#7F1A1A", "#A35E2D", "#625B7F", "#3F7F4A", "#4E4E4E", 
               "#947F4E", "#6C4A7F", "#377F79", "#9C3131", "#5A5A5A"]

    # Plot the top ten countries
    plt.figure(figsize=(12, 12), facecolor='#15130d')
    plt.pie(top_ten, labels=None, labeldistance=1.1, 
                colors=colors, wedgeprops={'edgecolor': 'black'}, autopct="%1.1f%%",
                textprops={"fontsize":12, "color":"white"})

    plt.gca().set_facecolor('#15130d')
    plt.title(title, color="white", fontsize=22)
    plt.legend(top_ten.index, title=legend_title, loc="upper right", bbox_to_anchor=(1.1, 1.1), 
           facecolor="black", edgecolor="white", title_fontsize=17, fontsize=14, 
           labelcolor="white")

    # Explicitly set the title color
    plt.setp(plt.gca().get_legend().get_title(), color='white')
    plt.savefig(f"figs/{file_name}.png", dpi = 800)

def expand_the_dataset(df, column):
    """
    This function expands the dataframe in multiple rows given a certain column
    Args:
        df (pandas.DataFrame): dataset
        column (str): name of the column that we want to expand

    Returns:
        pandas.DataFrame: dataframe correctly expanded
    """
    # Divide the column into multiple rows
    df.loc[:, column] = df[column].str.split(",")
    df_exploded = df.explode(column)
    df_exploded[column] = df_exploded[column].str.strip() 
    
    return df_exploded

def get_counts_of_certain_column(df, column):
    """
    This function count the amount of values that are on the dataframe given a certain column
    Args:
        df (pandas.DataFrame): dataset
        column (str): name of the column that we want to count values
    """
    
    new_df = expand_the_dataset(df, column)
    # Count the number of ocurrences of each genre
    df_genre_counts = new_df[column].value_counts()
    
    return df_genre_counts

def make_bar_plot(file, plot_title, xlabel, ylabel, ax, kind, need_custom_axes = False):
    if not need_custom_axes:
        file.plot(kind=kind , ax=ax, color="#7F1A1A", legend = False)
    else:
        file.plot(kind = kind, x = (file.columns.to_list())[0], y = (file.columns.to_list())[1], ax = ax, color = "#7F1A1A", legend = False)
    if kind == "barh":
       ax.invert_yaxis()
       ax.grid(True, axis='x', color='white', alpha=0.4)
    else:
       ax.grid(True, axis='y', color='white', alpha=0.4)
    ax.set_facecolor("#15130d")
    ax.set_title(plot_title, color = "white", fontsize = 20)
    ax.set_xlabel(xlabel, color = "white", fontsize = 12)
    ax.set_ylabel(ylabel, color = "white", fontsize = 12)
    ax.tick_params(colors = "white")
    for spine in ax.spines.values():
        spine.set_color("white")

def make_treemap(df, file, path, values, title, color):
    custom_colors = {
    "United States": "#7F1A1A",
    "India": "#A35E2D",
    "United Kingdom": "#625B7F",
    "Japan" : "#A35E2D"
    }

    # Add a column to map colors
    df["Color"] = df["country"].map(custom_colors)
    
    fig = px.treemap(
    file,
    path=path,
    values=values,
    title=title,
    color=color, 
    color_discrete_map=custom_colors
    )
    
    treemap_customization(fig)
    return fig
    

def treemap_customization(fig):
    fig.update_layout(
    font=dict(family="Arial", size=20, color="white"),
    paper_bgcolor="#15130d",
    plot_bgcolor="#15130d", 
    width=1300,
    height=1100
    )

    fig.update_traces(
        textfont_color="white",          
        textfont_size=16,
        marker=dict(
            line=dict(width=1, color="white")  
        )
    )

def rating_vs_genre_plot(iterator, data_file):
    # Plotting the data for movies
    fig, axes = plt.subplots(nrows = 1,
                            ncols = 3,
                            figsize = (30, 7),
                            facecolor = "#000000")
    
    axes = axes.flatten()
    
    for i, genre in enumerate(iterator):
        data_to_plot = pd.DataFrame(list(data_file[genre].items()), columns=["Rating", "Count"])
        make_bar_plot(data_to_plot, f"Rating Distribution for {genre}", "Ratings", "Count", axes[i], "bar", need_custom_axes = True)

