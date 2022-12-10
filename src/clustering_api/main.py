from fastapi import FastAPI,Request
from starlette.responses import RedirectResponse
from praw import Reddit
from utils import *
from models import *
import os
import time

CLIENT_ID  = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]


app = FastAPI()
reddit = Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    user_agent = 'stinky'
)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(process_time)
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get('/')
def home():
    return {'message':'Hello from docker fastapi template'}

@app.post('/saved_posts')
def saved(req:PostsRequest):
    return {'res':nltk_praw(reddit,req.num_posts)}


@app.get('/user')
def user(request: Request):
    if reddit.user.me():
        return {'name': reddit.user.me().name}
    authurl = reddit.auth.url(["identity", "history", "read"], "...", "permanent")
    return {'login':authurl}

@app.get('/authorize_callback')
def authorize(request: Request):
    state = request.query_params['state']
    code = request.query_params['code']
    info = reddit.auth.authorize(code)
    user = reddit.user.me()
    print(f'{user} logged into reddit')
    return RedirectResponse(url=app.url_path_for('user'))





