from . import posts
from flask import request, flash, redirect, url_for, render_template
from app.models import PostForm, db, Post
from flask_login import current_user, login_required

@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        caption = form.caption.data
        img_url = form.img_url.data
        user_id = current_user.id

        #create an instance of our post class
        post = Post(title, caption, img_url, user_id)

        # add user to database
        db.session.add(post)
        db.session.commit()

        flash(f"Post {title} successfully created!", 'success')
        return redirect(url_for('feed'))
    else:
        return render_template('signup.html', form=form)

