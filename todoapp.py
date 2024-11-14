from flask import Flask, render_template, redirect, request
import re
import pickle

app = Flask(__name__)

todos = []
error = None
firstRun = True


@app.route("/")
def hello_world():
    global todos, firstRun
    if firstRun:
        firstRun = False
        try:
            with open("todolist.pkl", "rb") as f:
                todos = pickle.load(f)
        except:
            print("Error loading To Do List")
            return render_template("index.html", todos=todos, error=error)

    return render_template("index.html", todos=todos, error=error)


@app.route("/submit", methods=["POST"])
def submit():
    global error
    task = request.form["task"]
    email = request.form["email"]
    priority = request.form["priority"]
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not task:
        error = "Invalid Task. Please make sure the task field is not empty."
    elif not re.match(email_pattern, email):
        error = (
            "Invalid Email address. Please make sure to enter a valid email address."
        )
    elif priority == "":
        error = "Invalid Priority. Please make sure to pick a priority level."
    else:
        error = None
        todos.append((task, email, priority.capitalize()))
        print("Task successfully added!")

    return redirect("/")


@app.route("/clear")
def clear():
    global todos
    todos = []
    print("Task list cleared!")
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    id = int(request.form["id"])
    del todos[id]
    print("Task successfully deleted")
    return redirect("/")


@app.route("/save", methods=["POST"])
def save():
    global todos
    try:
        with open("todolist.pkl", "wb") as f:
            pickle.dump(todos, f)
        print("Task list successfully saved!")
        f.close()
    except:
        f.close()
        print("Error saving To Do List")
        return redirect("/")
    return redirect("/")


if __name__ == "__main__":
    app.run()
