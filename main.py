from flask import request, render_template, redirect, session, flash, url_for
from app import db, app
from models import Post, User
from hashutils import check_hash, make_hash, make_salt

@app.before_request
def require_login():
    allowed_routes = ["register", "login", "all_posts", "index"]
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect ("/login")

@app.route("/")
def index():
    users = User.query.all()
    return render_template("main_page.html", users=users)

@app.route('/all-posts', methods=['POST','GET'])
def all_posts():

    users = User.query.all()

    if request.args.get("id") != None:
        id = request.args.get("id") 
        post = Post.query.get(id)
        return render_template("post.html", post=post, users=users)

    if request.args.get("username") != None:
        username = request.args.get("username")
        owner = User.query.filter_by(username=username).first()
        user_posts = Post.query.filter_by(owner_id=owner.id).all()
        return render_template("user_posts.html", user_posts=user_posts, username=username)

    else:
        posts = Post.query.all()
        users = User.query.all()
        return render_template('all_posts.html', posts=posts, users = users)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        if len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = "Please enter a username between 3 and 20 characters, with no spaces."
        else:
            username_error = ''
        if len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = "Please enter a password between 3 and 20 characters, with no spaces."
        else:
            password_error = ''
        if password != verify or len(password) ==0 and len(verify) == 0:
            verify_error = "Password and verify password must match"
        else: 
            verify_error =''

        if username_error and password_error and verify_error:
            return render_template("registration.html", username_error = username_error, password_error=password_error, verify_error=verify_error, username=username)
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session["username"] = username
                flash("Welcome!")
                return redirect("/add-new")
            else:
                flash("Duplicate User. Please login.")
                return redirect("/login")
    else:
        return render_template("registration.html")

@app.route("/logout")
def logout():
    del session["username"]
    flash("Logged Out")
    return redirect("/")


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_hash(password, user.pw_hash):
            session["username"] = username
            flash("Logged In!")
            return redirect('/add-new')
        else:
            if user == None:
                error = "User does not exist. Please register a new user."
                return render_template("login.html", error=error)
            else:
                error = "Password incorrect."
                return render_template("login.html", error=error, username=username)
    else:
        error=""
        return render_template("login.html")
        
@app.route("/add-new", methods = ["POST", "GET"])
def new():
    error = ""
    owner = User.query.filter_by(username=session['username']).first()
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
            post = Post(title, content, owner)
            db.session.add(post)
            db.session.commit()
            return render_template("post.html", post=post)
    else:
        return render_template("new_post.html", error=error)

if __name__=="__main__":
    app.run()

