
import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from madkudu import (
    genre_group,
    year_metascore_genre,
    director_group,
    dramadesc_freq,
    dramarev_freq,
    comedydesc_freq,
    comedyrev_freq,
    no_of_movies,
    total_mins,
    first_movie,
    first_year,
    last_movie,
    last_year,
    highest_metascore_movie,
    highest_rating_movie
)

st.set_page_config(
    page_title="Nicolas Cage Movie Analysis",  # Title of the app
    page_icon="🎬",  # Icon of the app
    layout="wide",  # Use wide layout for larger content
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar
)

st.title("App Mission: Crafting Nicolas Cage's Next Hit Movie")
st.write ("We are on a mission to create the ultimate movie for Nicolas Cage. In an era where data drives entertainment success—like Netflix using analytics to create viewer-favorite films—we aim to analyze Nicolas Cage’s past movies to uncover what makes a hit.")
st.write("We are going to explore trends in genres, overtime analysis, director performance, and movie description and audience feedback to discover insights that could inspire his next blockbuster!")
st.write("Please select a button below to continue.")

image_url = "https://th.bing.com/th/id/R.da3b86e65490d4fe9c4781de43f1d973?rik=dafUXUWVXZHnZQ&pid=ImgRaw&r=0"
st.markdown("""
    <style>
        .stButton>button {
            width: 100% !important;
            height: 60px !important;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    basic_button = st.button("Overview", use_container_width=True)

with col2:
    genre_button = st.button("Genre Performance", use_container_width=True)

with col3:
    overtime_button = st.button("Overtime Analysis", use_container_width=True)

with col4:
    director_button = st.button("Director Performance", use_container_width=True)

with col5:
    sentiment_button = st.button("Movie Description & Audience Sentiment", use_container_width=True)

if basic_button:
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_url, caption="This is Nicolas Cage", width=500)
    with col2:
        st.subheader("Basic Information")
        st.write("- Full Name: Nicolas Kim Coppola")
        st.write("- Born: January 7, 1964")
        st.write("- Years Active: 1982 – Present")
        st.subheader("Fun Fact")
        st.write("- Nicolas Cage is part of the Coppola family, one of Hollywood's most famous dynasties. His uncle is legendary director Francis Ford Coppola.")
        st.write("- Cage won the Academy Award for Best Actor for his powerful performance in the 1995 film Leaving Las Vegas.")
        st.write("- Nicolas Cage almost became a superhero when he was cast as Superman in the late '90s, but the project was canceled.")
    st.subheader("Nicolas Cage Movie Stats")
    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="Total Movies", value=no_of_movies)
        st.metric(label="First Movie Released", value=f"{first_movie} ({first_year})")
        st.metric(label="Movie with Highest Rating", value = highest_rating_movie)
    with col4:
        st.metric(label="Total Minutes Acted", value=total_mins)
        st.metric(label="Last Movie Released", value=f"{last_movie} ({last_year})")
        st.metric(label="Movie with Highest Metascore", value = highest_metascore_movie)

# Genre Performance
if genre_button:
    st.subheader("Genre Average Performance")
    st.write("This scatter plot shows how each genre performs and how frequently Nicolas Cage starred in each genre.")
    st.write("- The highest-performing genres Nicolas Cage starred in are Romance, War, Drama, and Comedy. These genres boast the highest average metascores and ratings among his films.")

    # Create an interactive scatter plot
    fig = px.scatter(
        genre_group.reset_index(),  # Reset index to make 'Genre' a column
        x="Rating",
        y="Metascore",
        text="Genre",  # Add genre labels
        title="Genre Average Performance",
        labels={"Rating": "Average Rating", "Metascore": "Average Metascore"},
        template="plotly_white",
        size="Count", 
    )
    fig.update_traces(marker=dict(sizemode='area', color='green'), textposition="top center", textfont=dict(size=13))
    fig.update_layout(
        xaxis_title="Average Rating",
        yaxis_title="Average Metascore",
        height=600,
        width=1400,
    )
    st.plotly_chart(fig)

#Overtime analysis
if overtime_button:
    st.subheader("Metascore and Genre Overtime")
    st.write("This chart shows the average metascore of all Nicolas Cage movies every five years, along with the most frequent genres for each period.") 
    st.write("- The Comedy genre shows an average trend in Metascore over time, maintaining relatively stable ratings.")
    st.write("- The metascore for Drama fluctuates across periods, but it generally remains on the higher side compared to other genres.")
    st.write("- When both Comedy and Drama genres are combined, the movie(s) achieves the highest Metascores, reflecting a strong performance.")
    
    # Create an interactive line chart
    fig = px.line(
    year_metascore_genre, 
    x='Period', 
    y='Metascore', 
    title="Nicolas Cage's Movie Rating Over Time (Grouped by 5 Years)", 
    labels={"Period": "Time Period", "Metascore": "Average Metascore"},
)
    
    fig.update_traces(line=dict(color='green'))
    for i in range(len(year_metascore_genre)):
        genre = year_metascore_genre['Genre'][i]
        if pd.notnull(genre) and genre != '':  # Check if genre is not empty or null
            fig.add_annotation(
                x=year_metascore_genre['Period'][i],  # x-position (5-year period)
                y=year_metascore_genre['Metascore'][i],  # y-position (Metascore)
                text=genre,  # Genre(s) for annotation
                font=dict(size=12),
                align="center"
            )

# Display the plot in Streamlit
    st.plotly_chart(fig)

#Director performance
if director_button:
    st.subheader("Director Average Performance")
    st.write("Since the director plays a crucial role in a movie's success, choosing the right director increases our chance of creating the next blockbuster for Nicolas Cage.")
    st.write("- Spike Jonze stands out among the directors that have worked with Cage, achieving the highest scores in both rating and metascore."
    )
    
    # Create an interactive scatter plot
    fig = px.scatter(
        director_group.reset_index(),  # Reset index to make 'Director' a column
        x="Rating",
        y="Metascore",
        text="Director",  # Add director names as labels
        title="Director Average Performance",
        labels={"Rating": "Average Rating", "Metascore": "Average Metascore"},
        template="plotly_white",
    )
    
    # Customize the layout and markers
    fig.update_traces(marker=dict(size=9, color="green"), textposition="top right", textfont=dict(size=12))  # Blue dots, labels on top-right
    fig.update_layout(
        xaxis_title="Average Rating",
        yaxis_title="Average Metascore",
        height=800,
        width=1400,
    )
    st.plotly_chart(fig)

# Word Cloud and Frequency Analysis
def display_wordcloud(freq_dist, title, width=400, height=200):
    st.subheader(title)
    wordcloud = WordCloud(width=width, height=height, background_color="white").generate_from_frequencies(freq_dist)
    fig, ax = plt.subplots(figsize=(5, 2.5))  # Adjust size for smaller wordcloud
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

if sentiment_button:
    st.subheader("Movie Description and Review analysis")
    st.write("Based on the data from Genre Performance and Metascore Performance, Nicolas Cage should focus on the genres of Drama and Comedy. Therefore, we want to explore the themes of these movies and analyze audience sentiment to gain a better understanding of what the next project should focus on and the type of sentiment it should convey.")
    st.write("- Drama movies' description emphasizes intense themes like 'war,' 'wife,' and 'wilderness,' reflecting serious and emotionally charged narratives.")
    st.write("- Reviews of drama movies focus on themes like 'dead,' 'real,' and 'new,' reflecting a mix of intense storytelling and unique perspectives.")
    st.write("- Comedy movies typically center around family and relationships, with keywords like 'family,' 'school,' and 'life' dominating the narratives.")
    st.write("- Comedy reviews highlight how these movies are 'funny' with a 'new' and 'different' twist, adding an extra 'kick' to the humor.")


    col6, col7 = st.columns(2)  # Two columns for side-by-side wordclouds
    
    with col6:
        display_wordcloud(dramadesc_freq, "Drama Description Word Cloud", width=400, height=200)
        display_wordcloud(comedydesc_freq, "Comedy Description Word Cloud", width=400, height=200)
        
    with col7:
        display_wordcloud(dramarev_freq, "Drama Review Word Cloud", width=400, height=200)
        display_wordcloud(comedyrev_freq, "Comedy Review Word Cloud", width=400, height=200)
