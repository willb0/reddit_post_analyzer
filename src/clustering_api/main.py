from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from asyncpraw import Reddit
from utils import *
from models import *
import os
import time

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]


app = FastAPI()
reddit =  Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    user_agent="saved post aggregator:v1 by u/Nerg44"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(process_time)
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def home():
    return {"message": "Hello from docker fastapi template"}


@app.post("/saved_posts")
async def saved(req: PostsRequest):
    if req.raw == True:
        raw = await nltk_praw_raw(reddit, req.num_posts)
        return {"res": raw}
    reg = await nltk_praw(reddit, req.num_posts)
    return {"res": reg}


@app.post("/saved_posts_async")
async def saved(req: PostsRequest):
    res = await nltk_praw_raw_async(reddit, req.num_posts)
    return {"res": res}


@app.get("/user")
async def user(request: Request):
    if await reddit.user.me():
        u = await reddit.user.me()
        return {"name": u.name}
    authurl = reddit.auth.url(["identity", "history", "read"], "...", "permanent")
    return {"login": authurl}


@app.get("/authorize_callback")
async def authorize(request: Request):
    state = request.query_params["state"]
    code = request.query_params["code"]
    info = await reddit.auth.authorize(code)
    user = await reddit.user.me()
    print(f"{user} logged into reddit")
    return RedirectResponse(url=app.url_path_for("user"))
