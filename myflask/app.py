from flask import Flask, abort, render_template, session, url_for, redirect,request #import Flask class, other modules can go here

app = Flask(__name__) #we create an instance of this class, Flask uses this to look for resources like static files or templates
app.secret_key = "supersecretkey"  # Required for session handling

# @app.route("/") #this is the root directory of the app, route is called a decorator
# def hello_world(): #this is a function that returns something to this route, it can be anything served as well
#     return "<p>Hello, World!</p>" + ("Hi again!")

@app.route("/")
def index():
    title = "The best page ever!"
    return render_template("index.html", title=title)

# @app.route("/login")
# def home():
#     """Display username if logged in, otherwise show 'Not logged in'."""
#     if 'username' in session:
#         return f"Hello, {session['username']}!"
#     return "Not logged in"

@app.route("/about")
def about():
    names = ["Jos", "Mary", "Tim"]
    return render_template("about.html", names=names)

#example of a page which can be a form
#you can add an HTTP method such as post for data
#there are request and response objects in flask
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route('/')
def home():
    """Display username if logged in, otherwise show 'Not logged in'."""
    if 'username' in session:
        return f"Hello, {session['username']}!"
    return "Not logged in"

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render login form if not logged in. Redirect to home if logged in."""
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:  # Reject empty usernames
            abort(403)  # 403 Forbidden

        session['username'] = username  # Store username in session
        return redirect(url_for('home'))

    return '''
        <form method="post">
            <label>Username:</label>
            <input type="text" name="username" required>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/logout')
def logout():
    """Logs out the user and redirects to the login page."""
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return "<h1>404 Not Found</h1><p>The page you are looking for does not exist.</p>", 404

@app.errorhandler(403)
def forbidden(e):
    """Custom 403 Forbidden error for empty username."""
    return "<h1>403 Forbidden</h1><p>Username cannot be empty.</p>", 403

if __name__ == "__main__":
    app.run(debug=True)
