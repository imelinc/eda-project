import matplotlib.pyplot as plt

def fill_data(df):
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

def make_pie(top_ten, title, legend_title, file_name):
    """_summary_

       Args:
           top_ten (_type_): _description_
           title (_type_): _description_
           legend_title (_type_): _description_
           file_name (_type_): _description_
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


def get_counts_of_certain_column(df, column):
    # Divide the "listed_in" column into multiple rows with each genre
    df.loc[:, column] = df[column].str.split(",")
    df_exploded = df.explode(column)
    df_exploded[column] = df_exploded[column].str.strip() 
    
    # Count the number of ocurrences of each genre
    df_genre_counts = df_exploded[column].value_counts()
    
    return df_genre_counts

def make_bar_plot(file, plot_title, xlabel, ylabel, ax, kind):
    file.plot(kind=kind , ax=ax, color="#ad1d3c")
    if kind == "barh":
       ax.invert_yaxis()
       ax.grid(True, axis='x', color='white', alpha=0.4)
    else:
       ax.grid(True, axis='y', color='white', alpha=0.4)
    ax.set_facecolor("#15130d")
    ax.set_title(plot_title, color = "white")
    ax.set_xlabel(xlabel, color = "white")
    ax.set_ylabel(ylabel, color = "white")
    ax.tick_params(colors = "white")
    for spine in ax.spines.values():
        spine.set_color("white")
