# Reddit Post Tokenizer using PRAW,Flask,nltk,gensim
This project is a basic Flask server with no middleware,session mgmt etc to
yield tokenized reddit posts for natural language processing

Also provides some basic user stats with visualizations using pygal(generate svg in python)

## You will need PRAW setup with a reddit api key & secret
follow directions in https://praw.readthedocs.io/en/stable/getting_started/authentication.html#oauth

create a `creds.json` file 
```json
[{
    "client_id": "",
    "client_secret": ""
}]
```

## To run the server (tested using py 3.8.10:

### macOS/Linux 
```bash
cd red_flask_scrape
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python -c "import nltk;nltk.download('stopwords')"
python ex_webserver.py
```
### windows (only tested in virtualbox with only python3 installed)
```cmd
cd red_flask_scrape
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python -c "import nltk;nltk.download('stopwords')"
python ex_webserver.py
```
## Web interface
Still working on the web interface, here are the endpoints
/ is homepage, will show some links and 2 input boxes if authenticated
/user_stats will show some user visaulizations if authenticated
/download will download some posts
/user_clusters takes the input box as (posts,clusters) and does some magic to show LDA(will talk more later)

can use reddit creds for testing:
u: sussybaklava
pw: wizard27

i saved a bunch of random posts from r/all and also specific subreddits r/nosleep r/programming r/nba feel free to add more
