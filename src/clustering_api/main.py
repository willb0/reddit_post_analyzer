from fastapi import FastAPI,Request
from starlette.responses import RedirectResponse
from praw import Reddit
import os

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

@app.get('/')
def home():
    return {'message':'Hello from docker fastapi template'}

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




