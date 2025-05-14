import matplotlib.pyplot as plt

def make_pie(top_ten, title, legend_title, file_name):
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


def get_genre_counts(df):
    # Divide the "listed_in" column into multiple rows with each genre
    df.loc[:, "listed_in"] = df["listed_in"].str.split(",")
    df_exploded = df.explode("listed_in")
    df_exploded["listed_in"] = df_exploded["listed_in"].str.strip() 
    
    # Count the number of ocurrences of each genre
    df_genre_counts = df_exploded['listed_in'].value_counts()
    
    return df_genre_counts