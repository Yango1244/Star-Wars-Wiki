from flask import render_template

from flaskr.backend import Backend

from fileinput import filename
from flask import request


def make_endpoints(app):
    global_test = Backend()

    #./run-flask.sh

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    @app.route("/home")
    def home():
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
        authors = ["Oluwayimika Adeyemi", "Lerone Joyner"]
        urls = [x for x in authors]
        iters = len(authors)
        back = Backend()
        
        for i in range(0, iters):
            name = authors[i].replace(" ","")
            name += ".jpg"
            urls[i] = (back.get_image(name))

        
        return render_template("about.html", authors = authors, urls = urls, iters = iters)

    @app.route("/upload")
    def upload():
        return render_template("upload.html")

    @app.route('/upload/upload_submit', methods = ['POST'])
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
                return render_template("login_success.html", username = form_username)
            
            return render_template("signup.html", failure = True)

        

    # TODO(Project 1): Implement additional routes according to the project requirements.
