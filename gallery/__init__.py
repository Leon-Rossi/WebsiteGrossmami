import os

from flask import Flask, redirect, render_template, url_for


def create_app():
    # create and configure the app
    app = Flask(__name__, static_url_path="/static", instance_relative_config=True)

    @app.route("/")
    def home():
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
