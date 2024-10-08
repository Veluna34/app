from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def signin():
    return render_template("signInPage.html")

@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html')

@app.route('/signIn')
def signIn():
    return render_template('signIn.html')

@app.route('/homepage', methods=['POST'])
def homePage():
    # Here you can handle the form submission (e.g., create the account)
    
    # After processing, redirect to homepage
    return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')