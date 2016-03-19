# Import pyscopg2 libraries.
import psycopg2
import psycopg2.extras
# Import operating system module.
import os

# Import class called "Flask"
#from flask import Flask, render_template
from flask import Flask, render_template, session, request
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
    
    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    #Find out from the database if the username is already taken.
    try:
        cur.execute("SELECT games.title, gamedetails.gdesc FROM games NATURAL JOIN gamedetails;")
    except:
        print("Error executing SELECT for username lookup.")
    games=cur.fetchall()
        
    # test
    """
    for entry in games:
        temptitle = entry.get('title')
        tempdesc = entry.get('gdesc')
        print "Title: %s" % temptitle
        print "Description: %s" % tempdesc
        print "\n"
    """
            
    print 'in hello world'
    
    if 'userName' in session:
        tempName=session['userName']
        # Capitalize the name for HTML print.
        newName = tempName.capitalize()
        print "(Root) Logged in user is: %s" % newName
    else:
        newName = ''
        print "(Root) No one is logged in."
    name = [newName]    
    return render_template('index.html', sessionUser=name, games=games, selected = 'home')
    #return render_template('index-backup.html', sessionUser=name)
    #return app.send_static_file('index-backup.html')

# A python decorator.  Whenever '/allgames' run the 'displaygames' webpage.
@app.route('/allgames')
def displayAllGames():
    
    if 'userName' in session:
        tempName=session['userName']
        # Capitalize the name for HTML print.
        newName = tempName.capitalize()
        print "(Register) Logged in user is: %s" % newName
    else:
        tempName = ''
        newName = ''
        print "(Register) No one is logged in."
        
    # original username
    originalname = [tempName]
    # capitalized username
    name = [newName]
    
    # Search for all games.
    searchtype = 'all'
    
    return render_template('displaygames.html', originalUser=originalname, sessionUser=name, games=searchtype, selected = 'allgames')
    #return render_template('index-backup.html', sessionUser=name)
    #return app.send_static_file('index-backup.html')

# Decorator.  When a game search request happens, do this.
@socketio.on('searchtype', namespace='/gg')
def findGames(searchtype):
    
    # Grab all the values and verify they are received.
    localSearchType = searchtype

    print "Game search type is: %s" % localSearchType

    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    if localSearchType == 'all':
        
        # Get data for all games.
        try:
            cur.execute("SELECT * FROM games NATURAL JOIN gamedetails;")
            #cur.execute("SELECT games.title, gamedetails.gdesc FROM games NATURAL JOIN gamedetails;")
        except:
            print("Error executing SELECT for all games lookup.")
        games=cur.fetchall()
        
        gamesResult = []
        
        
        for entry in games:
            # Test
            #temptitle = entry.get('title')
            #localprice = entry.get('price')
            #tempdesc = entry.get('gdesc')
            #print "Title: %s" % temptitle
            #print "TEST: Game price is: %s" % localprice
            #print "Description: %s" % tempdesc
            #print "\n"
            
            # Grab the price (in decimal).
            decimalprice = entry.get('price')
            # Convert the price to a string.
            stringprice = str(decimalprice)
            # Add the $ character.
            finalprice = '$' + stringprice
            
            #Grab the discount price (in decimal).
            decimaldiscount = entry.get('discountprice')
            # Convert the discout price to a string.
            stringdiscount = str(decimaldiscount)
            # Add the $ character.
            finaldiscount = '$' + stringdiscount

            
            game = {'gid': entry.get('gid'), 'title': entry.get('title'), 'price': finalprice, 'discountprice': finaldiscount, 'desc': entry.get('gdesc')}
            #game = {'gid': entry.get('gid'), 'title': entry.get('title'), 'desc': entry.get('gdesc')}
            gamesResult.append(game)
            
        # Test
        for entry2 in gamesResult:
            tempid = entry2.get('gid')
            temptitle = entry2.get('title')
            tempprice = entry2.get('price')
            tempdiscount = entry2.get('discountprice')
            tempdesc = entry2.get('desc')
            print "Game ID: %s" % tempid
            print "Title: %s" % temptitle
            print "Price: %s" % tempprice
            print "Discount Price: %s" % tempdiscount
            print "Description: %s" % tempdesc
            print "\n"
            
        # Test
        print("You successfull retreived all games!")
        emit('gamesResult', gamesResult)


# Decorator.  When a socket add-to-cart event happens, do this.
@socketio.on('addtocart', namespace='/gg')
def addtocart(cartdata):
    
    # Grab all the values and verify they are received.
    localName = cartdata[0];
    localGameID = cartdata[1];

    print "Logged in user's name: %s" % localName
    print "Game ID to add to user's cart: %s" % localGameID
    
    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    # Get the logged in user's userid.
    try:
        cur.execute("SELECT userid FROM users WHERE username = %s;", (localName,))
    except:
        print("Error executing SELECT for username lookup.")
    answer=cur.fetchall()
           
    # Find out if the result set is empty.
    count=0
    for row in answer:
        count = count + 1
            
    if count == 0:
            status = 'Username does not exist.'

    # Get the userid.
    for entry in answer:
        localUserID = entry.get('userid')
        print 'Userid is: %s' % localUserID
        
    # Attempt to add the game to the user's userlibrary.
    try:
        print(cur.mogrify("INSERT INTO userlibrary (gid, userid) VALUES (%s, %s);", (localGameID, localUserID)))
        cur.execute("INSERT INTO userlibrary (gid, userid) VALUES (%s, %s);", (localGameID, localUserID))
    except:
        print("Error executing UPDATE for userlibrary.")
        conn.rollback()
    conn.commit()
    
    
    
# A python decorator.  Display the register content page.
@app.route('/register')
def registerPage():

    if 'userName' in session:
        tempName=session['userName']
        # Capitalize the name for HTML print.
        newName = tempName.capitalize()
        print "(Register) Logged in user is: %s" % newName
    else:
        newName = ''
        print "(Register) No one is logged in."
    
    name = [newName]
    return render_template('register.html', sessionUser=name, selected = 'register')
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


# A python decorator.  Login.
@app.route('/login', methods=['GET', 'POST'])
def loginEvaluate():
    
    if request.method == 'POST':
        
        # Connect to the database.
        conn = connectToDB()
        # Create a database cursor object (dictionary style).
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        #Find out from the database if the username is already taken.
        
        # **************Getting games for  front page here.  Will remove when frontpage is restored/replaced **************
        try:
            cur.execute("SELECT games.title, gamedetails.gdesc FROM games NATURAL JOIN gamedetails;")
        except:
            print("Error executing SELECT for username lookup.")
        games=cur.fetchall()
    
    
        # Grab the credentials.
        localName = request.form['username']
        localPass = request.form['password']
    
        # Debug message.
        print "Username is: %s" % localName
        #print "Password is: %s" % localPass
    
        if localName != '':
            if localPass != '':

                # Verify that the username and password match a user entry in the database.
                try:
                    # print(cur.mogrify("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password);", (tempUser, tempPassword)))
                    cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password);", (localName, localPass))
                except:
                    print("Error executing SELECT for user lookup.")
                answer=cur.fetchall()
            
                # Find out if the result set is empty.
                count=0
                for row in answer:
                    count = count + 1
        
                # Set the session variables, if user entry found, and log them in.
                if count == 1:
                    print("TEST: Found the username/password in the database!")
        
                    # Set the session variables.
                    session['userName'] = localName
                    session['userPassword'] = localPass
                    # Capitalize the name for HTML print.
                    newName = localName.capitalize()
                    name = [newName]
                    return render_template('index.html', sessionUser=name, games=games, selected = 'home')
            
                elif count == 0:
                    # For anyone already logged in on this machine, log them out.
                    if 'userName' in session:
                        del session['userName']
                        del session['userPassword']
                        
                    print("Failed to log in.")
                    #emit('loggedinStatus', failed)
                    name = ['']
                return render_template('index.html', sessionUser=name, games=games, selected = 'home')
            else:
                # For anyone already logged in on this machine, log them out.
                if 'userName' in session:
                    del session['userName']
                    del session['userPassword']
                name = ['']
                return render_template('index.html', sessionUser=name, games=games, selected = 'home')
        else:
            # For anyone already logged in on this machine, log them out.
            if 'userName' in session:
                del session['userName']
                del session['userPassword']
            name = ['']
            return render_template('index.html', sessionUser=name, games=games, selected = 'home')

# A python decorator.  Login.
@app.route('/logout', methods=['GET', 'POST'])
def logoutEvaluate():
    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT games.title, gamedetails.gdesc FROM games NATURAL JOIN gamedetails;")
    except:
        print("Error executing SELECT for username lookup.")
    games=cur.fetchall()
    
    # For anyone already logged in on this machine, log them out.
    if 'userName' in session:
        del session['userName']
        del session['userPassword']
        name = ['']
        return render_template('index.html', sessionUser=name, games=games, selected = 'home')

@app.route('/checkout', methods=['GET', 'POST'])
def Checkout():
    cartdict = []
    pricedict = 0
    
    if (request.method == 'POST' or request.method == 'GET'):
            # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                print(cur.mogrify(("SELECT SUM(price) FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = 3;")))
                
                cur.execute("SELECT title FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = 3;")
                cur2.execute("SELECT SUM(price) FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = 3;")
                cartdict = cur.fetchall()
                pricedict = cur2.fetchall()
                cart = []
                price = 0
                
                for game in cartdict:
                    cart.append(game.get('title'))
                for total in pricedict:
                    price = total.get('sum')
            except:
                print("Error selecting from library.")
            name = ['']    
            
    tempName=session['userName']
    newName = tempName.capitalize()
    name = [newName]
    return render_template('checkout.html', cart=cart, price = price, sessionUser = name, selected = 'checkout')
            


@app.route('/checkout2', methods = ['GET', 'POST'])
def Check_Complete():
        
        if request.method == 'POST':
            
	
		    # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print("I'm printing something")
            try:
               print(cur.mogrify(("INSERT INTO creditcards (userid, ccnumber, cccode, exp_month, expyear) VALUES (2,%s,%s,%s,%d);", (request.form['ccnumber'], request.form['cccode']
                , request.form['expmonth'], request.form['expyear']))))
                #cur.execute("INSERT INTO creditcards (user_id, cc_number, cc_code, exp_month, exp_year) VALUES (2,12345,333,June,2014);", (request.form['cc_number'], request.form['cc_code']
                #, request.form['exp_month'], request.form['exp_year']))
                #cur.execute("INSERT INTO userlibrary VALUES (1,1,TRUE);")
                
                #cur.execute()
                
                #answer=cur.fetchall()
            except:
                print("Error executing updating game library.")
            print("I printed something")
        name = ['']
        return render_template('checkout2.html', sessionUser = name, selected = 'checkout')   

@app.route('/changeInfo')
def changeInfo():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    tempName=session['userName']
    newName = tempName.capitalize()
    name = [newName]
    try:
        cur.execute("select username, firstname, lastname, password from users WHERE username= '%s'" % (tempName))
    except:
        print("ERROR inserting from the wall")
        conn.rollback()
    conn.commit()
    results = cur.fetchall()
    return render_template('changeInfo.html', sessionUser=name, info=results, selected = 'changeinfo')
    #return app.send_static_file('index.html')





# Start the server.  Main method.  
if __name__ == '__main__':
    # Use the IP address for host.  If not present, use 0.0.0.0.
    # Use the PORT address.  If not present, use 8080.
    #app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)