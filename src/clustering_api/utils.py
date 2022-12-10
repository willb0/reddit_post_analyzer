import re
import time
import nltk
from praw.models import MoreComments


stop = set(nltk.corpus.stopwords.words('english'))





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
    submissions = [[y for y in filter(lambda x:len(x) > 1 and x not in stop, p.findall(
        f'{x.title} {x.selftext[:200]} {comments(x)}'.rstrip().lower()))] for x in saved if type(x).__name__ == 'Submission' and print('{} elapsed'.format(time.time()-start)) == None]
    # print(submissions)
    return (submissions)