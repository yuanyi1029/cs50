# Import Flask function, render_template function and request variable
from flask import Flask, render_template, request

# Use Flask() function to turn current file name into a flask application
app = Flask(__name__)


# Execute the index function when a user visits the default address ('/')
# Return the contents of index.html using the render_template() function
# request.args.get is a function that gets the value of the key value pair arguments from the URL,
# "world" value will be used if "name" key is not found
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        return render_template("greet.html", name=request.form.get("name","world"))
