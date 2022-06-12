from cgitb import html

from datetime import datetime
from email.policy import default
from unicodedata import name
from django import db
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    content = db.Column(db.Text,nullable = False)
    author = db.Column(db.String(100),nullable = False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self) -> str:
        return 'Blog post ' + str(self.id)
all_posts = [
    {
        'title':'Post 1',
        'content':'This is the content of post 1',
        'author':'Shaikh'
    },
    {
        'title':'Post 2',
        'content':'This is the content of post 2'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(
            title = post_title,
            content = post_content,
            author = 'Shaikh',
            )
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html',posts=all_posts)

    return render_template("posts.html",posts=all_posts)

# pass variable in url
@app.route('/hello/<string:name>')
def hello(name):
    return "Hello :" + name

# pass nested variable in url / dynamic url
@app.route('/blog/users/<string:name>/posts/<int:_id>')
def blog(name,_id):
    return "Hello :" + name + "ur id is: " + str(_id)


if __name__ == "__main__":
    app.run(debug=True)