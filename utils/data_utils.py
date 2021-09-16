from praw.models import MoreComments
from praw.reddit import Submission
import re
import time
import nltk
import pandas as pd
from .graph_utils import *

stop = set(nltk.corpus.stopwords.words('english'))

def gen_csv(r, n):
    return '\n'.join([y for y in [' '.join(x)
                           for x in nltk_praw(r, n)]])

def praw_saved_text(r):
    """
    Function to get all of a Reddit user's saved posts and the text
    content within. This function assumes use of PRAW and OAuth
    """
    def comments(post):
        """Get nested comments from a PRAW post model"""
        return [comment.body for comment in post.comments.list()[:25] if not isinstance(comment, MoreComments)]
    user = r.user.me()
    saved = list(user.saved(limit=10))
    lsaved = len(saved)

    # I only want Submissions, comments can be parsed as well
    # by changing 'Submission' to 'Comment'
    submissions = [x for x in saved if type(x).__name__ == 'Submission']
    # First part is list comp using str.format to create one long
    # string that contains Title,selftext,comments
    #
    # Second part is mapping re.sub to get rid of all escape
    # characters
    #
    # Third part is some BS i had to add because my re.sub
    # was not extracting single brackies
    submissions_list = ['{} {} {} '.format(
        x.title, x.selftext, comments(x)).rstrip() for x in submissions]
    submissions_list = list(
        map(lambda x: re.sub('[\[\]\n\t]', '', x), submissions_list))
    submissions_list = [[z.replace('\\', '') for z in re.findall(
        '[A-z\d]+', x)] for x in submissions_list]

    return submissions_list


def nltk_praw(r, posts):
    start = time.time()

    def comments(post):
        print(f'{time.time()-start} elapsed in comments')
        """Get nested comments from a PRAW post model"""
        return [comment.body[:200] for comment in post.comments.list()[:25] if not isinstance(comment, MoreComments)]
    user = r.user.me()
    saved = list(user.saved(limit=posts))
    lsaved = len(saved)

    p = re.compile('[a-zA-Z]+')
    # I only want Submissions, comments can be parsed as well
    # by changing 'Submission' to 'Comment'
    # trying to do set operation for speed:
    # a - (a&b) will give all elements in a not in b
    # in this case we want all elements in submissions not in stopwords
    submissions = [[y for y in filter(lambda x:len(x) > 3 and x not in stop, p.findall(
        f'{x.title} {x.selftext[:200]} {comments(x)}'.rstrip().lower()))] for x in saved if type(x).__name__ == 'Submission' and print('{} elapsed'.format(time.time()-start)) == None]
    # print(submissions)
    return(submissions)


def gen_user_stats(user, posts):
    '''
    top 5 subreddits by appearance
    group by subreddit order by count

    top 5 subreddits by total upvotes
    group by subreddit order by sum(score)

    pie chart of makeup
    group by subreddit agg by sum(score)

    smallest 5 subreddits subscribed to
    min(subs)

    '''

    data = pd.DataFrame([{'subreddit': str(submission.subreddit.display_name),
                          'score': int(submission.score),
                          'subs': int(submission.subreddit.subscribers)} for submission in user.saved(limit=posts)])
    subred = data.groupby('subreddit')
    title1 = 'Top 5 subreddits by appearance in saved'
    top_app = subred.count(
    ).sort_values(by='score', ascending=False)['score'].head(5)
    # print(top_app)
    title2 = 'Top 5 subreddits by total upvotes in saved'
    top_up = subred.sum()['score'].sort_values(ascending=False).head(5)
    # print(top_up)
    title3 = 'pie chart of all subreddits with appearances'
    totalagg = subred.count()['score']
    # print(totalagg)
    title4 = 'smallest subreddits with saved post'
    smallest = data.sort_values(
        by='subs')[['subreddit', 'subs']].drop_duplicates().head(10)
    subs = list(smallest.subs)
    subr = list(smallest.subreddit)
    smallest = pd.Series(subs, index=subr)
    return [bar_graph(top_app, title1),
            bar_graph(top_up, title2),
            pie_chart(totalagg, title3),
            bar_graph(smallest, title4)]                           