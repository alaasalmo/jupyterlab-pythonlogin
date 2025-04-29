from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import psycopg2
import os



app = Flask(__name__)
app.view_functions.clear()

def getURL(tokenpath,HOSTNAME,PORT):
    with open(tokenpath, 'r') as file:
        TOKEN = file.read().strip()
        app.secret_key = TOKEN 
        JUPYTER_URL = f"http://{HOSTNAME}:{PORT}?token=" + str(TOKEN)
    return JUPYTER_URL




##os.environ['SESSION'] ="2"
##os.environ['MINIKUBE_IP'] ="172.28.176.130"
##os.environ['JUPYTERPORT']="30088"
##os.environ['POSTGRES_DB'] ="jupyterlabdb"
##os.environ['POSTGRES_USER'] ="admin"
##os.environ['POSTGRES_PASSWORD'] ="admin"
##os.environ['POSTGRES_PORT']="30432"
##os.environ['SESSION']="5"

HOSTNAME=str(os.getenv('MINIKUBE_IP'))
PORT=str(os.getenv('JUPYTERPORT'))
MINUTEINSESSION=os.getenv('SESSION')
if MINUTEINSESSION==None or MINUTEINSESSION=="":
    MINUTEINSESSION = 5
else:
    MINUTEINSESSION = int(os.getenv('SESSION'))

DBHOSTNAME="postgresql-service"
DATABASE=os.getenv('POSTGRES_DB')
DBPORT=os.getenv('POSTGRES_PORT')
DBUSERNAME=os.getenv('POSTGRES_USER')
DBPASSWORD=os.getenv('POSTGRES_PASSWORD')
tokenpath="/notebook/"+"token.file"

with open(tokenpath, 'r') as file:
    TOKEN = file.read()
    app.secret_key = TOKEN.replace("\n","")

# check username & password function
def checkuser(name: str, passw: str):

    conn = psycopg2.connect(
    host=DBHOSTNAME,  # Node IP or Minikube IP
    port=DBPORT,             # NodePort from your Service
    database=DATABASE,
    user=DBUSERNAME,
    password=DBPASSWORD
    )


    cur = conn.cursor()
    s=f"SELECT * FROM USERS WHERE username='{name}' and password='{passw}'"
    cur.execute(s)
    user = cur.fetchone()

    if user!=None:
        return True
    else: 
        return False
    cur.close()

# Set session lifetime (5 minutes)
app.permanent_session_lifetime = timedelta(minutes=MINUTEINSESSION)

@app.route("/", methods=["GET", "POST"])
def login():

    if "user" in session:  # Ensure the user is logged in
        return redirect(url_for("dashboard"))  # Redirect to the dashboard

    if request.method == "POST":
    ##    # Get data from login form
        username = request.form["username"]
        password = request.form["password"]
         
    ##    # Check if username and password are valid
    ##    #if username == VALID_USERNAME and password == VALID_PASSWORD:
        if (checkuser(username,password)):   
            # Store the username in the session
            session["user"] = username
            session.permanent = True  # Enable session expiration time
            return redirect(url_for("dashboard"))
        return "Invalid credentials, please try again."

    return '''
    <form method="post">
    <p><b>Login page</b></p>
    <table border=0>
     <tr><td colspan=2><br></td></tr>
     <tr>
      <td> <label>Username:</label></td>
      <td> <input type="text" name="username"></td>
     </tr> 
     <tr> 
      <td><label>Password:</label></td> 
      <td><input type="password" name="password"></td>
     </tr>
     <tr><td colspan=2><br></td></tr>
     <tr>
       <td colspan=2 align='center'><input type="submit" value="Login"></td>
     </tr>
    </form> '''

@app.route("/dashboard")
def dashboard():
    if "user" in session:  # Check if user is logged in
        JUPYTER_URL=getURL(tokenpath, HOSTNAME, PORT)
        return redirect(JUPYTER_URL)
    else:
        return redirect(url_for("login"))  # Redirect to login if not logged in

@app.route("/jupyter")
def jupyter_redirect():
    if "user" in session:  # Ensure the user is logged in
        JUPYTER_URL=getURL(tokenpath, HOSTNAME, PORT)
        return redirect(JUPYTER_URL)  # Redirect to JupyterLab
    else:
        return redirect(url_for("login"))  # Redirect to login if not logged in

@app.route("/logout")
def logout():
    session.pop("user", None)  # Remove user from session
    return redirect(url_for("login"))  # Redirect to login page after logout

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
