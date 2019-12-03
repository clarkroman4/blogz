from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(255))
    content = db.Column(db.String(10000))

    def __init__(self, post, content):
        self.post = post
        self.content = content




@app.route("/", methods = ["POST", "GET"])
def index():
    posts = Post.query.all()
    return render_template("main_page.html", posts=posts)

@app.route("/add-new", methods = ["POST", "GET"])
def new():
    error = ""
    if request.method =="POST":
        title = request.form["title"]
        content = request.form["content"] 
        if title == "" and content =="":
            error = "Please add a title and content to your post!"
            return render_template("new_post.html", error=error, title=title, content=content)
        elif title == "":
            error = "Please add a title to your post!"
            return render_template("new_post.html", error=error, title=title, content=content)
        elif content == "":
            error = "Please add content to your post!"
            return render_template("new_post.html", error=error, title=title, content=content)
        else:
            new_post = Post(title, content)
            db.session.add(new_post)
            db.session.commit()
            return redirect("/?=" + title)   
    else:
        return render_template("new_post.html", error=error)



if __name__=="__main__":
    app.run()

