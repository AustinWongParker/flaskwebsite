# Austin Wong-Parker
# Flask Website main program

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__) # app is an instance of the flask class.

@app.route('/') # route decorator tells flask which URL to go through.
def home():
    try:
        return render_template('home.html')
    except Exception:
        return str(e)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/contact')
def contact():
    return redirect('https://www.linkedin.com/in/a-w-p/')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/blog')
def links():
    return render_template('blog.html')

@app.route('/gaming')
def gaming():
    return render_template('gaming.html')

'''
@app.route('/test')
def test():
    return render_template("home.html")
'''

'''
# Error handler
@app.errorhandler(404)
def page_not_found:
    return make_response(render_template("404.html"), 404)
'''

if __name__ == "__main__":
    app.run()
    #app.run(debug=True) # uncomment for debugging
