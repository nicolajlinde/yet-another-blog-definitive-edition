import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Body')
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:id>")
def show_post(id):
    requested_post = None
    posts = BlogPost.query.all()
    for blog_post in posts:
        print(blog_post.id)
        if blog_post.id == id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=['POST', 'GET'])
def add_post():
    form = CreatePostForm()
    if request.method == 'POST':
        x = datetime.datetime.now()
        date_now = x.strftime("%B %d, %Y")
        new_post = BlogPost(
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            date=date_now,
            body=request.form['body'],
            author=request.form['author'],
            img_url=request.form['img_url']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    else:
        return render_template('make-post.html', form=form)


@app.route("/post/edit/<int:id>", methods=['POST', 'GET'])
def edit_post(id):
    post = BlogPost.query.filter_by(id=id).first()
    post_form = {
        "title": post.title,
        "subtitle": post.subtitle,
        "body": post.body,
        "author": post.author,
        "img_url": post.img_url,
    }
    form = CreatePostForm(data=post_form)
    if request.method == 'POST':
        post.title = request.form['title']
        post.subtitle = request.form['subtitle']
        post.body = request.form['body']
        post.author = request.form['author']
        post.img_url = request.form['img_url']
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    else:
        return render_template('make-post.html', form=form, is_edit=True)


@app.route('/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
