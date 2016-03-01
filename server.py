# Import pyscopg2 libraries.
import psycopg2
import psycopg2.extras
# Import operating system module.
import os

# Import class called "Flask"
#from flask import Flask, render_template
from flask import Flask, render_template, session
#import socketio
from flask.ext.socketio import SocketIO, emit
# Create 'app' object.  Name is a built-in environment variable that refers to scope.
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

# Create socketio app.
socketio = SocketIO(app)

# Define database connection method.
def connectToDB():
    connectionString = 'dbname=garage user=limited password=limited762* host=localhost'
    # connectionString = 'dbname=garage user=postgres password=postgres host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")


# Decorator.  When a socket connect event happens, do this.
@socketio.on('connect', namespace='/gg')
def makeConnection():
    # Print debug message.
    print('connected')



# A python decorator.  Whenever route('/') run the layout/index webpage.
@app.route('/')
def mainIndex():
    
    print 'in hello world'
    return render_template('index.html')
    #return app.send_static_file('index.html')
    
# A python decorator.  Display the register content page.
@app.route('/register')
def registerPage():

    return render_template('register.html')
    #return app.send_static_file('index.html')

# Start the server.  Main method.  
if __name__ == '__main__':
    # Use the IP address for host.  If not present, use 0.0.0.0.
    # Use the PORT address.  If not present, use 8080.
    #app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)