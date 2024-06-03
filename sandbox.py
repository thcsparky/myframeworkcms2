from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os 
import time

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_pyfile(r'C:\Users\spark\OneDrive\Documents\coding\python\tay\madeaconfig.py')
socketio = SocketIO(app)

# Dictionary to store the timestamps of the last login attempts for each IP address
login_attempts = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index2.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(data):
    print(data)  # devmessage
    if 'gethomepanel' in data:
        with open('./static/filds/homepanel.html', 'r') as files:
            homepanelstring = files.read()
            socketio.emit('response', homepanelstring) 
    if 'getmenupanel' in data:
        with open('./static/filds/menupanel.html', 'r') as files2:
            menupanelstring = files2.read()
            socketio.emit('menupanel_response', menupanelstring)  
    if 'geteventspanel' in data:
        with open('./static/filds/eventspanel.html', 'r') as files3:
            eventspanelstring = files3.read()
            socketio.emit('eventspanel_response', eventspanelstring)
    if 'getcontactspanel' in data:
        with open('./static/filds/contactspanel.html', 'r') as files4:
            contactspanelstring = files4.read()
            socketio.emit('contactspanel_response', contactspanelstring)
            
    if 'getallpanels' in data: 
        filestring = []
        #create a list of paths
        sp = './static/filds/'
        spa = sp + 'homepanel.html'
        filestring.append(spa)
        spa = sp + 'menupanel.html'
        filestring.append(spa)
        spa = sp + 'eventspanel.html'
        filestring.append(spa)
        spa = sp + 'contactspanel.html'
        filestring.append(spa)
        spa = sp + 'picturespanel.html'
        filestring.append(spa)

        #load files into a list of data
        datastring = []
        for filepath in filestring:
            with open(filepath, 'r') as f:
                datastring.append(f.read())

        # Join the contents of the files with the delimiter "::"
        joined_content = "::".join(datastring)

        socketio.emit('returnpanels', joined_content)



    if 'getpicturespanel' in data:
        with open('./static/filds/picturespanel.html', 'r') as files5:
            picturesfilestring = files5.read()
            socketio.emit('picturespanel_response', picturesfilestring)
    if 'getloginmessage:' in data:
        try:
            split_data = data.split(',mid.')
            username = split_data[0].split('loginmessage:')[1]
            password = split_data[1].split(',ip.')[0]
            userip = split_data[1].split(',ip.')[1]
            loginitem = trylogin(username, password, userip)
            if loginitem == "RATE_LIMITED":
                socketio.emit('rate_limit_response', "You are rate-limited. Please try again later.")
                print('ratelimitONE')
            elif loginitem == "WRONG_PASSWORD":
                socketio.emit('wrong_password_response', "Incorrect password. Please try again.")
                print('wrongpasswordONE')
            elif loginitem == "CORRECT_PASSWORD":
                socketio.emit('correct_password_response', "Login successful.")
                print('correctpasswordONE')
        except Exception as E:
            print(E)

def openstring(dirfrommain):
    thisdir = './' + dirfrommain 
    with open(thisdir, 'r') as t:
        f = t.read()
        return f 
    
def savestring(dirfrommain, stringhere):
    thisdir = './' + dirfrommain
    with open(thisdir, 'w') as fileout:
        fileout.write(stringhere)

def listToString(list):
    stringout = ''
    for x in list:
        stringout += x + '\n'
    return(stringout)

def trylogin(username, password, userip):
    global login_attempts
    sn = username
    pw = password
    ip = userip 

    if ip in login_attempts:
        last_attempt_time = login_attempts[ip]
        if time.time() - last_attempt_time < 30:
            print('ratelimitTWO')
            return "RATE_LIMITED"
    
    # Record the current login attempt time
    login_attempts[ip] = time.time()

    serverlogstring1 = 'Attempted login from: ' + ip + '\n'
    serverlogstring1 += sn + ":" + pw 
    print(serverlogstring1)

    loginstuff = openstring('static/loginstuff.txt')
    loginstufflist = loginstuff.splitlines()
    
    loginstufflist.append(ip + ":attemptedtologin")
    loginstuff = listToString(loginstufflist)
    savestring('static/loginstuff.txt', loginstuff)

    pws = openstring('static/hi234235252352345.pws')
    rightsn = pws.split(':')[0]
    rightpw = pws.split(':')[1]
    if sn == rightsn and pw == rightpw:
        print('correctpasswordTWO')
        return "CORRECT_PASSWORD" ## make sure to verify some way other in the program too
    else:
        failurestring = ip + ':'  + str(int(time.time()))
        fedit = openstring('static/loginstuff.txt')
        fedit += failurestring + '\n' 
        savestring('static/loginstuff.txt', fedit)
        print('wrongpasswordTWO')
        return "WRONG_PASSWORD"

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000)
