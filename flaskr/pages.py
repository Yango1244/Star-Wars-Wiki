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
            
            
    

        

    # TODO(Project 1): Implement additional routes according to the project requirements.
