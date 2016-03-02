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

# Decorator.  When a socket registration event happens, do this.
@socketio.on('register', namespace='/gg')
def register(data):
    
    # Grab all the values and verify they are received.
    localAvatar = data[0];
    localFirstName = data[1];
    localLastName = data[2];
    localPass = data[3];
    localRetyped = data[4];

    print "New username to register is: %s" % localAvatar
    print "New firstname to register is: %s" % localFirstName
    print "New lastname to register is: %s" % localLastName
    #print "New password is: %s" % localPass
    #print "Retyped password is: %s" % localRetyped
    
    # Find out if the passwords match.
    if localPass == localRetyped:
        
        # Connect to the database.
        conn = connectToDB()
        # Create a database cursor object (dictionary style).
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Find out from the database if the username is already taken.
        try:
            cur.execute("SELECT * FROM users WHERE username = %s;", (localAvatar,))
        except:
            print("Error executing SELECT for username lookup.")
        answer=cur.fetchall()
            
        # Find out if the result set is empty.
        count=0
        for row in answer:
            count = count + 1
            
        if count > 0:
            status = 'Username already exists.'
            emit('status', status)
        else:
            # Go ahead and register the new user.
            try:
                print(cur.mogrify("INSERT INTO users (username, firstname, lastname, password) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')));", (localAvatar, localFirstName, localLastName, localPass)))
                cur.execute("INSERT INTO users (username, firstname, lastname, password) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')));", (localAvatar, localFirstName, localLastName, localPass))
            except:
                print("Error executing INSERT for new registered user.")
                conn.rollback()
            conn.commit()
      
            # Test
            print("You successfull registered!")
            status = "You sucessfully registered!"
            emit('status', status)

    else:
        # Test
        print("Passwords do not match.")
        status = 'Passwords do not match.'
        emit('status', status) 




# Start the server.  Main method.  
if __name__ == '__main__':
    # Use the IP address for host.  If not present, use 0.0.0.0.
    # Use the PORT address.  If not present, use 8080.
    #app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)