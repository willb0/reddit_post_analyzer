import re
import nltk
import time
from asyncpraw.models import MoreComments,Comment,Submission
# import aiofiles
import asyncio
import nest_asyncio
nest_asyncio.apply()


stop = set(nltk.corpus.stopwords.words('english'))
words = set(nltk.corpus.words.words())





async def nltk_praw(r, posts):
    start = time.time()

    def comments(post):
        print(f'{time.time()-start} elapsed in comments')
        """Get nested comments from a PRAW post model"""
        return [comment.body[:200] for comment in post.comments.list()[:25] if not isinstance(comment, MoreComments)]
    user = await r.user.me()
    saved = list(user.saved(limit=posts).__iter__())

    p = re.compile('[a-zA-Z]+')
    # I only want Submissions, comments can be parsed as well
    # by changing 'Submission' to 'Comment'
    # trying to do set operation for speed:
    # a - (a&b) will give all elements in a not in b
    # in this case we want all elements in submissions not in stopwords
    # submissions = [[y for y in p.findall(
    #    f'{x.title} {x.selftext[:200]} {comments(x)}'.rstrip().lower())] for x in saved if type(x).__name__ == 'Submission' and print('{} elapsed'.format(time.time()-start)) == None]
    submissions = [[y for y in filter(lambda x:len(x) > 1 and x not in stop and x in words, p.findall(
      f'{x.title} {x.selftext[:200]} {comments(x)}'.rstrip().lower()))] for x in saved if type(x).__name__ == 'Submission' and print('{} elapsed'.format(time.time()-start)) == None]
    # print(submissions)
    return (submissions)

async def nltk_praw_raw_async(r, posts):

    async def get_comment_str(comment):
        return await comment.body

    async def get_comments_str(comments):
        """Get nested comments from a PRAW post model"""
        tasks = []
        for comment in comments:
            if comment is not MoreComments:
                tasks.append(get_comment_str(comment))
        await asyncio.gather(*tasks)
        return ' '.join(tasks)

    async def get_post_str(post_id):
        post = await r.submission(post.id)
        comments = await post.comments.list()
        res = await get_comments_str(comments)
        res = res[:25]
        res = ' '.join(res)
        return f'{post.title} {post.selftext} {res}'.rstrip().lower()
        
    async def get_post_strings(posts):
        tasks = []
        async for post in posts:
            try:
                tasks.append(get_post_str(submission))
            except:
                pass
        await asyncio.gather(*tasks)
        return ' '.join(tasks)

    user = await r.user.me()
    saved = user.saved(limit=posts)
    
     
    # print(submissions)
    return await get_post_strings(saved)
    
async def nltk_praw_raw(r, posts):
    async def comments(comments):
        """Get nested comments from a PRAW post model"""
        async def get_comment(obj):
            if isinstance(obj,MoreComments):
                comments = await obj.comments()
                tasks = []
                for comment in comments:
                    tasks.append(get_comment(comment))
                res = await asyncio.gather(*tasks)
                return ' '.join(res)
            else:
                return obj.body
        tasks = []
        for comment in comments:
            tasks.append(get_comment(comment))
        res = await asyncio.gather(*tasks)
        return ' '.join(res)

    async def gather(id):
        try:
            await id.load()
        except:
            print('idk man')
            return ''
        if isinstance(id,Submission):
            comms = await id.comments.list()
            comms = await comments(comms[:10])
            return f'{id.title} {id.selftext} {comms}'
        else:
            comms = await id.replies.list()
            comms = await comments(comms)
            return f'{id.body} {comms}'
            
    user = await r.user.me()
    saved = user.saved(limit=posts)
    submissions = []
    async for x in saved:
        print(type(x))
        submissions.append(gather(x))
    submissions = await asyncio.gather(*submissions)
    return (submissions)