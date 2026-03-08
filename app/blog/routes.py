from flask import Blueprint, render_template, session, Response, flash, redirect, url_for 
from app.models import load_posts
from app.extensions import limiter

blog = Blueprint('blog', __name__)
@blog.route('/')
@limiter.exempt
def index() -> str:
        posts: list = load_posts()
        posts.sort(key=lambda x: x['date'], reverse=True)
        return render_template('index.html', posts=posts, logged_in=session.get('logged_in'))

@blog.route('/post/<int:post_id>')
def show_post(post_id) -> str|Response:
    posts: list = load_posts()
    post: dict = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        flash('Post not found!')
        return redirect(url_for('blog.index'))

    return render_template('post.html', post=post, logged_in=session.get('logged_in'))
