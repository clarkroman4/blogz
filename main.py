from flask import request, render_template, redirect, session, flash
from app import db, app
from models import Post

@app.route("/")
def index():

    if request.args.get("id") != None:
        id = request.args.get("id")
        post = Post.query.get(id)
        return render_template("post.html", post=post)
    else:   
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
            post = Post(title, content)
            db.session.add(post)
            db.session.commit()
            return render_template("post.html", post=post)
    else:
        return render_template("new_post.html", error=error)

if __name__=="__main__":
    app.run()

