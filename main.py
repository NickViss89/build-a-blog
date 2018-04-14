from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog1:password@localhost:8889/build-a-blog1'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

   
@app.route("/newpost", methods=['GET', 'POST'])
def blog_entries():
    if request.method == 'POST':    
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

    title = Blog.query.all()
    body = Blog.query.all()  
    return render_template('new_post.html')
        
@app.route("/blog", methods=['GET', 'POST'])
def blog():

    title = Blog.query.get('title')
    body = Blog.query.get('body')
    posts = Blog(title, body)
    return render_template("blog.html", title=title, body=body)


if __name__ == '__main__':
    app.run()