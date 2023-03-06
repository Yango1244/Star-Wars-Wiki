from flask import render_template
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
    @app.route("/main")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")
    
    @app.route("/pages")
    def pages():
        
        page_names = global_test.get_all_page_names()

        return render_template("pages.html",page_names = page_names)

    @app.route('/pages/<filename>')
    def pages_redirect(filename):
        file = global_test.get_wiki_page(filename)
        display = file.download_as_string().decode('utf-8')
        return render_template('display.html',display = display)
        

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/upload")
    @login_required
    def upload():
        return render_template("upload.html")

    @app.route('/success', methods = ['POST'])
    def upload_success():
        back = Backend()
        if request.method == 'POST':  
            f = request.files['file']
            f.save(f.filename)
            result = back.upload(f.filename)

            if result == "Success":
                return render_template("upload_success.html")

    @app.route("/signup")
    def signup():
        return render_template("signup.html", failure = False)
        
    @app.route("/signup/validate", methods = ['POST'])
    def signup_validate():
        if request.method == 'POST':
            form_username = request.form.get("username")
            form_password = request.form.get("password")
            valid = global_test.sign_up(form_username, form_password)

            if valid:
                return render_template("signup_success.html")
            
            return render_template("signup.html", failure = True)

    @app.route("/login")
    def login():
        return render_template("login.html", failure = False)        
            
    @app.route("/login/validate", methods = ['POST'])
    def login_validate():
        if request.method == 'POST':
            form_username = request.form.get("username")
            form_password = request.form.get("password")
            valid = global_test.sign_in(form_username, form_password)

            if valid:
                users.add_user_from_id(form_username)
                user = load_user(form_username)
                login_user(user)
                user.authenticate()
                return render_template("login_success.html", username = form_username)
            
            return render_template("signup.html", failure = True)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return render_template("main.html")

    @login_manager.user_loader
    def load_user(user_id):
        return users.get_user(user_id)
        

    # TODO(Project 1): Implement additional routes according to the project requirements.
