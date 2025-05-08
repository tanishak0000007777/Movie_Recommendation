# CouchCritic

A smart movie recommendation app built using Python and Streamlit.

## Features

- Recommends similar movies based on a selected movie.
- Displays posters and titles of recommended movies.
- Allows users to watch trailers directly from YouTube.
- Shows a dynamic banner featuring a random movie.
- Uses real-time movie details from TMDb API.

## Technologies Used

- Python
- Streamlit
- TMDb API
- Pickle (for movie data and similarity matrix)

## How to Use

1. Make sure you have Python and Streamlit installed.
2. Place `movie.pkl`, `similarity.pkl`, and `code.py` in the same folder.
3. Run the app using the following command:
   ```bash
   streamlit run code.py
Select a movie from the dropdown to get recommendations.

Click "Watch Trailer" to preview the movie trailer inside the app.

Project Structure
bash
Copy
Edit
CouchCritic/
│── code.py          # Main Streamlit application
│── movie.pkl        # Pickled movie data
│── similarity.pkl   # Pickled similarity matrix
License
This project is open-source and free to use. Feel free to modify and enhance it!

Author
Tanishak Bansal
GitHub: https://github.com/tanishak0000007777
