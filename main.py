from flask import request, render_template, redirect, session, flash
from app import db, app
from models import Post

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
    else:
        return render_template("new_post.html", error=error)

@app.route("/<id>")

id = request.get.args("id")
def new_post(id):

    return render_template("post.html")

if __name__=="__main__":
    app.run()

