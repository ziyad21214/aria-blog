import os
import json

POSTS_FILE: str = os.path.abspath('posts.json')


def load_posts() -> list[dict]|list:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as f:
                return json.load(f)
        return []

def save_posts(posts) -> None:
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f, indent=2)