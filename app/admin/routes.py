from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from functools import wraps
from werkzeug.wrappers import Response
from werkzeug.security import check_password_hash
from typing import Callable, Any
from app.models import save_posts, load_posts
from app.extensions import limiter
from app.db_setup import DatabaseManager
import os

admin = Blueprint('admin', __name__, template_folder='templates')
ADMIN_USERNAME: str = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD: str = os.environ.get('ADMIN_PASSWORD')

def admin_required(f) -> Callable[..., Any]:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Please log in as admin to access this page')
                return redirect(url_for('admin.login'))
            return f(*args, **kwargs)
        return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
@limiter.limit('10 per hour')
def login() -> str|Response:
    if session.get('logged_in'):
        return redirect(url_for('blog.index'))
        
    if request.method == 'POST':
        username: str = request.form.get('username', '').strip()
        password: str = request.form.get('password', '').strip()
        hashed_password: str = DatabaseManager.get_admin_hash_from_db(ADMIN_USERNAME)
        if username == ADMIN_USERNAME and check_password_hash(hashed_password, password):
            session['logged_in'] = True
            flash('Logged in as admin successfully!')
            return redirect(url_for('blog.index'))
        else:
            flash('Invalid credentials')
        
    return render_template('login.html')

@admin.route('/logout')
def logout() -> Response:
    session.pop('logged_in', None)
    flash('Logged out successfully!')
    return redirect(url_for('blog.index'))

@admin.route('/create', methods=['GET', 'POST'])
@admin_required
def create_post() -> str|Response:
    if request.method == 'POST':
        title: str = request.form.get('title', '').strip()
        content: str = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required!')
            return redirect(url_for('admin.create_post'))
        
        posts: list = load_posts()
        new_id: int = max([p['id'] for p in posts], default=0) + 1
        
        new_post: dict = {
            'id': new_id,
            'title': title,
            'content': content,
            'author': 'Admin',  # Hardcoded as admin
            'date': datetime.now().strftime('%B %d, %Y at %H:%M'),
            'timestamp': datetime.now().isoformat()
        }
        
        posts.append(new_post)
        save_posts(posts)
        
        flash('Post created successfully!')
        return redirect(url_for('blog.index'))
        
    return render_template('create.html')

@admin.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def edit_post(post_id) -> str|Response:
    posts: list = load_posts()
    post: dict = next((p for p in posts if p['id'] == post_id), None)
    
    if post is None:
        flash('Post not found!')
        return redirect(url_for('blog.index'))
    
    if request.method == 'POST':
        title:str = request.form.get('title', '').strip()
        content: str = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Title and content are required!')
            return redirect(url_for('admin.edit_post', post_id=post_id))
        
        # Update post
        post['title'] = title
        post['content'] = content
        post['date'] = datetime.now().strftime('%B %d, %Y at %H:%M')
        post['timestamp'] = datetime.now().isoformat()
        
        save_posts(posts)
        flash('Post updated successfully!')
        return redirect(url_for('blog.show_post', post_id=post_id))
    
    return render_template('edit.html', post=post)

@admin.route('/delete/<int:post_id>')
@admin_required
def delete_post(post_id) -> Response:
    posts: list = load_posts()
    posts: dict = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    flash('Post deleted successfully!')
    return redirect(url_for('blog.index'))