from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/links')
def links():
    return render_template('links.html')

'''
@app.route('/test')
def test():
    return render_template("home.html")
'''

if __name__ == "__main__":
    app.run()
