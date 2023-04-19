from flask import render_template, send_file
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
        character_names = global_test.get_character_names()
        return render_template("main.html",character_names = character_names)

    @app.route("/pages")
    def pages():

        files, page_names = global_test.get_all_page_names()

        result = {page_names[i]: files[i] for i in range(len(page_names))}

        return render_template("pages.html", result=result)

    @app.route('/pages/<filename>')
    def pages_redirect(filename):
        print('enter')
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

    @app.route("/character_profile<name>")
    def character_profiles(name):
        name_passed = str()
        name = name.lower()
        good_name = list([val for val in name if val.isalpha()])
        
        result = "".join(good_name)
        #List of lists of dictionaries
        global_people = global_test.request_maker()
        #Returns a dictionary with the correct character information
        person_info, name_passed = global_test.get_info(global_people,result)
        #Simplified logic
        if person_info and name_passed:
            return render_template('character_profile.html',person_info = person_info,name_passed = name_passed)
        else:
            return "That character doesn't exist"

    @app.route("/images/<image>")
    def images(image):
        """Returns the image from backend.get_image."""
        return send_file(global_test.get_character_image(image), mimetype='image/png')

