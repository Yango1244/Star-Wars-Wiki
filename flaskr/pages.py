from flask import render_template
from flask import session
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from flaskr.backend import Backend
from flaskr.models import User
from flaskr.models import Users

from fileinput import filename
from flask import request


def make_endpoints(app, login_manager):
    global_test = Backend()
    users = Users()

    #./run-flask.sh

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("main.html")

    @app.route("/pages")
    def pages():

        files, page_names = global_test.get_all_page_names()

        result = {page_names[i]: files[i] for i in range(len(page_names))}

        return render_template("pages.html", result=result)

    @app.route('/pages/<filename>')
    def pages_redirect(filename):
        file = global_test.get_wiki_page(filename)
        display = file.download_as_string().decode('utf-8')
        return render_template('display.html', display=display)

    @app.route("/about")
    def about():
        authors = [
            "Oluwayimika Adeyemi", "Lerone Joyner",
            "Emilio Tadeo de la Rocha Galan", "Daniel Marin"
        ]
        urls = [x for x in authors]
        iters = len(authors)
        back = Backend()

        for i in range(0, iters):
            name = authors[i].replace(" ", "")
            name += ".jpg"
            urls[i] = (back.get_image(name))

        return render_template("about.html",
                               authors=authors,
                               urls=urls,
                               iters=iters)

    @app.route("/profiles")
    def profiles():
        users = global_test.get_users()
        result = {users[i]: users[i] for i in range(len(users))}
        return render_template("profiles.html", result=result)

    @app.route("/profiles/<username>")
    def user_profile(username):
        users = global_test.get_users()
        if username not in users:
            return render_template("invalid_user.html")

        photourl = global_test.get_profile_pic(username)
        bannerurl = global_test.get_banner_pic(username)
        bio = global_test.get_bio(username)
        result = {
            "username": username,
            "photourl": photourl,
            "banner": bannerurl,
            "bio": bio
        }
        return render_template("profile.html", result=result)

    @app.route("/upload")
    @login_required
    def upload():
        return render_template("upload.html")

    @app.route('/upload/upload_submit', methods=['POST'])
    def upload_submit():
        back = Backend()
        if request.method == 'POST':
            f = request.files['file']
            result = back.upload(f.filename, f)

            if result == "Success":
                return render_template("upload_success.html")

            elif result == "Failure":
                return render_template("upload_failure.html")

    @app.route("/signup")
    def signup():
        return render_template("signup.html", failure=False)

    @app.route("/signup/validate", methods=['POST'])
    def signup_validate():
        if request.method == 'POST':
            form_username = request.form.get("username")
            form_password = request.form.get("password")
            valid = global_test.sign_up(form_username, form_password)

            if valid:
                users.add_user_from_id(form_username)
                user = load_user(form_username)
                login_user(user)
                user.authenticate()
                return render_template("signup_success.html")

            return render_template("signup.html", failure=True)

    @app.route("/login")
    def login():
        return render_template("login.html", failure=False)

    @app.route("/login/validate", methods=['POST'])
    def login_validate():
        if request.method == 'POST':
            form_username = request.form.get("username")
            session['username'] = form_username
            form_password = request.form.get("password")
            valid = global_test.sign_in(form_username, form_password)

            if valid:
                users.add_user_from_id(form_username)
                user = load_user(form_username)
                login_user(user)
                user.authenticate()
                return render_template("login_success.html",
                                       username=form_username)

            return render_template("login.html", failure=True)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return render_template("main.html")

    @login_manager.user_loader
    def load_user(user_id):
        return users.get_user(user_id)

    @app.route("/edit_profile")
    @login_required
    def edit_profile():
        return render_template('edit_profile.html')

    @app.route("/edit_profile/submit", methods=['POST'])
    def submit_profile():
        if request.method == 'POST':
            username = session["username"]
            new_pass = request.form.get("new_password")
            profile_pic = request.files['profile_pic']
            banner_pic = request.files['banner_pic']
            bio = request.form.get("bio")

            result = global_test.change_profile(username, new_pass,
                                                profile_pic.filename,
                                                profile_pic,
                                                banner_pic.filename, banner_pic,
                                                bio)

            if result == "Success":
                return render_template("edit_success.html")

            elif result == "Failure":
                return render_template("edit_failure.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.
