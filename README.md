# 🎬 Movie Recommendation Engine

A simple content-based movie recommendation system built with:

- Python
- Pandas
- Scikit-learn
- Streamlit
- MovieLens dataset

The application allows a user to select a movie and receive the top 10
movies that are most similar to it based on movie title and genre information.

Movie similarity is calculated using:

1. TF-IDF (Term Frequency-Inverse Document Frequency)
2. Cosine similarity

MovieLens ratings are also displayed alongside the recommendations.

---

## 📌 Features

- Select a movie from a searchable dropdown
- Recommend the top 10 similar movies
- Content-based filtering
- TF-IDF text vectorization
- Cosine similarity
- Movie genre information
- MovieLens average ratings
- Number of ratings
- Simple Streamlit interface
- Runs locally in VS Code
- Can be deployed using Streamlit Community Cloud

---

## 📂 Project Structure

```text
movie-recommendation-engine/
│
├── app.py
├── recommender.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── ml-latest-small/
        ├── movies.csv
        ├── ratings.csv
        ├── tags.csv
        └── links.csv
````

---

# 📊 Dataset

This project uses the MovieLens `ml-latest-small` dataset provided by
GroupLens Research at the University of Minnesota.

The dataset contains approximately:

* 9,742 movies
* 100,836 ratings
* 3,683 tag applications
* 610 users

The dataset was generated in September 2018.

Official MovieLens page:

https://grouplens.org/datasets/movielens/

Direct download:

https://files.grouplens.org/datasets/movielens/ml-latest-small.zip

---

# ⬇️ Dataset Setup

## Step 1 — Download the dataset

Download:

`ml-latest-small.zip`

from the official GroupLens MovieLens dataset page:

https://grouplens.org/datasets/movielens/

---

## Step 2 — Extract the ZIP file

Extract the downloaded ZIP file.

It should produce a folder called:

```text
ml-latest-small
```

Inside that folder you should see:

```text
ml-latest-small/
├── links.csv
├── movies.csv
├── ratings.csv
├── tags.csv
└── README.txt
```

---

## Step 3 — Create the data folder

Inside your project folder create:

```text
data/
```

Then place the complete `ml-latest-small` folder inside it.

Your final structure should be:

```text
movie-recommendation-engine/
│
├── app.py
├── recommender.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── ml-latest-small/
        ├── links.csv
        ├── movies.csv
        ├── ratings.csv
        ├── tags.csv
        └── README.txt
```

IMPORTANT:

The application expects the files to be located at:

```text
data/ml-latest-small/movies.csv
data/ml-latest-small/ratings.csv
```

Do not move `movies.csv` and `ratings.csv` somewhere else unless you also
change the paths in `recommender.py`.

---

# 💻 Running Locally in VS Code

## Step 1 — Install Python

Install Python 3.12.

Check your installation:

```bash
python --version
```

You should see something similar to:

```text
Python 3.12.x
```

---

## Step 2 — Open the project in VS Code

Open the project folder:

```text
movie-recommendation-engine
```

in Visual Studio Code.

---

## Step 3 — Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

If you are using PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## Step 4 — Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Step 5 — Start Streamlit

Make sure your terminal is currently inside the project root:

```text
movie-recommendation-engine/
```

Then run:

```bash
streamlit run app.py
```

Streamlit will display a local URL, normally similar to:

```text
http://localhost:8501
```

Open that address in your browser.

---

# 🧠 How the Recommendation System Works

This project uses content-based filtering.

## 1. Load the movie data

The application reads:

```text
movies.csv
```

The important columns are:

```text
movieId
title
genres
```

---

## 2. Prepare movie text

The title and genres are combined into one text feature.

For example:

```text
Toy Story (1995) Toy Story (1995) Adventure Animation Children Comedy
```

The title is repeated so that the movie title has slightly more influence
than an individual genre.

---

## 3. TF-IDF

The application uses Scikit-learn's:

```python
TfidfVectorizer
```

TF-IDF converts the movie text into numerical vectors.

Words that occur frequently across many movies receive less importance,
while more distinctive words receive greater importance.

The application also uses:

```python
ngram_range=(1, 2)
```

which allows both individual words and two-word combinations to contribute
to the representation.

---

## 4. Cosine Similarity

After creating TF-IDF vectors, the application calculates cosine similarity.

Conceptually:

```text
Movie A vector
       ↓
   TF-IDF
       ↓
Numerical vector
       ↓
Cosine similarity
       ↓
Compare with all movies
       ↓
Sort similarity scores
       ↓
Return top 10
```

A similarity value closer to `1` means the movie representations are more
similar.

---

# ⭐ Ratings

Ratings are loaded from:

```text
ratings.csv
```

The application calculates:

* Average rating
* Number of ratings

These values are displayed next to recommendations.

Ratings are NOT used to calculate content similarity.

This makes the recommendation algorithm a content-based system rather than
a collaborative filtering system.

---

# 🚀 Deploy to Streamlit Community Cloud

Streamlit Community Cloud can deploy applications directly from GitHub.

Official deployment site:

https://share.streamlit.io/

---

## Step 1 — Create a GitHub repository

Go to GitHub and create a new repository.

For example:

```text
movie-recommendation-engine
```

You can make the repository public, which is the simplest option for a
course project.

---

## Step 2 — Add the project files

Your GitHub repository should contain:

```text
movie-recommendation-engine/
│
├── app.py
├── recommender.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── ml-latest-small/
        ├── movies.csv
        ├── ratings.csv
        ├── tags.csv
        └── links.csv
```

The CSV files need to be available to the deployed application because
Community Cloud runs your application on a remote machine.

---

## Step 3 — Push the project to GitHub

From the VS Code terminal:

```bash
git init
```

Add the files:

```bash
git add .
```

Create the first commit:

```bash
git commit -m "Initial movie recommendation engine"
```

Connect your GitHub repository:

```bash
git remote add origin https://github.com/YOUR_USERNAME/movie-recommendation-engine.git
```

Rename the branch:

```bash
git branch -M main
```

Push:

```bash
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# ☁️ Step 4 — Open Streamlit Community Cloud

Go to:

https://share.streamlit.io/

Sign in using GitHub.

If prompted, authorize Streamlit to access your GitHub repositories.

---

# ☁️ Step 5 — Create the application

Click:

```text
Create app
```

Choose:

```text
Yup, I have an app
```

Select your:

```text
Repository:
YOUR_USERNAME/movie-recommendation-engine
```

Select:

```text
Branch:
main
```

For the main file / entrypoint, select:

```text
app.py
```

You can optionally choose a custom app URL.

Then click:

```text
Deploy
```

---

# 🔧 Step 6 — Wait for deployment

Streamlit Community Cloud will:

1. Clone your GitHub repository
2. Create a Python environment
3. Install the packages in `requirements.txt`
4. Start `app.py`
5. Give your application a public `streamlit.app` URL

The first deployment may take a few minutes.

---

# 🔄 Updating the deployed application

Once the application is connected to GitHub, pushing changes to the selected
branch will cause Community Cloud to update the application.

For example:

```bash
git add .
git commit -m "Improve recommendation UI"
git push
```

Community Cloud will detect the repository update and redeploy the app.

---

# 🛠️ Troubleshooting

## Error: movies.csv not found

Check that your project contains:

```text
data/ml-latest-small/movies.csv
```

and:

```text
data/ml-latest-small/ratings.csv
```

---

## Error: ModuleNotFoundError

Run:

```bash
pip install -r requirements.txt
```

Make sure your virtual environment is activated.

---

## Streamlit command not found

Try:

```bash
python -m streamlit run app.py
```

---

## App works locally but not on Streamlit Cloud

Check:

1. `requirements.txt` exists in the repository root.
2. `app.py` is pushed to GitHub.
3. `recommender.py` is pushed to GitHub.
4. The `data/ml-latest-small/` directory is pushed to GitHub.
5. `movies.csv` and `ratings.csv` exist inside that directory.
6. The Streamlit deployment is using the correct branch.
7. The Streamlit deployment is using `app.py` as the entrypoint.

---

# 📚 Possible Future Improvements

This project can be extended in several ways.

### 1. Add movie posters

Use the TMDB IDs from:

```text
links.csv
```

to retrieve movie poster information.

### 2. Add user-based recommendations

Implement collaborative filtering using the ratings data.

### 3. Combine content and ratings

Create a hybrid recommendation system combining:

```text
Content similarity
+
Collaborative filtering
```

### 4. Add genre filters

Allow users to select:

```text
Action
Comedy
Drama
Sci-Fi
Horror
Romance
```

etc.

### 5. Add evaluation metrics

Possible recommendation-system evaluation metrics include:

* Precision@K
* Recall@K
* Precision@10
* Recall@10
* Mean Average Precision

---

# 📜 Dataset License / Attribution

This project uses the MovieLens dataset provided by GroupLens Research.

Please review the MovieLens README and usage conditions before
redistributing the dataset or using the project commercially.

Citation:

F. Maxwell Harper and Joseph A. Konstan. 2015.
The MovieLens Datasets: History and Context.
ACM Transactions on Interactive Intelligent Systems 5, 4: 19:1–19:19.

DOI:

https://doi.org/10.1145/2827872

---

# 👨‍💻 Technology Stack

| Technology                | Purpose                       |
| ------------------------- | ----------------------------- |
| Python                    | Programming language          |
| Pandas                    | Data loading and manipulation |
| Scikit-learn              | TF-IDF and cosine similarity  |
| Streamlit                 | Web interface                 |
| MovieLens                 | Movie and rating data         |
| GitHub                    | Source-code hosting           |
| Streamlit Community Cloud | Deployment                    |

---

# 🎬 Result

The final application allows a user to:

1. Select a movie.
2. Click "Get Recommendations".
3. Receive 10 similar movies.
4. View their genres.
5. View their MovieLens average ratings.
6. View the content similarity score.

This demonstrates a complete machine-learning application from dataset
preparation to model construction, user interface, and cloud deployment.