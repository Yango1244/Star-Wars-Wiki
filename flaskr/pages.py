from flask import render_template

from flaskr.backend import Backend


def make_endpoints(app):

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
        test = Backend()
        page_names = test.get_all_page_names()

        return render_template("pages.html",page_names = page_names)
    @app.route("/about")
    def about():
        return render_template("about.html")
    

        

    # TODO(Project 1): Implement additional routes according to the project requirements.
