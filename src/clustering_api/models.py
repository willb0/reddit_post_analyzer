from pydantic import BaseModel


class PostsRequest(BaseModel):
    num_posts: int = 10
    raw: bool = False
