# Import pyscopg2 libraries.
import psycopg2
import psycopg2.extras
# Import operating system module.
import os

# Import time module.
import time

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

# Global flag for game sale price reset.
resetFlag=0

#@app.before_first_request
# Runs before EACH request.
@app.before_request
def resetgamesonsale():
    
    # Change the time zone to Eastern Standard Time.
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()
    
    day = time.strftime('%A')
    print 'DAY: %s' % day

    global resetFlag
    # If today is NOT reset day, reset the global to zero.
    # if day != 'Saturday'
    if day != 'Sunday':
        resetFlag == 0
        print('Sorry, today is not reset day.')

        # If today is reset day, only run reset once.  
        # elif day == 'Saturday':
    elif day == 'Sunday':      
        
        localFlag = resetFlag
        
        if localFlag == 0:
            print 'resetFlag is: %s' % resetFlag
            print 'Today is %s.  You are executing the reset method.' % day
            
            # If today is Sunday:
            # 1. Reset all games to retail price.
            # 2. Grab the top 3 voted games.
            # 3. Set the top 3 voted games on discount.
            # 4. Reset the top 3 games voted for discount, by setting 1 vote to all games.
    
            # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
            # 1. Reset all games to retail price.
            try:
              print(cur.mogrify("UPDATE games SET onsale = %s;", (False,)))
              cur.execute("UPDATE games SET onsale = %s;", (False,))
            except:
                print('Could not wipe all games of discount price flag.')
                conn.rollback()
            conn.commit()
    
             #  2. Get top 3 voted games.
            try:
                print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
                cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
            except:
                print('Could not SELECT top 3 voted games.')
            votedgames = cur.fetchall()    
    
            # 3. Set the top 3 voted games on discount.
    
            for game in votedgames:
                tempName = game.get('title')
                print 'Game name: %s' % tempName
    
                try:
                    print(cur.mogrify("UPDATE games SET onsale = %s WHERE title = %s;", (True, tempName)))
                    cur.execute("UPDATE games SET onsale = %s WHERE title = %s;", (True, tempName))
                except:
                    print('Could not set game to discount price.')
                    conn.rollback()
                conn.commit()
                
            # 4. Reset the top 3 games voted for discount, by setting 1 vote to all games.
             
            try:
                print(cur.mogrify("UPDATE gamedetails SET votes = %s;", (1,)))
                cur.execute("UPDATE gamedetails SET votes = %s;", (1,))
            except:
                print('Could not reset all game votes.')
                conn.rollback()
            conn.commit()
            
            resetFlag = 1
            print 'resetFlag is now: %s' % resetFlag

        else:
            print 'resetFlag is: %s' % resetFlag

# Decorator.  When a socket connect event happens, do this.
@socketio.on('connect', namespace='/gg')
def makeConnection():
    # Print debug message.
    print('connected')
    

        
         
 
# A python decorator.  Whenever route('/') run the layout/index webpage.
@app.route('/')
def mainIndex():
    
    print 'in hello world'
    
    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Get top 3 voted games.
    try:
        print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
        cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")

    except:
        print('Could not SELECT top 3 voted games.')
    votedgames = cur.fetchall()
    
    # TEST
    # print('Printing top 3 voted games.')
    # for game in votedgames:
    #     print(game)
    
    # Get top 3 user blog data.
    try:
        print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
        cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
    except:
        print('Could not SELECT top 3 comments.')
    topcomments = cur.fetchall() 
 
    
    if 'userName' in session:
        tempName=session['userName']
        avatarValue=session['avatarpath']
        
        # Capitalize the name for HTML print.
        newName = tempName.capitalize()
        print "(Root) Logged in user is: %s" % newName
    else:
        newName = ''
        avatarValue = ''
        print "(Root) No one is logged in."
    name = [newName]    
    return render_template('index.html', sessionUser=name, avatarValue=avatarValue, votedgames = votedgames, topcomments=topcomments, selected = 'home')


# A python decorator.  Whenever '/allgames' run the 'displaygames' webpage.
@app.route('/allgames')
def displayAllGames():

    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
        cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")

    except:
        print('Could not SELECT top 3 voted games.')
    votedgames = cur.fetchall()
    
    # Get top 3 user blog data.
    try:
        print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
        cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
    except:
        print('Could not SELECT top 3 comments.')
    topcomments = cur.fetchall() 
    
    if 'userName' in session:
        tempName=session['userName']
        avatarValue=session['avatarpath']
        # Capitalize the name for HTML print.
        newName = tempName.capitalize()
        print "(Register) Logged in user is: %s" % newName
    else:
        tempName = ''
        newName = ''
        avatarValue= ''
        print "(Register) No one is logged in."
        
    # original username
    originalname = [tempName]
    # capitalized username
    name = [newName]
    
    # Search for all games.
    searchtype = 'all'
    
    return render_template('displaygames.html', originalUser=originalname, avatarValue=avatarValue, votedgames = votedgames, topcomments=topcomments, sessionUser=name, games=searchtype, selected = 'allgames')


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
            cur.execute("SELECT * FROM games NATURAL JOIN gamedetails ORDER BY gid;")
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
            
            finalprice = ''
            # Grab the onsale value.
            onsale = entry.get('onsale')
            print "Onsale value is: %s" % onsale
            if onsale == False:
                # Grab the price (in decimal).
                decimalprice = entry.get('price')
                # Convert the price to a string.
                stringprice = str(decimalprice)
                # Add the $ character.
                finalprice = 'Price $' + stringprice
            
            elif onsale == True:
                #Grab the discount price (in decimal).
                decimaldiscount = entry.get('discountprice')
                # Convert the discout price to a string.
                stringdiscount = str(decimaldiscount)
                # Add the $ character.
                finalprice = 'Sale Price $' + stringdiscount

            
            game = {'gid': entry.get('gid'), 'title': entry.get('title'), 'price': finalprice, 'desc': entry.get('gdesc'), 'artpath': entry.get('artpath')}
            #game = {'gid': entry.get('gid'), 'title': entry.get('title'), 'desc': entry.get('gdesc')}
            gamesResult.append(game)
            
        # Test
        for entry2 in gamesResult:
            tempid = entry2.get('gid')
            temptitle = entry2.get('title')
            tempprice = entry2.get('price')
            #tempdiscount = entry2.get('discountprice')
            tempdesc = entry2.get('desc')
            temppath = entry2.get('artpath')
            print "Game ID: %s" % tempid
            print "Title: %s" % temptitle
            print "Price: %s" % tempprice
            #print "Discount Price: %s" % tempdiscount
            print "Cover art path: %s" % temppath
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
    pageposition = cartdata[2];

    print "Logged in user's name: %s" % localName
    print "Game ID to add to user's cart: %s" % localGameID
    print "Position of game on inventory page: %s" % pageposition
    
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
        
    # Find out if the game is already in the user's cart.
    try:
        print(cur.mogrify("SELECT * FROM userlibrary WHERE gid = %s AND userid = %s;", (localGameID, localUserID)))
        cur.execute("SELECT * FROM userlibrary WHERE gid = %s AND userid = %s;", (localGameID, localUserID))
    except:
        print("Error searching for game in userlibrary.")
    duplicategames = cur.fetchall()

    # Find out if the result set is empty.
    gamecount=0
    for gamerow in duplicategames:
        gamecount = gamecount + 1
    
    # Declare empty string for gamestatus just in case it never gets set.
    gamestatus = ''
    
    if gamecount > 0:
            for game in duplicategames:
                localpurchase = game.get('purchasedstatus')
                if localpurchase == True:
                    gamestatus = 'Game already purchased.'
                else:
                    gamestatus = 'Game already in cart.'
            print(gamestatus)
    else:
        # Attempt to add the game to the user's userlibrary.
        try:
            print(cur.mogrify("INSERT INTO userlibrary (gid, userid) VALUES (%s, %s);", (localGameID, localUserID)))
            cur.execute("INSERT INTO userlibrary (gid, userid) VALUES (%s, %s);", (localGameID, localUserID))
        except:
            print("Error executing UPDATE for userlibrary.")
            conn.rollback()
        conn.commit()
        gamestatus = 'Added game to cart!'
        print(gamestatus)
        
    gameinfo = {'pageposition': pageposition, 'gamestatus': gamestatus}
    emit('gameinfo', gameinfo)
    

    
    
    
# A python decorator.  Display the register content page.
@app.route('/register')
def registerPage():

    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
        cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")

    except:
        print('Could not SELECT top 3 voted games.')
    votedgames = cur.fetchall()
    
    # Get top 3 user blog data.
    try:
        print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
        cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
    except:
        print('Could not SELECT top 3 comments.')
    topcomments = cur.fetchall() 
    
    if 'userName' in session:
        tempName=session['userName']
        avatarValue = session['avatarpath']
        # Capitalize the name for HTML print.
        newName = tempName.capitalize()
        print "(Register) Logged in user is: %s" % newName
    else:
        newName = ''
        avatarValue = ''
        print "(Register) No one is logged in."
    
    name = [newName]
    return render_template('register.html', sessionUser=name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'register')
    #return app.send_static_file('index.html')

# Decorator.  When a socket registration event happens, do this.
@socketio.on('register', namespace='/gg')
def register(data):
    
    # Grab all the values and verify they are received.
    localUser = data[0];
    localFirstName = data[1];
    localLastName = data[2];
    localPass = data[3];
    localRetyped = data[4];
    localAvatar = data[5];

    print "New username to register is: %s" % localUser
    print "New firstname to register is: %s" % localFirstName
    print "New lastname to register is: %s" % localLastName
    print "New avatar to register is: %s" % localAvatar
    
    if localAvatar == 'babyMario':
        localPath = "avatars/m1.jpg"    
    if localAvatar == 'jumpingMario':
        localPath = "avatars/m2.jpg" 
    if localAvatar == 'flyingMario':
        localPath = "avatars/m3.jpg" 
    if localAvatar == '':
        localPath = "NONE"        

    # print "New path to register is: %s" % localPath
    #print "New password is: %s" % localPass
    #print "Retyped password is: %s" % localRetyped
    # Find out if the passwords match.
    
    if localPath == "NONE":
        status = 'Please choose an avatar.'
        emit('status', status) 
        
    else:
        if localPass == localRetyped:
        
        # Connect to the database.
            conn = connectToDB()
        # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Find out from the database if the username is already taken.
            try:
                cur.execute("SELECT * FROM users WHERE username = %s;", (localUser,))
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
                    print(cur.mogrify("INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);", (localUser, localFirstName, localLastName, localPass, localPath)))
                    cur.execute("INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);", (localUser, localFirstName, localLastName, localPass, localPath))
                except:
                    print("Error executing INSERT for new registered user.")
                    conn.rollback()
                conn.commit()
          
                # Test
                print("You successfull registered!")
                status = "You sucessfully registered!"
                emit('status', status)


# A python decorator.  Login.
@app.route('/login', methods=['GET', 'POST'])
def loginEvaluate():
    
    if request.method == 'POST':
        
        # Connect to the database.
        conn = connectToDB()
        # Create a database cursor object (dictionary style).
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        # Get top 3 voted games.
        try:
            print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
            cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
    
        except:
            print('Could not SELECT top 3 voted games.')
        votedgames = cur.fetchall()
        
        # TEST
        # print('Printing top 3 voted games.')
        # for game in votedgames:
        #     print(game)
        
        # Get top 3 user blog data.
        try:
            print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
            cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
        except:
            print('Could not SELECT top 3 comments.')
        topcomments = cur.fetchall() 
    
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

                for entry in answer:
                    avatarValue=entry.get('avatarpath')                       
        
                # Set the session variables, if user entry found, and log them in.
                if count == 1:
                    print("TEST: Found the username/password in the database!")
        
                    # Set the session variables.
                    session['userName'] = localName
                    session['userPassword'] = localPass
                    session['avatarpath'] = avatarValue

                    # Capitalize the name for HTML print.
                    newName = localName.capitalize()
                    name = [newName]
                    return render_template('index.html', sessionUser=name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'home')
            
                elif count == 0:
                    # For anyone already logged in on this machine, log them out.
                    if 'userName' in session:
                        del session['userName']
                        del session['userPassword']
                        del session['avatarpath']

                    print("Failed to log in.")
                    #emit('loggedinStatus', failed)
                    name = ['']
                    avatarValue=''
                return render_template('index.html', sessionUser=name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'home')
            else:
                # For anyone already logged in on this machine, log them out.
                if 'userName' in session:
                    del session['userName']
                    del session['userPassword']
                    del session['avatarpath']

                name = ['']
                avatarValue=''
                return render_template('index.html', sessionUser=name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'home')
        else:
            # For anyone already logged in on this machine, log them out.
            if 'userName' in session:
                del session['userName']
                del session['userPassword']
                del session['avatarpath']

            name = ['']
            avatarValue=''
            return render_template('index.html', sessionUser=name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'home')

# A python decorator.  Logout.
@app.route('/logout', methods=['GET', 'POST'])
def logoutEvaluate():
    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Get top 3 voted games.
    try:
        print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
        cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")

    except:
        print('Could not SELECT top 3 voted games.')
    votedgames = cur.fetchall()
 
    # Get top 3 user blog data.
    try:
        print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
        cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
    except:
        print('Could not SELECT top 3 comments.')
    topcomments = cur.fetchall()   
    
    
    
    # For anyone already logged in on this machine, log them out.
    if 'userName' in session:
        del session['userName']
        del session['userPassword']
        del session['avatarpath']

        name = ['']
        return render_template('index.html', sessionUser=name, votedgames=votedgames, topcomments=topcomments, selected = 'home')


# A python decorator for a logged in user to purchase games in their shopping cart.
@app.route('/checkout', methods=['GET', 'POST'])
def Checkout():
    cartdict = []
    pricedict = 0
    
    if (request.method == 'POST' or request.method == 'GET'):
        
        if 'userName' in session:
            localName=session['userName']
            avatarValue=session['avatarpath']
            
            # Capitalize the name for HTML print.
            newName = localName.capitalize()
            # Add the capitalized name to a list.
            name = [newName]
        
        # Connect to the database.
        conn = connectToDB()
        # Create a database cursor object (dictionary style).
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
        # Grab the top 3 voted games.
        try:
            print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
            cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
    
        except:
            print('Could not SELECT top 3 voted games.')
        votedgames = cur.fetchall()    
   
        # Get top 3 user blog data.
        try:
            print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
            cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
        except:
            print('Could not SELECT top 3 comments.')
        topcomments = cur.fetchall()  

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
        
        # Grab all the games in this user's cart that are NOT already purchased.
        try:
            print(cur.mogrify("SELECT * FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = %s AND purchasedstatus  = %s;", (localUserID, False)))
            cur.execute("SELECT * FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = %s AND purchasedstatus  = %s;", (localUserID, False))
        except:
            print("Error selecting games from this user's cart.")
        cartdict = cur.fetchall()
        # test
        #print cartdict
        
        # Variable to track subtotal price of games in cart.
        finalprice = 0.00
        # List of dictionaries to gather data for each game.
        gamesList = []
        # Game count.
        cartSize = 0
        # Get the price of each game and subtotal the game prices.
        for entry in cartdict:
            cartSize = cartSize + 1
            
            onsaleflag = entry.get('onsale')
            
            if onsaleflag == False:
                gameprice = float(entry.get('price'))
                # Convert the price to a string.
                stringprice = str(gameprice)
                if stringprice == '0.0':
                    stringprice = '0.00'
                pricedesc = 'Price: $' + stringprice
            elif onsaleflag == True:
                gameprice = float(entry.get('discountprice'))
                # Convert the price to a string.
                stringprice = str(gameprice)
                if stringprice == '0.0':
                    stringprice = '0.00'
                pricedesc = 'Sale Price: $' + stringprice
                
            # TEST
            print('TEST')
            print 'Title: %s' % entry.get('title')
            print(pricedesc)
   
            # Now add the game to the gamesList.
            game = {'title': entry.get('title'), 'pricedesc': pricedesc}
            gamesList.append(game)

            # Aggregate the subtotal price.
            finalprice = finalprice + gameprice
        
        # TEST
        print '\nTEST: Final Price: %s' % finalprice
            
        # Change the time zone to Eastern Standard Time.
        os.environ['TZ'] = 'US/Eastern'
        time.tzset()

        # Grab the day of the week and the time.
        #weekDay = time.strftime('%A')
        today = time.asctime(time.localtime(time.time()))
        print '\nTEST: Today is: %s' % today
        fullMonth = time.strftime('%B')
        currentMonth = str(fullMonth)
        print 'TEST: Current month is: %s' % fullMonth
        tempDigitMonth = time.strftime('%m')
        digitMonth = int(tempDigitMonth)
        print 'TEST: Current month as integer is: %s' % digitMonth
        tempYear = time.strftime('%G')
        fullYear = int(tempYear)
        print 'TEST: Current year is: %s' % fullYear
        

        # Find out if the user has NO credit card OR if the credit card is expired.
        try:
            print(cur.mogrify("SELECT expmonth, expyear FROM creditcards WHERE userid = %s;", (localUserID,)))
            cur.execute("SELECT expmonth, expyear FROM creditcards WHERE userid = %s;", (localUserID,))
        except:
            print('Could not execute credit card search for this logged in  user.')
        ccresult = cur.fetchall()

        count2=0
        for entry2 in ccresult:
            count2 = count2 + 1
        
        # Declare credit card status variables.
        ccstatus = 'true'
        ccmessage = 'An unexpired credit card is on file.'
        
        # Does the user have a credit card?
        if count2 == 0:
            ccstatus = 'false'
            ccmessage = 'No credit card on file.  Please register a credit card.'
            print('TEST: User has no credit card!')
        elif count2 == 1:
            print('TEST: User has exactly 1 credit card!')
            
            # Variable to grab user's cc expmonth
            expMonth = 0
            # Variable to grab user's cc expyear
            expYear = 0
            
            # Compare the month and year on the credit card to today's month and year.
            for cc in ccresult:
                bigExpMonth = cc.get('expmonth')
                tempExpMonth = bigExpMonth.lower()
                print'TEST: Credit card expiration month is: %s' % bigExpMonth
                if tempExpMonth == 'january':
                    expMonth = 1
                elif tempExpMonth == 'february':
                    expMonth = 2
                elif tempExpMonth == 'march':
                    expMonth = 3
                elif tempExpMonth == 'april':
                    expMonth = 4
                elif tempExpMonth == 'may':
                    expMonth = 5
                elif tempExpMonth == 'june':
                    expMonth = 6
                elif tempExpMonth == 'july':
                    expMonth = 7
                elif tempExpMonth == 'august':
                    expMonth = 8
                elif tempExpMonth == 'september':
                    expMonth = 9
                elif tempExpMonth == 'october':
                    expMonth = 10
                elif tempExpMonth == 'november':
                    expMonth = 11
                elif tempExpMonth == 'december':
                    expMonth = 12
                
                expYear = cc.get('expyear')
                
            print 'TEST: Credit card expiration month is: %s' % expMonth
            print 'TEST: Credit card expiration year is: %s' % expYear
               
            print 'TEST: current year is: %s' % fullYear
            print 'TEST: cc expyear is: %s' % expYear
            
            # Compare the user's cc expmonth and expyear to today's month and year.
            if expYear < fullYear:
                ccstatus = 'expired'
                ccmessage = 'Your credit card expiration year is exceeded.  Please update your credit card information.'
            elif expYear == fullYear:
                if expMonth < digitMonth:
                    ccstatus = 'expired'
                    ccmessage = 'Your credit card expiration month is exceeded.  Please update your credit card information.'

        # TEST
        print('\nCredit card status is:')
        print(ccstatus)
        print('Credit card message is:')
        print(ccmessage)

        print 'cartSize is: %s' % cartSize
        
        return render_template('checkout.html', cartSize=cartSize, cart=gamesList, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, price=finalprice, ccstatus=ccstatus, ccmessage=ccmessage, currentmonth = digitMonth, currentyear = fullYear, sessionUser=name, selected='checkout')

# Decorator.  When a socket credit card update event happens, do this.
@socketio.on('updatecc', namespace='/gg')
def updatecc(newccinfo):
    
    # Grab all the values and verify they are received.
    localccnum = newccinfo[0];
    localcccode = newccinfo[1];
    localexpmonth = newccinfo[2];
    localintexpyear = newccinfo[3];
    
    localmonth=''
    
    # Convert the month to text.
    if localexpmonth == '1':
        localmonth = 'January'
    elif localexpmonth == '2':
        localmonth = 'February'
    elif localexpmonth == '3':
        localmonth = 'March'
    elif localexpmonth == '4':
        localmonth = 'April'
    elif localexpmonth == '5':
        localmonth = 'May'
    elif localexpmonth == '6':
        localmonth = 'June'
    elif localexpmonth == '7':
        localmonth = 'July'
    elif localexpmonth == '8':
        localmonth = 'August'
    elif localexpmonth == '9':
        localmonth = 'September'
    elif localexpmonth == '10':
        localmonth = 'October'
    elif localexpmonth == '11':
        localmonth = 'November'
    elif localexpmonth == '12':
        localmonth = 'December'

    print "New ccnum is: %s" % localccnum
    print "New cccode is: %s" % localcccode
    print "New expmonth is: %s" % localmonth
    print "New expyear is: %s" % localintexpyear
    
    if 'userName' in session:
        localName=session['userName']
        avatarValue=session['avatarpath']
        # Capitalize the name for HTML print.
        newName = localName.capitalize()
        # Add the capitalized name to a list.
        name = [newName]
        
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
       
    # Now find if the user already has a credit card.
    try:
        cur.execute("SELECT * FROM creditcards WHERE userid = %s;", (localUserID,))
    except:
        print("Error attempting to SELECT logged in user's credit card info.")
    ccanswer = cur.fetchall()
    
    # Find out if the result set = 1.
    counttwo = 0
    for entry in ccanswer:
        counttwo = counttwo + 1
    
    # Update the credit card, if it exists.
    if counttwo == 1:
        try:
            print(cur.mogrify("UPDATE creditcards SET ccnumber = crypt('%s', gen_salt('bf')), cccode = crypt('%s', gen_salt('bf')), expmonth = %s, expyear = %s WHERE userid = %s;", (localccnum, localcccode, localmonth, localintexpyear, localUserID)))
            cur.execute("UPDATE creditcards SET ccnumber = crypt('%s', gen_salt('bf')), cccode = crypt('%s', gen_salt('bf')), expmonth = %s, expyear = %s WHERE userid = %s;", (localccnum, localcccode, localmonth, localintexpyear, localUserID))
            
            updatestatus = 'Successfully updated credit card.'
        except:
            print("Error attempting to update logged in user's credit card.")
            updatestatus = 'Failed to update credit card.'
            conn.rollback()
        conn.commit()
        
        emit('updatestatus', updatestatus) 
        
    elif counttwo == 0:
        # Add a NEW credit card.
        try:
            print(cur.mogrify("INSERT INTO creditcards (userid, ccnumber, cccode, expmonth, expyear) VALUES (%s, crypt('%s', gen_salt('bf')), crypt('%s', gen_salt('bf')), %s, %s);", (localUserID, localccnum, localcccode, localmonth, localintexpyear)))
            cur.execute("INSERT INTO creditcards (userid, ccnumber, cccode, expmonth, expyear) VALUES (%s, crypt('%s', gen_salt('bf')), crypt('%s', gen_salt('bf')), %s, %s);", (localUserID, localccnum, localcccode, localmonth, localintexpyear))

            updatestatus = 'Successfully added credit card.'
        except:
            print("Error attempting to add new credit card.")
            updatestatus = 'Failed to add new credit card.'
            conn.rollback()
            
        conn.commit()
        
        emit('updatestatus', updatestatus)
        

@app.route('/checkout2', methods = ['GET', 'POST'])
def Check_Complete():
        
        if request.method == 'POST':
            
            print('TEST: Inside checkout2 POST')
            
            # Grab the cartcount and print it.
            localCartCount = request.form['cartcount']
            print 'localCartCartCount: %s' % localCartCount
            
            if 'userName' in session:
                localName=session['userName']
                avatarValue=session['avatarpath']
                # Capitalize the name for HTML print.
                newName = localName.capitalize()
                # Add the capitalized name to a list.
                name = [newName]
        
            # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
          
            # Grab the top 3 voted games.
            try:
                print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
                cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
        
            except:
                print('Could not SELECT top 3 voted games.')
            votedgames = cur.fetchall()          
          
            # Get top 3 user blog data.
            try:
                print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
                cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
            except:
                print('Could not SELECT top 3 comments.')
            topcomments = cur.fetchall()        
            
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
               
            # Now flip all the games in the user's cart to PURCHASED.
            try:
                print(cur.mogrify("UPDATE userlibrary SET purchasedstatus = %s WHERE userid = %s;", (True, localUserID)))
                cur.execute("UPDATE userlibrary SET purchasedstatus = %s WHERE userid = %s;", (True, localUserID))
            except:
                print("Error update inventory games to purchased.")
                conn.rollback()
            conn.commit()

            originalname = [localName]
            return render_template('checkout2.html', originalUser=originalname, sessionUser = name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'checkout', cartcount = localCartCount)   


@socketio.on('deletecart', namespace='/gg')
def deletecart(name):
    print 'TEST: Inside deletecart socketio method.  Logged in user is: %s' % name

    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if 'userName' in session:
        localName=session['userName']
        avatarValue=session['avatarpath']
        
    try:
        cur.execute("SELECT * FROM users WHERE username = %s;", (localName,))
    except:
        print("Error executing SELECT for username lookup.")
    answer=cur.fetchall()
    
    # Find out if the result set is empty.
    count=0
    for row in answer:
        count = count + 1
    
    if count == 0:
        print 'Username does not exist.'
    elif count == 1:    
    
        # Get the userid.
        for entry in answer:
            localUserID = entry.get('userid')
            print 'UserID is: %s' % localUserID
    
        # Now try to delete all games that are flagged as in the cart (NOT purchased)
        try:
            print(cur.mogrify("DELETE FROM userlibrary WHERE userid = %s AND purchasedstatus = %s;", (localUserID, False)))
            cur.execute("DELETE FROM userlibrary WHERE userid = %s AND purchasedstatus = %s;", (localUserID, False))
        except:
            print("Error executing DELETE for all games in user's cart.")
            conn.rollback()
        conn.commit()
    
        deletestatus = 'Your cart is now empty.'
        emit('deletestatus', deletestatus)
    
    
@app.route('/changeInfo')
def changeInfo():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Grab the top 3 voted games.
    try:
        print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
        cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
    except:
        print('Could not SELECT top 3 voted games.')
    votedgames = cur.fetchall()
    
    # Get top 3 user blog data.
    try:
        print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
        cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
    except:
        print('Could not SELECT top 3 comments.')
    topcomments = cur.fetchall() 
    
    if 'userName' in session:
        tempName=session['userName']
        # Capitalize the name for HTML print.
        avatarValue=session['avatarpath']
        newName = tempName.capitalize()
        print "(Register) Logged in user is: %s" % newName
    else:
        print("OOPS")
        
        tempName = ''
        newName = ''
        avatarValue = ''
        print "(Register) No one is logged in."    
    
    tempName=session['userName']
    newName = tempName.capitalize()
    name = [newName]
    try:
        cur.execute("SELECT username, firstname, lastname, password, favgame, favgenre from users WHERE username= '%s'" % (tempName))
    except:
        print("ERROR")
        conn.rollback()
    conn.commit()
    results = cur.fetchall()
    return render_template('changeInfo.html', sessionUser=name, info=results, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'changeinfo')
    #return app.send_static_file('index.html')

@app.route('/updateinformation', methods=['GET', 'POST'])
def updateinformation():
    if (request.method == 'POST' or request.method == 'GET'):
            
            currentname=session['userName']
            # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
            # Grab the top 3 voted games.
            try:
                print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
                cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
        
            except:
                print('Could not SELECT top 3 voted games.')
            votedgames = cur.fetchall()
    
            # Get top 3 user blog data.
            try:
                print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
                cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
            except:
                print('Could not SELECT top 3 comments.')
            topcomments = cur.fetchall() 
    
            try:
                newusername = request.form['username']
                newfirst = request.form['firstname']
                newlast = request.form['lastname']
                newgenre = request.form['favgenre']
                newgame = request.form['favgame']
                newpass = request.form['newpassword']
                newpassretype = request.form['retypedpassword']
                
                # print(newpass)
                # print(cur.mogrify("UPDATE users SET avatarpath = '%s' WHERE username= '%s'" % (newavatar, tempName))
                if newfirst != '': 
                    cur.execute("UPDATE users SET firstname = '%s' WHERE username= '%s'" % (newfirst, currentname))
                if newlast != '': 
                    cur.execute("UPDATE users SET lastname = '%s' WHERE username= '%s'" % (newlast, currentname))                    
                if newgenre != '': 
                    cur.execute("UPDATE users SET favgenre = '%s' WHERE username= '%s'" % (newgenre, currentname))
                if newgame != '': 
                    cur.execute("UPDATE users SET favgame = '%s' WHERE username= '%s'" % (newgame, currentname))
                if newpass != '':
                    # if newpassretype == newpass:
                    cur.execute("UPDATE users SET password = crypt('%s', gen_salt('bf')) WHERE username= '%s'" % (newpass, currentname))
                print(newpass)
                print(newpassretype)

                # cur.execute("INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s);", (localUser, localFirstName, localLastName, localPass, localPath))

            # cur.execute("INSERT INTO userlibrary (gid, userid) VALUES (%s, %s);", (localGameID, localUserID))
            
            except:
                print("Error updating Information.")
                conn.rollback()
            conn.commit()
    avatarValue=session['avatarpath']
    tempName=session['userName']
    newName = tempName.capitalize()
    name = [newName]
    return render_template('updateinformation.html', sessionUser=name, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, selected = 'updateinformation')
    #return app.send_static_file('index.html')
    
@app.route('/updatecreditcard', methods=['GET', 'POST'])
def updatecreditcard():
    cartdict = []
    pricedict = 0
    
    if (request.method == 'POST' or request.method == 'GET'):
            # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Grab the top 3 voted games.
            try:
                print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
                cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
        
            except:
                print('Could not SELECT top 3 voted games.')
            votedgames = cur.fetchall()
            
            # Get top 3 user blog data.
            try:
                print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
                cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
            except:
                print('Could not SELECT top 3 comments.')
            topcomments = cur.fetchall()             
            
            
            cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                print(cur.mogrify(("SELECT SUM(price) FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = 3;")))
                
                cur.execute("SELECT title FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = 3;")
                cur2.execute("SELECT SUM(price) FROM games JOIN userlibrary ON games.gid = userlibrary.gid WHERE userid = 3;")
                cartdict = cur.fetchall()
                pricedict = cur2.fetchall()
                cart = []
                price = 0
            except:
                print("Error selecting from library.")
            name = ['']    
    avatarValue=session['avatarpath']
    tempName=session['userName']
    newName = tempName.capitalize()
    name = [newName]
    return render_template('updatecreditcard.html', cart=cart, price = price, avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, sessionUser = name, selected = 'updatecreditcard')
            
@app.route('/updateavatar', methods=['GET', 'POST'])
def updateavatar():
    if (request.method == 'POST' or request.method == 'GET'):
            # Connect to the database.
            conn = connectToDB()
            # Create a database cursor object (dictionary style).
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Grab the top 3 voted games.
            try:
                print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
                cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
        
            except:
                print('Could not SELECT top 3 voted games.')
            votedgames = cur.fetchall()
            
            # Get top 3 user blog data.
            try:
                print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
                cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
            except:
                print('Could not SELECT top 3 comments.')
            topcomments = cur.fetchall() 
            
            tempName=session['userName']
            try:
                newavatar = request.form['avatar']
                print(tempName)
                print(newavatar)
                # print(cur.mogrify("UPDATE users SET avatarpath = '%s' WHERE username= '%s'" % (newavatar, tempName))
                session['avatarpath']=newavatar
                cur.execute("UPDATE users SET avatarpath = '%s' WHERE username= '%s'" % (newavatar, tempName))
            # cur.execute("INSERT INTO userlibrary (gid, userid) VALUES (%s, %s);", (localGameID, localUserID))
            
            except:
                print("Error updating Avatar.")
                conn.rollback()
            conn.commit()
    avatarValue=session['avatarpath']
    tempName=session['userName']
    newName = tempName.capitalize()
    name = [newName]
    return render_template('updateavatar.html', avatarValue=avatarValue, votedgames=votedgames, topcomments=topcomments, sessionUser = name, selected = 'updateavatar')


# Update the database vote count and post the user's comment to the mini-blog.
@socketio.on('voteList', namespace='/gg')
def vote(voteList):
    user = voteList[0];
    favorite = voteList[1];
    comment = voteList[2];
    color = voteList[3];

    print('Received voting data:')
    print 'user: %s' % user
    print 'favorite: %s' % favorite
    print 'comment: %s' % comment
    print 'color: %s' % color
    
    # Change the time zone to Eastern Standard Time.
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()

    # Grab the numerical day of the week.
    day = time.strftime('%e')
    actualday = int(day)
    # Grab the abbreviated month.
    actualmonth = time.strftime('%b')
    # Grab the year.
    year = time.strftime('%Y')
    actualyear = int(year)
    
    # TEST
    print 'Day of the week: %s' % actualday
    print 'Abbreviated Month: %s' % actualmonth
    print 'Year: %s' % actualyear
    

    
    # Connect to the database.
    conn = connectToDB()
    # Create a database cursor object (dictionary style).
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Get the logged in user's userid.
    try:
        cur.execute("SELECT userid FROM users WHERE username = %s;", (user,))
    except:
        print("Error executing SELECT for username lookup.")
    usans=cur.fetchall()
           
    # Find out if the result set is empty.
    countu=0
    for row in usans:
        countu = countu + 1
            
    if countu == 0:
        print('Username does not exist.')

    if countu == 1:
        # Get the userid.
        for entry in usans:
            localUserID = entry.get('userid')
            print 'Userid is: %s' % localUserID    
    
        # Get the game id.
        try:
            print(cur.mogrify("SELECT gid FROM games WHERE title = %s;", (favorite,)))
            cur.execute("SELECT gid FROM games WHERE title = %s;", (favorite,))
        except:   
            print('Could not SELECT game id.')
        answer = cur.fetchall()
    
        # Find out if the result set is empty.
        count=0
        for row in answer:
            count = count + 1
        
        if count == 0:
            print 'Game ID does not exist.'
        elif count == 1:
            for row in answer:
                localgid = row.get('gid')
                print localgid
        
            # Find out the vote count for this game.
            try:
                print(cur.mogrify("SELECT votes FROM gamedetails WHERE gid = %s;", (localgid,)))
                cur.execute("SELECT votes FROM gamedetails WHERE gid = %s;", (localgid,)) 
            except:
                print('Could not SELECT votes.')
            answertwo = cur.fetchall()
            
            # Find out if the result set is empty.
            counttwo = 0
            for entry in answertwo:
                counttwo = counttwo + 1
                
            if counttwo == 0:
                print 'Game votes does not exist.'
            elif counttwo == 1:
                for entrytwo in answertwo:
                    votes = entrytwo.get('votes')
                    print votes
                
                # Increment votes
                votes = votes + 1
                print 'Votes is now: %s' % votes
                # Update the database.
                try:
                    print(cur.mogrify("UPDATE gamedetails SET votes = %s WHERE gid = %s;", (votes, localgid)))
                    cur.execute("UPDATE gamedetails SET votes = %s WHERE gid = %s;", (votes, localgid))
                except:
                    print("Error executing UPDATE for votes.")
                    conn.rollback()
                conn.commit()
                
                # Note: Comments are now optional.
                if comment != '':
                    # Add the comment data to the database.
                    try:
                        print(cur.mogrify("INSERT INTO comments (userid, month, day, year, color, comment) VALUES (%s, %s, %s, %s, %s, %s);", 
                        (localUserID, actualmonth, actualday, actualyear, color, comment)))
                        
                        cur.execute("INSERT INTO comments (userid, month, day, year, color, comment) VALUES (%s, %s, %s, %s, %s, %s);", 
                        (localUserID, actualmonth, actualday, actualyear, color, comment))
        
                    except:
                        print("Error inserting new comment into comments table.")
                        conn.rollback()
                    conn.commit()           

                # Now get the (1) updated votes and (2) updated blog comments and send them over to the js controller.
    
                # Get top 3 voted games.
                try:
                    print(cur.mogrify("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;"))
                    cur.execute("SELECT games.title, gamedetails.votes, gamedetails.artpath FROM games NATURAL JOIN gamedetails ORDER BY votes DESC LIMIT 3;")
            
                except:
                    print('Could not SELECT top 3 voted games.')
                votedgames = cur.fetchall()
                
                # TEST
                # print('Printing top 3 voted games.')
                # for game in votedgames:
                #     print(game)
                
                # Get top 3 user blog data.
                try:
                    print(cur.mogrify("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC; "))
                    cur.execute("SELECT * FROM (SELECT comments.commentid, users.username, comments.month, comments.day, comments.year, comments.color, comments.comment FROM users NATURAL JOIN comments ORDER BY commentid DESC LIMIT 3) AS tmp ORDER BY commentid ASC;")
                except:
                    print('Could not SELECT top 3 comments.')
                topcomments = cur.fetchall() 
    
                sidebarData = []
                
                # Add the data to the list as a dictionary.
                for abc in votedgames:
                    game = {'title': abc.get('title'), 'artpath': abc.get('artpath'), 'votes': abc.get('votes')}
                    sidebarData.append(game)
                for cba in topcomments:
                    comment = {'username': cba.get('username'), 'month': cba.get('month'), 'day': cba.get('day'), 'comment': cba.get('comment'), 'color': cba.get('color')} 
                    sidebarData.append(comment)
                
                # TEST
                print('Sidebar Data:')
                for xyz in sidebarData:
                    print(xyz)
                    
                # Send the data over to controller.js.
                emit('sidebarData', sidebarData)




# Start the server.  Main method.  
if __name__ == '__main__':
    # Use the IP address for host.  If not present, use 0.0.0.0.
    # Use the PORT address.  If not present, use 8080.
    #app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
    
    
    
    
    
