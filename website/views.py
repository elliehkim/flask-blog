from flask import Flask, render_template, request, url_for, redirect, flash, Blueprint, current_app
from flask_login import login_required, current_user
from . import posts, enquiries
from .models import Enquiry, Post
from .db import db


views = Blueprint("views", __name__)

@ views.route('/', methods=['GET', 'POST'])
@ views.route('/home', methods=['GET', 'POST'])
def index():
    blog_posts = db.blog_collection.find()
    posts = [Post.from_dict(post) for post in blog_posts]
 
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not phone or not message:
            flash('All fields required', category="error")
            return redirect(url_for('views.index'))
        else:
            enquiry = Enquiry(name, email, phone, message)
            enquiries.insert_one(enquiry.json())
            flash('Enquiry Received', category="success")
            return redirect(url_for('views.index'))

    return render_template("index.html", user=current_user, posts =posts)


@ views.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        img_file = request.files.get('image')

        if not title:
            flash('Title cannot be empty', category="error")
            return redirect(url_for('views.write'))
        if not content:
            flash('Post cannot be empty', category="error")
            return redirect(url_for('views.write'))
        
        new_post = Post(current_user.username, title, content)
        
        if img_file:
            new_post.save_image(img_file)
        
        db.blog_collection.insert_one(new_post.json())

        flash('Post Created', category="success")
        return redirect(url_for('views.index'))
    
    return render_template("write.html", user=current_user)


@ views.route('/posts/<string:post_id>')
def single_post(post_id):
    single_post = posts.find_one({'_id': post_id})
    post = Post.from_dict(single_post)
    return render_template("single_post.html", user=current_user, post=post)


@ views.route('/delete/<string:post_id>')
def delete(post_id):
    delete_post = posts.find_one({'_id': post_id})
    if not current_user.is_authenticated:
        flash("You do not have permission to delete this post", category="error")
        return redirect(url_for('views.single_post', post_id=post_id))
    elif current_user.username != delete_post['username'][0]:
        flash("You do not have permission to delete this post", category="error")
        return redirect(url_for('views.single_post', post_id=post_id))
    else:
        posts.delete_one(delete_post)
        flash('Post Deleted', category="success")
    return redirect(url_for('views.index'))


@ views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return redirect(url_for('views.index'))
    else:
        posts.create_index([('title', 'text')])
        search = request.form.get('search')
        results = posts.find({"$text": {"$search": search}})
        count = posts.count_documents({"$text": {"$search": search}})

        result_posts = [Post.from_dict(result) for result in results]

        if count != 0:
            return render_template('index.html', posts=result_posts, user=current_user)
        else:
            message = "Not Found"
            return render_template('index.html', message=message, user=current_user)
