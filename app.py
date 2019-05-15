"""
    Author : Rickardo Henry
    Proj ID: IS211_Final Project
    Description:
        This is a BlogPost, Just like every other BlogPost
        there are two sets of users, standard and Admin.

        There is already a Test Entry of Blog Created, Click
        Read More to access the full Blog.

        Standard Users must create an account to read the
        full Blog, and participate by making comments to the Blog.
        -Here are Admin Account Credentials:
                Email: rhenry@gmail.com
                Passw: admin11230
"""




from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
import os, sys, random, sqlite3
from random import shuffle
from os import listdir
from os.path import isfile, join
import datetime




currentDateTime = datetime.datetime.now()
cwd = os.getcwd()
mypath = cwd + "/static/img/"
DB_LOCATION = cwd + "/newBlogPost.db"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

conn = sqlite3.connect(DB_LOCATION, check_same_thread=False)
cur = conn.cursor()


app = Flask(__name__)
app.secret_key = "edeb8273e8ae2cb527a22ab5e18f1292"

@app.route("/authorize/blogPost/member/login", methods=["POST"])
def login():
    username = request.form["email"]
    password = request.form["password"]
    db_email = cur.execute("SELECT * from users WHERE email = ? AND password = ? ;", (username, password,)).fetchone()
    if db_email is None:
        msg = "Login Failed: Information Invalid".title()
        flash(msg, 'danger')
        return redirect(url_for('index'))

    elif username == db_email[3] and password == db_email[4]:
        session["username"] = db_email[1]
        print(session["username"])
        r = make_response(redirect(url_for('index')))
        r.set_cookie('memberCheck', 'True')
        return r


@app.route("/becoming-member/new-user/singing-up", methods=["POST"])
def signup():
    name     = request.form["name"]
    username = request.form["username"]
    email    = request.form["email"]
    password = request.form["password"]
    
    db_information = cur.execute("SELECT username, email FROM users WHERE username=? OR email=?", (username, email,)).fetchone()
    if db_information is None:
        cur.execute("INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)", (name, username, email, password,))
        conn.commit()
        #conn.close()
        msg = "You've Signed Up Successfully. You can now Login.".title()
        flash(msg, "success")
        return redirect(url_for('index'))

    elif db_information[0] == username or db_information[1] == email:
        flash("User Account With This Information Already Exists. Try Again With Different Username or Password.", "danger")
        return redirect(url_for("index"))
    

@app.route("/")
def index():
    memberCheck = request.cookies.get('memberCheck')
    if memberCheck == "True":
        value = "<script>$('#loginModal').modal('show');</script>"
    else:
        value = "<script>$('#signupModal').modal('show');</script>"
    print("COOKIE_VALUE: %s" % (memberCheck))
    blogs = cur.execute("SELECT * FROM blogposts;").fetchall()
    return render_template("index.html", memberCheck=value, blogs=blogs)


@app.route("/BlogPost/articales/makePost", methods=["POST"])
@app.route("/articles/Posting-New-Articale/", methods=["GET", "POST"])
def postingNewArticale():
    try:
        ErrorMsg = "You Don't Have Sufficient Access To Perform This Action. (Note: This Incident Has Recorded/Logged.)"
        if session["username"] == "rhenry":
            if request.method == "POST":
                title      = request.form["title"]
                SubHeading = request.form["SubHeading"]
                blogPost   = request.form["blogPost"]
                postDateTime = currentDateTime.strftime("%a, %b %d, %Y At %I:%M:%S %p")
                image = "/static/img/" + random.choice(onlyfiles)
                cur.execute("INSERT INTO blogPosts (author, title, subHeading, blogPost, dateTime, image) VALUES (?, ?, ?, ?, ?, ?, ?)", (session["username"], title, SubHeading, blogPost, postDateTime, image,))
                conn.commit()
                
                msg = "New Articale Has Been Added Successfully."
                flash(msg, "success")
                return redirect(url_for('index'))        

            return render_template("postingNewArticle.html")
        
        flash(ErrorMsg, "danger")
        return redirect(url_for('index'))

    except KeyError:
        flash(ErrorMsg, "danger")
        return redirect(url_for('index'))


@app.route("/articales/posted/<string:id>", methods=["GET"])
def articales(id):
    if session:
        data       = cur.execute("SELECT * FROM blogPosts WHERE id=?", (id,)).fetchone()
        articleID  = data[0]
        title      = data[2]
        SubHeading = data[3]
        blogPost   = data[4]
        author     = data[1]
        postDateTime = data[5]
        image = data[6]
        #commentsText = cur.execute("SELECT * FROM comments WHERE articale_id= ?;", (id,)).fetchall()
        commentsText = cur.execute("SELECT users.username, comments.comment_text, comments.comment_dateTime FROM users LEFT JOIN comments ON comments.user_id = users.id WHERE comments.articale_id= ? ORDER BY comments.id DESC;", (id,)).fetchall()
        print(commentsText)
        return render_template("articales.html", data=data, commentsText=commentsText)

    msg = "Sorry You Need To Be Logged In To View Full BlogPost."
    flash(msg, "danger")
    return redirect(url_for("index"))


@app.route("/Authorized/Member/Make/Comment/Articale", methods=["POST", "GET"])
def makeComment():
    CommentError = "Your Comment Was Not Made Due To Bad Authentication (Try Logging In Again, and Then Make a Comment)."

    try:
        if session["username"]:
            userID    = cur.execute("SELECT id FROM users WHERE name=?", (session["username"],)).fetchone()[0]
            articleID = request.form["articaleID"]
            print("USER ID : " + str(userID))
            comment   = request.form["commentText"]
            print("\
            Articale ID: %s\
            Users    ID: %s\
            CommentText: %s\
            " % (articleID, userID, comment))
            if len(comment) > 5:    
                cur.execute("INSERT INTO comments (user_id, comment_text, articale_id, comment_dateTime) VALUES (?, ?, ?, ?);", (userID, comment, articleID, currentDateTime,))
                conn.commit()
            else:
                flash("Comment Invalid, Try Again With a Longer/Valid Comment of more than 5 characters.", "danger")
                return redirect(url_for("articales", id=articleID))

            msg = "Sucess! Your Comment Has Been Saved Successfuly!"
            flash(msg, "success")
            return redirect(url_for("articales", id=articleID))
        
        flash(CommentError, "danger")
        return redirect(url_for("index"))

    except KeyError:
        flash(CommentError, "danger")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    #app.secret_key = "os.urandom(4096)"
    app.run()
    
