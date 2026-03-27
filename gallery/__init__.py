from flask import Flask, redirect, url_for, render_template
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_url_path="/static", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "gallery.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    @app.route("/")
    def home():
        return os.listdir("./gallery/static/gallery")
        return redirect(url_for("person"))

    @app.route("/person")
    def person():
        return render_template("person.html")

    @app.route("/kontakt")
    def kontakt():
        return render_template("kontakt.html")

    @app.route("/kurse")
    def kurse():
        return render_template("kurse.html")

    @app.route("/werke")
    def werkeMain():
        filenames = listCategories()
        filepaths = firstImageInCategoriesPaths(filenames)
        files = zip(filepaths, filenames)
        print(files)
        return render_template("galleryMain.html", files=files)

    @app.route("/werke/<category>")
    def werke(category):
        filepaths = filepathsInCategory(category)
        filenames = filenamesFromPaths(filepaths)
        files = zip(filepaths, filenames)
        print(files)
        return render_template("werke.html", category=category, files=files)

    return app


def listCategories():
    path = "./gallery/static/gallery"
    categories = os.listdir(path)

    return categories


def firstImageInCategoriesPaths(names):
    filepaths = []
    for name in names:
        path = "./gallery/static/gallery/" + name
        shortenedPath = "gallery/" + name
        filepaths.append(os.path.join(shortenedPath, os.listdir(path)[0]))

    return filepaths


def filepathsInCategory(name):
    path = "./gallery/static/gallery/" + name
    shortenedPath = "gallery/" + name
    filepaths = []
    for filename in os.listdir(path):
        filepaths.append(os.path.join(shortenedPath, filename))

    return filepaths


def filenamesFromPaths(filepaths):
    filenames = []
    for path in filepaths:
        name = path[path.find("/", 8) + 1 :]
        name = name[: name.find(".")]
        name = name.replace("-", " ")
        filenames.append(name)

    return filenames
