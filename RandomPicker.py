import pandas as pd
from flask import Flask, render_template, jsonify, request
import psycopg2
from dotenv import load_dotenv
import os
from typing import Optional, List

# Load environment variables
load_dotenv()

# Get database connection information from environment variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Create Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')

def get_db_connection() -> Optional[psycopg2.extensions.connection]:
    """Create and return a database connection"""
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME,
            client_encoding='utf8'  # Explicitly set client encoding
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def get_data_from_db() -> pd.DataFrame:
    """Fetch data from the database and convert it to a Pandas DataFrame"""
    connection = get_db_connection()
    if connection is None:
        print("Database connection failed, returning an empty DataFrame")
        return pd.DataFrame()  # Return an empty DataFrame

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dataset;")
        columns = cursor.description
        if columns is None:
            print("Unable to get column descriptions, returning an empty DataFrame")
            return pd.DataFrame()  # Return an empty DataFrame

        # Extract column names from the description
        columns: List[str] = [desc[0] for desc in columns]  # desc[0] is the column name
        data = cursor.fetchall()
        if data is None:
            print("Unable to fetch data, returning an empty DataFrame")
            return pd.DataFrame()  # Return an empty DataFrame

        if not data:  # If the query result is empty
            print("Database query result is empty, returning an empty DataFrame")
            return pd.DataFrame()  # Return an empty DataFrame

        # Manually decode data
        decoded_data = []
        for row in data:
            decoded_row = [item.decode('utf-8') if isinstance(item, bytes) else item for item in row]
            decoded_data.append(decoded_row)

        df = pd.DataFrame(decoded_data, columns=columns)
        df['Score'] = pd.to_numeric(df['Score'], errors='coerce')  # Convert Score column to numeric type
        return df
    except Exception as e:
        print(f"Database query failed: {e}")
        return pd.DataFrame()  # Return an empty DataFrame
    finally:
        if connection:
            connection.close()

# Load data from the database
df = get_data_from_db()
if df.empty:  # Check if DataFrame is empty
    print("Data loaded from the database is empty. Please check the database connection or table content.")
    exit(1)  # Exit the program

@app.route('/')
def index():
    """Home route, render the page and pass type data"""
    if df.empty:
        return render_template('error.html', message="Data loading failed, please try again later.")
    types = df['Type'].dropna().unique().tolist()  # Get all unique types
    return render_template('index.html', types=types)

@app.route('/get_genres', methods=['GET'])
def get_genres():
    """Get genres based on the selected type"""
    selected_type = request.args.get('type')
    if not selected_type:
        return jsonify({'message': 'Please select a type'}), 400  # Return error message

    filtered_df = df[df['Type'] == selected_type]
    genres = filtered_df['Genres'].dropna().unique().tolist()  # Get all unique genres
    response = jsonify({'genres': genres})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'  # Set response header
    return response

@app.route('/random_item', methods=['GET'])
def random_item():
    """Randomly return an item based on the selected type, genre, and minimum score"""
    selected_genre = request.args.get('genre')
    selected_type = request.args.get('type')
    min_score_str = request.args.get('min_score', '0')

    try:
        min_score = float(min_score_str)  # Convert minimum score to float
    except ValueError:
        min_score = 0  # If conversion fails, default minimum score to 0

    # Filter data based on minimum score
    filtered_df = df[df['Score'] >= min_score]

    # Further filter data based on selected type and genre
    if selected_genre:
        filtered_df = filtered_df[filtered_df['Genres'] == selected_genre]
    if selected_type:
        filtered_df = filtered_df[filtered_df['Type'] == selected_type]

    if filtered_df.empty:
        return jsonify({'message': 'No items match the criteria'}), 404  # If no items match, return 404

    # Randomly select an item
    random_row = filtered_df.sample(n=1)
    item_name = random_row['Item_name'].values[0]
    response = jsonify({'item_name': f'《{item_name}》'})  # Return item name
    response.headers['Content-Type'] = 'application/json; charset=utf-8'  # Set response header
    return response

if __name__ == '__main__':
    app.run(debug=True)
