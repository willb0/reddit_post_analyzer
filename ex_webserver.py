# example_webserver.py #
########################
from flask import Flask, request, session, Response, flash, url_for, render_template
import praw
from utils.data_utils import nltk_praw,gen_user_stats, gen_csv
from werkzeug.utils import redirect
from utils.document_clustering_utils import lda
import json


app = Flask(__name__)

cred = None
with open('creds.json') as f:
    cred = json.load(f)[0]

CLIENT_ID = cred['client_id']
CLIENT_SECRET = cred['client_secret']
REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'


@app.route('/')
def homepage():
    if r.user.me():
        return render_template('index.html', user=r.user.me().name, numposts=len(list(r.user.me().saved(limit=100))))
    authurl = r.auth.url(["identity", "history", "read"], "...", "permanent")
    return "<a href = %s>authorization_link</a>" % authurl


@app.route('/user_stats')
def user_stats():
    '''
    top 5 subreddits by appearance
    top 5 subreddits by total upvotes
    pie chart of makeup
    smallest 5 subreddits subscribed to

    '''
    user = r.user.me()
    if user:
        top5app, top5up, pie, smallest5 = gen_user_stats(user, 100)
        content = {'g1': top5app,
                   'g2': top5up,
                   'g3': pie,
                   'g4': smallest5}
        return render_template('stats.html', **content)
    return '<b>Not Authenticated</b><br/><a href = />login here</a>'


@app.route('/authorize_callback')
def authorized():
    state = request.args.get('state', '')
    code = request.args.get('code', '')
    info = r.auth.authorize(code)
    user = r.user.me()
    # print(state, info, user.name, file=sys.stderr)
    flash("%s logged in to reddit" % (str(user.name)))
    return redirect(url_for('homepage'))


@ app.route('/download')
def download():
    if r.user.me():
        n = int(request.args.get('num_posts_dl', None))
        if n:
            data = gen_csv(r,n)
        else:
            data = gen_csv(r,10)
        return Response(
            data,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=posts.csv"})
    return '<b>Not Authenticated</b><br/><a href = />login here</a>'


@ app.route('/user_clusters')
def user_clusters():
    if r.user.me():
        data = nltk_praw(r, int(request.args['number_of_posts']))
        print('data done')
        return lda(data, int(request.args['num_clusters']))
    return '<b>Not Authenticated</b><br/><a href = />login here</a>'


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'ringding'
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    redirect_uri=REDIRECT_URI,
                    user_agent='my app to scrape saved posts')
    print(r)
    app.run(debug=True, port=65010)
