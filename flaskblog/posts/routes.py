from flask import Blueprint
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flask import render_template, url_for, flash, redirect, request , abort
from flaskblog import db
from flask_login import current_user,  login_required


posts = Blueprint('posts',__name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Has Been Successfully Added', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Posts', form=form, lengend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('post.html', title=posts.title, post=posts)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    posts = Post.query.get_or_404(post_id)
    if posts.author != current_user:
        abort(403)
    else:
        form = PostForm()
        if form.validate_on_submit():
            posts.title = form.title.data
            posts.content = form.content.data
            db.session.commit()
            flash('Your Post Has Been Updated!', 'success')
            return redirect(url_for('posts.post', post_id=posts.id))
        elif request.method == 'GET':
            form.title.data = posts.title
            form.content.data = posts.content
        return render_template('create_post.html', title='Update Post', form=form , lengend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    posts = Post.query.get_or_404(post_id)
    if posts.author != current_user:
        abort(403)
    db.session.delete(posts)
    db.session.commit()
    flash('Your Post Has Been Deleted!', 'success')
    return redirect(url_for('main.home'))
