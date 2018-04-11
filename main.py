from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    completed = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['post']
        new_task = Post(post_name)
        db.session.add(new_post)
        db.session.commit()

    posts = Task.query.filter_by(completed=False).all()
    completed_posts = Task.query.filter_by(completed=True).all()
    return render_template('post.html',title="Blog it!", 
        posts=posts, completed_posts=completed_posts)


@app.route('/new-post', methods=['POST'])
def new_post():

    post_id = int(request.form['task-id'])
    post = Post.query.get(post_id)
    post.completed = True
    db.session.add(post)
    db.session.commit()

    return redirect('/all-posts')


if __name__ == '__main__':
    app.run()