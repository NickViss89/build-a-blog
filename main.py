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

   
@app.route("/newpost", methods=['POST', 'GET'])
def blog_entries():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error = ""
        body_error = ""
        if len(blog_title) == 0:
            title_error = "Title is required"
        if len(blog_body) == 0:
            body_error = "Body is required"
        if title_error or body_error:
            return render_template('new_post.html', title_error=title_error, body_error=body_error, blog_title=blog_title, blog_body=blog_body)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            post = new_blog.id
            return redirect('/blog?id=' + str(post))
    return render_template('new_post.html')
      
@app.route("/blog", methods=['GET', 'POST'])
def blog():

    posts = Blog.query.all()
    id = request.args.get('id')
    unique_id = Blog.query.filter_by(id=id).first()
    if not unique_id:
        return render_template("blog.html", posts=posts)
    else:
        return render_template("single_post.html", post=unique_id)




if __name__ == '__main__':
    app.run()