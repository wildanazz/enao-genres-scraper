import os
import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

def init_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('dbname'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            host=os.getenv('host'),
            port=os.getenv('port')
        )
        print(f'Successfully connected to {os.getenv('dbname')} database.')
        return conn
    
    except (Exception, psycopg2.Error) as e:
        print('Failed connecting to database.', e)
        return None

def fetch_data(conn):
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM genre;')
            data = cursor.fetchall()
            genre_df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            print('Fetched data from database.')
            return genre_df
        
        except (Exception, psycopg2.Error) as e:
            print('Error fetching data from PostgreSQL.', e)
            return None
        
    else:
        try:
            genre_df = pd.read_csv(os.path.join('data', 'enao-genres.csv'))
            print('Fetched data from local folder.')
            return genre_df
        
        except Exception as e:
            print('Failed to fetch data from folder.', e)
            return None

def plot(genre_df):
    print('Plotting...')

    # Initialize the plot
    plt.figure(figsize=(20, 16))

    # Create a scatter plot with Seaborn
    sns.scatterplot(data=genre_df, x='left_pixel', y='top_pixel', hue='color', size='font_size', sizes=(20, 80), alpha=0.6, palette='Set2', legend= None)
    plt.gca().invert_yaxis()

    # Overlay the KDE plot (Density Plot)
    sns.kdeplot(data=genre_df, x='left_pixel', y='top_pixel', cmap='Blues', fill=True, thresh=0, alpha=0.3)

    # Label only a few genres (e.g., rock and jazz)
    for genre in ['metal', 'pop rock', 'rock', 'funk', 'jazz', 'rap', 'pop', 'folk', 'focus', 'classical', 'techno']:
        # Get the data points for this genre
        subset = genre_df[genre_df['genre_name'] == genre]
        for i in range(subset.shape[0]):
            plt.text(subset['left_pixel'].iloc[i], subset['top_pixel'].iloc[i], genre, 
                    horizontalalignment='center', verticalalignment='center', 
                    fontsize=subset['font_size'].iloc[i] * 0.2, color='black')

    # Title and labels
    plt.title('Every Noise at Once - Spotify Genres', fontsize=16)
    plt.xlabel('← Denser & Atmospheric, Spikier & Bouncier →', fontsize=12)
    plt.ylabel('← Organic, Mechanical & Electric →', fontsize=12)

    # Show plot
    plt.grid(True)
    plt.savefig(os.path.join('data', 'plot.png'))

if __name__ == '__main__':
    conn = init_db()
    if conn:
        genre_df = fetch_data(conn)
        if not genre_df is None:
            plot(genre_df)
