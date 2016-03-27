// Create an angular application called 'GameGarage' with no dependencies.
var GameGarage = angular.module('GameGarage', []);

// Create a controller that will interact with the user to update the data model.
GameGarage.controller('GarageController', function($scope){
    // Create connection back to the flask application 'server.py'.
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/gg');
    
    // User registration variables.
    // Variable for the new person's username/avatar.
    $scope.username = '';
    // Variable for the user's first name.
    $scope.firstname = '';
    // Variable for the user's last name.
    $scope.lastname = '';
    // Variable for the user's password.
    $scope.newpassword = '';
    // Variable for the retyped password.
    $scope.retypedpassword = '';
    // Array to hold registration info.
    $scope.registerList = [];
    // Feedback from the server.
    $scope.registerstatus='';
    
    // Variables to display game data dynamically.
    // Username variable passed from the server to HTML to the js controller.
    $scope.loggedinusername = '';
    // Variable to flag what type of game search to run.
    $scope.searchtype = '';
    // List to catch all game data emitted from the server.
    $scope.gamesList = [];
    // Size of master game list.
    $scope.gamesListSize = '';
    // List that holds current webpage's games.
    $scope.gamePageList = [];
    // Size of page list.
    $scope.gamePageListSize = '';
    // Variables for game content.
    $scope.gimage1 = '';
    $scope.gid1 = '';
    $scope.title1 = '';
    $scope.price1 = '';
    //$scope.discount1 = '';
    $scope.desc1 = '';
    $scope.art1 = '';
    $scope.status1 = '';
    
    $scope.gimage2 = '';
    $scope.gid2 = '';
    $scope.title2 = '';
    $scope.price2 = '';
    //$scope.discount2 = '';
    $scope.desc2 = '';
    $scope.art2 = '';
    $scope.status2 = '';
    
    $scope.gimage3 = '';
    $scope.gid3 = '';
    $scope.title3 = '';
    $scope.price3 = '';
    //$scope.discount3 = '';
    $scope.desc3 = '';
    $scope.art3 = '';
    $scope.status3 = '';
    
    $scope.gimage4 = '';
    $scope.gid4 = '';
    $scope.title4 = '';
    $scope.price4 = '';
    //$scope.discount4 = '';
    $scope.desc4 = '';
    $scope.art4 = '';
    $scope.status4 = '';
    
    $scope.gimage5 = '';
    $scope.gid5 = '';
    $scope.title5 = '';
    $scope.price5 = '';
    //$scope.discount5 = '';
    $scope.desc5 = '';
    $scope.art5 = '';
    $scope.status5 = '';
    
    // Variable to track current game content webpage.
    $scope.pagenumber = 0;
    // Variable to track webpage startup.
    $scope.startup=0;
    // Variable to track last game starting point.
    $scope.lastindex=0;
    // Variable to track current game starting point.
    $scope.startindex=0;
    // Variable to track page movement request.
    $scope.direction='';
    // Variable to track number of games on page.
    //$scope.numberofgames=0;


    // Variables for checkout functionality.
    $scope.cartSize=0;
    $scope.ccstatus='';
    $scope.cmonth=0;
    $scope.cyear=0;
    // User input
    $scope.ccnumber='';
    $scope.cccode='';
    $scope.expmonth='Select Month';
    $scope.expyear='';
    // Feedback to user for data checking.
    $scope.checkoutstatus='';
    $scope.ccmessage=''



    // If connect on the socket, run a function.
    socket.on('connect', function(){
        console.log('connected');
        
        // Perform game search if game search variable is not empty. 
        if($scope.searchtype != '')
        {
           $scope.searchGames(); 
        }
        
    });
    
    
     // Attempt to search for games.
    $scope.searchGames = function searchGames() {
        
        // TEST
        console.log('Game search type is: ', $scope.searchtype);
        // TEST
        console.log('Logged in user is: ', $scope.loggedinusername);

        // Send the info. to the server.
        socket.emit('searchtype', $scope.searchtype);
        // Reset all fields.
        $scope.searchtype = '';
    };
    
    // Handle game data emitted from the server.
    socket.on('gamesResult', function(gamesResult){
        
        var gamesResultSize = gamesResult.length;
        var index=0;
        for(index; index<gamesResultSize; index++)
        {
            // Grab one game object at a time.
            var tempGame = gamesResult[index];
            // Add the game to the local list.
            $scope.gamesList.push(tempGame);
            
            // TEST
            //var localtitle = tempGame.title;
            //var localdesc = tempGame.desc;
            //console.log('Title ', localtitle);
            //console.log('Desc ', localdesc);
        }

        // TEST: Print all games.
        $scope.gamesListSize = $scope.gamesList.length;
        var index2=0;
        for(index2; index2<$scope.gamesListSize; index2++)
        {
            // Game object.
            var tempGame2 = $scope.gamesList[index2];
            
            var localgid2 = tempGame2.gid;
            var localtitle2 = tempGame2.title;
            var localprice2 = tempGame2.price;
            //var discountprice2 = tempGame2.discountprice;
            var localdesc2 = tempGame2.desc;
            var localpath2 = tempGame2.artpath;
            
            // TEST
            console.log('Game ID', localgid2);
            console.log('Title: ', localtitle2);
            console.log('Price: ', localprice2);
            //console.log('Discount Price: ', discountprice2);
            console.log('Cover Art Path: ', localpath2);
            console.log('Desc: ', localdesc2);
            
        }
        
        // Empty the gamePageList list.
        var gamePageListSize = $scope.gamePageList.length;
        if(gamePageListSize > 0)
        {
            $scope.gamePageList.length = 0;
        }
        
        // TEST
        //console.log('After emptying gamePageList, its size is: ', $scope.gamePageList.length);
        
        // Call the method that loads the current webpage's games.
        $scope.updatePageGames();
        // Send over the 1st page of game data to the webpage.
        $scope.sendinnerHTML();
    });
    
    
    
    // Update the current webpage's list of games.
    $scope.updatePageGames = function updatePageGames() {
    
    
        if($scope.direction == 'next')
        {
            //console.log('inside next if');
            $scope.lastindex = $scope.startindex;
        }
        else if($scope.direction == 'prev')
        {
            //console.log('inside prev if');
            $scope.startindex = $scope.lastindex - 5;
            $scope.lastindex = $scope.lastindex - 5;
        }
   
        
        console.log('Inside updatePageGames method');
        console.log('Direction is: ', $scope.direction);
        console.log('startindex value is now: ', $scope.startindex);
        console.log('lastindex value is now: ', $scope.lastindex);
    
        $scope.gamesListSize = $scope.gamesList.length;
        var leftoverGames = $scope.gamesListSize - $scope.startindex;
        // TEST
        //console.log('startposition is: ', $scope.startindex);
        //console.log('LeftoverGames is: ', leftoverGames);
        //var fivecount=0;
        //var lessthanfivecount=0;
        
        if(leftoverGames >= 5)
        {
            //$scope.numberofgames = 5;
            //console.log('Number of games on this page is: ', $scope.numberofgames);
            //$scope.startindex=0;
            var endindex = $scope.startindex + 5;
            for($scope.startindex; $scope.startindex<endindex; $scope.startindex++)
            {
                var tempGame = $scope.gamesList[$scope.startindex];
                $scope.gamePageList.push(tempGame);
                //fivecount++;
            }
        }
        
        else
        {
            //$scope.numberofgames =  $scope.gamesListSize - $scope.startindex;
            //console.log('Number of games on this page is: ', $scope.numberofgames);
            //$scope.startindex=0;
            for($scope.startindex; $scope.startindex<$scope.gamesListSize; $scope.startindex++)
            {
                var tempGame2 = $scope.gamesList[$scope.startindex];
                $scope.gamePageList.push(tempGame2);
                //lessthanfivecount++;
            }
        }
        
         // TEST               
        //console.log('fivecount is: ', fivecount);
        //console.log('lessthanfivecount is: ', lessthanfivecount);
        
        //  TEST: Print all the games that will get displayed in the webpage.
        $scope.gamePageListSize = $scope.gamePageList.length;
        console.log('gamePageListSize is: ', $scope.gamePageListSize);
        console.log('Games for current page are:');
      
        var index2=0;
        for(index2; index2<$scope.gamePageListSize; index2++)
        {
            // Set the local game data variable values.
            var tempGame3 = $scope.gamePageList[index2];
            var tempgid3 = tempGame3.gid;
            var temptitle3 = tempGame3.title;
            var tempprice3 = tempGame3.price;
            //var tempdiscount3 = tempGame3.discountprice;
            var tempdesc3 = tempGame3.desc;
            var temppath3 = tempGame3.artpath;
            // TEST
            console.log('Game ID: ', tempgid3);
            console.log('Title: ', temptitle3);
            console.log('Price: ', tempprice3);
            console.log('Cover Art Path: ', temppath3);
            //console.log('Discount Price: ', tempdiscount3);
            console.log('Desc: ', tempdesc3);
            

        }
        
        // TEST
        /*
        console.log('Right BEFORE updating title1/desc1 scope variables.');
        console.log('title1: ', $scope.title1);
        console.log('desc1: ', $scope.desc1);
        
        console.log('title2: ', $scope.title2);
        console.log('desc2: ', $scope.desc2);
        
        console.log('title3: ', $scope.title3);
        console.log('desc3: ', $scope.desc3);
        
        console.log('title4: ', $scope.title4);
        console.log('desc4: ', $scope.desc4);
        
        console.log('title5: ', $scope.title5);
        console.log('desc5: ', $scope.desc5);
        */
        
        // Update the local game data variables from data that's in the gamePageList.
        // These variables are used to dynamically update the webpage.
        if($scope.gamePageListSize >= 1)
        {
            var gameData1 = $scope.gamePageList[0];
            $scope.gid1 = gameData1.gid;
            $scope.title1 = gameData1.title;
            $scope.price1 = gameData1.price;
            //$scope.discount1 = gameData1.discountprice;
            $scope.desc1 = gameData1.desc;
            $scope.art1 = gameData1.artpath;
        }
        
        if($scope.gamePageListSize >= 2)
        {
            var gameData2 = $scope.gamePageList[1];
            $scope.gid2 = gameData2.gid;
            $scope.title2 = gameData2.title;
            $scope.price2 = gameData2.price;
            //$scope.discount2 = gameData2.discountprice;
            $scope.desc2 = gameData2.desc;
            $scope.art2 = gameData2.artpath;
        }
        
        if($scope.gamePageListSize >= 3)
        {
            var gameData3 = $scope.gamePageList[2];
            $scope.gid3 = gameData3.gid;
            $scope.title3 = gameData3.title;
            $scope.price3 = gameData3.price;
            //$scope.discount3 = gameData3.discountprice;
            $scope.desc3 = gameData3.desc;
            $scope.art3 = gameData3.artpath;
        }

        if($scope.gamePageListSize >= 4)
        {
            var gameData4 = $scope.gamePageList[3];
            $scope.gid4 = gameData4.gid;
            $scope.title4 = gameData4.title;
            $scope.price4 = gameData4.price;
            //$scope.discount4 = gameData4.discountprice;
            $scope.desc4 = gameData4.desc;
            $scope.art4 = gameData4.artpath;
            
            // TEST
            //console.log('TEST: game4 title is: ', $scope.title4);
            //console.log('TEST: game4 desc is: ', $scope.desc4);
        }        
        
        if($scope.gamePageListSize >= 5)
        {
            var gameData5 = $scope.gamePageList[4];
            $scope.gid5 = gameData5.gid;
            $scope.title5 = gameData5.title;
            $scope.price5 = gameData5.price;
            //$scope.discount5 = gameData5.discountprice;
            $scope.desc5 = gameData5.desc;
            $scope.art5 = gameData5.artpath;
        }     
        
        // TEST
        /*
        console.log('Right AFTER updating title1/desc1 scope variables.');
        console.log('title1: ', $scope.title1);
        console.log('desc1: ', $scope.desc1);
        
        console.log('title2: ', $scope.title2);
        console.log('desc2: ', $scope.desc2);
        
        console.log('title3: ', $scope.title3);
        console.log('desc3: ', $scope.desc3);
        
        console.log('title4: ', $scope.title4);
        console.log('desc4: ', $scope.desc4);
        
        console.log('title5: ', $scope.title5);
        console.log('desc5: ', $scope.desc5);
        */
        
        
        // TEST
        //console.log('Local title5 variable is: ', $scope.title5);
        //console.log('Local desc5 variable is: ', $scope.desc5);
        
        // Update the current webpage page number.
        if(($scope.direction == 'next') || ($scope.startup == 0))
        {
            $scope.pagenumber++;
        }
        else if($scope.direction == 'prev')
        {
            $scope.pagenumber--;
        }
        
        // Webpage has initialized.
        if($scope.startup < 2)
        {
            $scope.startup++;
        }
        
        // TEST
        console.log('Current page number is: ', $scope.pagenumber);
        
        if($scope.startup == 1)
        {
            // Update the view for that variable.
            $scope.$apply();
            
        }
        
        // Send over the next page of game data to the webpage.
        //$scope.sendinnerHTML();
        
    };
    

    // Method to send game data over to webpage.
    $scope.sendinnerHTML = function sendinnerHTML() {
        
        // Send game data over to HTML page. 
        var elem1a = document.getElementById("title1ID");
        elem1a.innerHTML = $scope.title1;
        var elem1b = document.getElementById("price1ID");
        elem1b.innerHTML = $scope.price1;
        //var elem1c = document.getElementById("discount1ID");
        //elem1c.innerHTML = $scope.discount1;
        var elem1d = document.getElementById("desc1ID");
        elem1d.innerHTML = $scope.desc1;
        var update1 = document.getElementById("status1ID");
        update1.innerHTML = $scope.status1;
        var image1 = document.getElementById("image1ID");
        image1.setAttribute('src', $scope.art1);
        
        var elem2a = document.getElementById("title2ID");
        elem2a.innerHTML = $scope.title2;
        var elem2b = document.getElementById("price2ID");
        elem2b.innerHTML = $scope.price2;
        //var elem2c = document.getElementById("discount2ID");
        //elem2c.innerHTML = $scope.discount2;
        var elem2d = document.getElementById("desc2ID");
        elem2d.innerHTML = $scope.desc2;
        var update2 = document.getElementById("status2ID");
        update2.innerHTML = $scope.status2;
        var image2 = document.getElementById("image2ID");
        image2.setAttribute('src', $scope.art2);
        
        // TEST
        //var image = "css/images/slider4.jpg"
        //console.log('Image2ID path is: ', image)
        //var image2 = document.getElementById("image2ID");
        //image2.setAttribute('src',image);
        
        
        var elem3a = document.getElementById("title3ID");
        elem3a.innerHTML = $scope.title3;
        var elem3b = document.getElementById("price3ID");
        elem3b.innerHTML = $scope.price3;
        //var elem3c = document.getElementById("discount3ID");
        //elem3c.innerHTML = $scope.discount3;
        var elem3d = document.getElementById("desc3ID");
        elem3d.innerHTML = $scope.desc3;
        var update3 = document.getElementById("status3ID");
        update3.innerHTML = $scope.status3;
        var image3 = document.getElementById("image3ID");
        image3.setAttribute('src', $scope.art3);
        
        var elem4a = document.getElementById("title4ID");
        elem4a.innerHTML = $scope.title4;
        var elem4b = document.getElementById("price4ID");
        elem4b.innerHTML = $scope.price4;
        //var elem4c = document.getElementById("discount4ID");
        //elem4c.innerHTML = $scope.discount4;
        var elem4d = document.getElementById("desc4ID");
        elem4d.innerHTML = $scope.desc4; 
        var update4 = document.getElementById("status4ID");
        console.log('update4-status4ID is: ', update4);
        update4.innerHTML = $scope.status4;
        var image4 = document.getElementById("image4ID");
        image4.setAttribute('src', $scope.art4);
        
        console.log('TEST: $scope.title5 is: ', $scope.title5);
        
        var elem5a = document.getElementById("title5ID");
        console.log('elem5a=title5ID is: ', elem5a);
        elem5a.innerHTML = $scope.title5;
        var elem5b = document.getElementById("price5ID");
        elem5b.innerHTML = $scope.price5;
        //var elem5c = document.getElementById("discount5ID");
        //elem5c.innerHTML = $scope.discount5;
        var elem5d = document.getElementById("desc5ID");
        elem5d.innerHTML = $scope.desc5;
        var update5 = document.getElementById("status5ID");
        update5.innerHTML = $scope.status5;
        var image5 = document.getElementById("image5ID");
        image5.setAttribute('src', $scope.art5);
        
    };


    // Disable the nextpage button if there are no more games to get.
    $scope.disablednextpage = function disablednextpage() {
       
       // TEST
       //console.log('startindex value is: ', $scope.startindex);
       //console.log('gamesListSize value is: ', $scope.gamesListSize);
       
       if($scope.startindex >= $scope.gamesListSize)
       {
           //console.log('Next page button is disabled.');
           return true;
       }
 
        return false;
    };
    
    // Disable the prevpage button if there are no more games to get.
    $scope.disabledprevpage = function disabledprevpage() {
        
        // TEST
       console.log('startindex value is: ', $scope.startindex);
       
        if($scope.startindex <= 5)
        {
            return true;
        }
        
        return false;
    };
    
    
    //
    //angular.element(document).ready(function () {

    // your code here

    //});
    //angular.element($window).bind('load', function() {});
    // angular.element($window)

    // Attempt to load the next page of game data.
    $scope.nextpage = function nextpage() {
        
        // TEST
        console.log('TEST: Inside nextpage socketio method.  You pressed the button!');

        // Empty the gamePageList list.
        var gamePageListSize = $scope.gamePageList.length;
        if(gamePageListSize > 0)
        {
            $scope.gamePageList.length = 0;
        }

        // Reset variables.
        $scope.title1 = '';
        $scope.price1 = '';
        //$scope.discount1 = '';
        $scope.desc1 = '';
        $scope.art1 = '';
        $scope.status1 = '';

        $scope.title2 = '';
        $scope.price2 = '';
        //$scope.discount2 = '';
        $scope.desc2 = '';
        $scope.art2 = '';
        $scope.status2 = '';
        
        $scope.title3 = '';
        $scope.price3 = '';
        //$scope.discount3 = '';
        $scope.desc3 = '';
        $scope.art3 = '';
        $scope.status3 = '';
        
        $scope.title4 = '';
        $scope.price4 = '';
        //$scope.discount4 = '';
        $scope.desc4 = '';
        $scope.art4 = '';
        $scope.status4 = '';
        
        $scope.title5 = '';
        $scope.price5 = '';
        //$scope.discount5 =  '';
        $scope.desc5 = '';
        $scope.art5 = '';
        $scope.status5 = '';
        
        $scope.direction = 'next';
        // Call the method that loads the current webpage's games.
        $scope.updatePageGames();
        // Send over the next page of game data to the webpage.
        $scope.sendinnerHTML();
    };
    
    
    // Attempt to load the prev page of game data.
    $scope.prevpage = function prevpage() {
       
        // TEST
        console.log('TEST: Inside prevpage socketio method.  You pressed the button!'); 
        console.log('startindex value is: ', $scope.startindex);
        console.log('lastindex value is: ', $scope.lastindex);
        
        // Empty the gamePageList list.
        var gamePageListSize = $scope.gamePageList.length;
        if(gamePageListSize > 0)
        {
            $scope.gamePageList.length = 0;
        }

        // Reset variables.
        $scope.title1 = '';
        $scope.price1 = '';
        //$scope.discount1 = '';
        $scope.desc1 = '';
        $scope.art1 = '';
        $scope.status1 = '';

        $scope.title2 = '';
        $scope.price2 = '';
        //$scope.discount2 = '';
        $scope.desc2 = '';
        $scope.art2 = '';
        $scope.status2 = '';
        
        $scope.title3 = '';
        $scope.price3 = '';
        //$scope.discount3 = '';
        $scope.desc3 = '';
        $scope.art3 = '';
        $scope.status3 = '';
        
        $scope.title4 = '';
        $scope.price4 = '';
        //$scope.discount4 = '';
        $scope.desc4 = '';
        $scope.art4 = '';
        $scope.status4 = '';
        
        $scope.title5 = '';
        $scope.price5 = '';
        //$scope.discount5 = '';
        $scope.desc5 = '';
        $scope.art5 = '';
        $scope.status5 = '';
        
        $scope.direction = 'prev'
        // Call the method that loads the current webpage's games.
        $scope.updatePageGames();
        // Send over the next page of game data to the webpage.
        $scope.sendinnerHTML();
        
    };
    
    // Disable the addtocart buttons if no user is logged in.
    $scope.disabledcart = function disabledcart() {
        
        if($scope.loggedinusername == '')
        {
            return true;
        }
        
        return false;
    };
    
    // Attempt to add game 1 to cart.
    $scope.addtocart1 = function addtocart1() {

        // Create a list.
        var localList = [];
        // Add logged in user's name to the list.
        localList[0] = $scope.loggedinusername;
        // Add the game id to the list.
        localList[1] = $scope.gid1;
        // Add the page game number to the list.
        localList[2] = 'gameone';
        
        // TEST
        console.log('Sending username: ', localList[0]);
        console.log('Sending game id to add to cart: ', localList[1]);
        console.log('Sending game position: ', localList[2]);
        
        // Send the info. to the server.
        socket.emit('addtocart', localList);
   
    };
    
    // Attempt to add game 2 to cart.
    $scope.addtocart2 = function addtocart2() {

        // Create a list.
        var localList = [];
        // Add logged in user's name to the list.
        localList[0] = $scope.loggedinusername;
        // Add the game id to the list.
        localList[1] = $scope.gid2;
        localList[2] = 'gametwo';
        
        // TEST
        console.log('Sending username: ', localList[0]);
        console.log('Sending game id to add to cart: ', localList[1]);
        console.log('Sending game position: ', localList[2]);
        
        // Send the info. to the server.
        socket.emit('addtocart', localList);
   
    };
    
     // Attempt to add game 3 to cart.
    $scope.addtocart3 = function addtocart3() {

        // Create a list.
        var localList = [];
        // Add logged in user's name to the list.
        localList[0] = $scope.loggedinusername;
        // Add the game id to the list.
        localList[1] = $scope.gid3;
        localList[2] = 'gamethree';
        
        // TEST
        console.log('Sending username: ', localList[0]);
        console.log('Sending game id to add to cart: ', localList[1]);
        console.log('Sending game position: ', localList[2]);
        
        // Send the info. to the server.
        socket.emit('addtocart', localList);
   
    };  
    
     // Attempt to add game 4 to cart.
    $scope.addtocart4 = function addtocart4() {

        // Create a list.
        var localList = [];
        // Add logged in user's name to the list.
        localList[0] = $scope.loggedinusername;
        // Add the game id to the list.
        localList[1] = $scope.gid4;
        localList[2] = 'gamefour';
        
        // TEST
        console.log('Sending username: ', localList[0]);
        console.log('Sending game id to add to cart: ', localList[1]);
        console.log('Sending game position: ', localList[2]);
        
        // Send the info. to the server.
        socket.emit('addtocart', localList);
   
    }; 
    
     // Attempt to add game 5 to cart.
    $scope.addtocart5 = function addtocart5() {

        // Create a list.
        var localList = [];
        // Add logged in user's name to the list.
        localList[0] = $scope.loggedinusername;
        // Add the game id to the list.
        localList[1] = $scope.gid5;
        localList[2] = 'gamefive';
        
        // TEST
        console.log('Sending username: ', localList[0]);
        console.log('Sending game id to add to cart: ', localList[1]);
        console.log('Sending game position: ', localList[2]);
        
        // Send the info. to the server.
        socket.emit('addtocart', localList);
   
    };
    
    // Handle gameinfo status sent from server.
    socket.on('gameinfo', function(gameinfo){
        // Test that the data is receive.
        var localpageposition = gameinfo.pageposition;
        var localgamestatus = gameinfo.gamestatus;
        console.log('Received game position: ', localpageposition);
        console.log('Received game status: ', localgamestatus);
        
        // Send game data over to HTML page.
        if(localpageposition == 'gameone')
        {
            $scope.status1 = localgamestatus;
            var update1 = document.getElementById("status1ID");
            update1.innerHTML = $scope.status1;
        }
        else if(localpageposition == 'gametwo')
        {
            $scope.status2 = localgamestatus;
            var update2 = document.getElementById("status2ID");
            update2.innerHTML = $scope.status2;
        }
        else if(localpageposition == 'gamethree')
        {
            $scope.status3 = localgamestatus;
            var update3 = document.getElementById("status3ID");
            update3.innerHTML = $scope.status3;
        }
        else if(localpageposition == 'gamefour')
        {
            $scope.status4 = localgamestatus;
            var update4 = document.getElementById("status4ID");
            update4.innerHTML = $scope.status4;
        }
        else if(localpageposition == 'gamefive')
        {
            $scope.status5 = localgamestatus;
            var update5 = document.getElementById("status5ID");
            update5.innerHTML = $scope.status5;
        }

        
        // Add the status value to the local variable.
        //$scope.registerstatus = status;
        // Debug message.
        //console.log('Registration status is: ', $scope.registerstatus);
        // Update the view for that variable.
        //$scope.$apply();
    });    
    
    
    // Handle some registration conditions up front before getting to the server.
    $scope.disabledSubmit = function disabledSubmit() {
        if(($scope.username == '') || ($scope.firstname == '') || ($scope.lastname == '') || ($scope.newpassword == '') || ($scope.retypedpassword == ''))
        {
            return true;
        }
        return false;
    };
    
    // Attempt to register.
    $scope.register = function register() {
        // Add the username, password, retyped password, and chat room selections to list.
        // Debug messages.
        console.log('Sending new username: ', $scope.username);
        console.log('Sending firstname: ', $scope.firstname);
        console.log('Sending lastname: ', $scope.lastname);
        console.log('Sending password');
        //console.log('Password is: ', $scope.newpassword);
        console.log('Sending retyped password');
        //console.log('Retyped password is: ', $scope.retypedpassword);
   
        $scope.registerList[0] = $scope.username;
        $scope.registerList[1] = $scope.firstname;
        $scope.registerList[2] = $scope.lastname;
        $scope.registerList[3] = $scope.newpassword;
        $scope.registerList[4] = $scope.retypedpassword;
        
        // Send the info. to the server.
        socket.emit('register', $scope.registerList);
        // Reset all fields.
        $scope.username = '';
        $scope.firstname = '';
        $scope.lastname = '';
        $scope.newpassword = '';
        $scope.retypedpassword = '';
    };
    
    // Handle registration status from server.
    socket.on('status', function(status){
        // Add the status value to the local variable.
        $scope.registerstatus = status;
        // Debug message.
        console.log('Registration status is: ', $scope.registerstatus);
        // Update the view for that variable.
        $scope.$apply();
    });
    
    // Attempt to login.
    $scope.login = function login(){
        // Close the modal dialog box.  Let server.py handle the rest.
        modal.style.display = "none";
    }; 
    
    // Bootstrap modal dialog box js control script.
    $(document).ready(function(){
        $("#myBtn").click(function(){
            $("#myModal").modal();
         });
    });
    
    // Method to delete all games in the logged in user's cart
    // (that are flagged as in the cart (NOT purchased))
    $scope.deletegames = function deletegames(){
      var name = $scope.loggedinusername;
      socket.emit('deletecart', name);
    };
    
    // Method that handles server emit for socketio deletegames.
    socket.on('deletestatus', function(deletestatus){
       console.log('Game cart delete status is: ', $scope.deletestatus);
       $scope.cartSize=0;
       console.log('Number of games in cart is: ', $scope.cartSize);
       $scope.$apply();
    });

    // Method that disable/enables the 'Update' button
    // based on some BUT not all data checks. (for credit card update)
    $scope.disabledCheck = function disabledCheck() {
        

        // If ccstatus id is 'false', then there is no credit card on file.  Also if ccstatus is 'expired'.
        // Need to create a new credit card.
        if(($scope.ccstatus == 'false') || ($scope.ccstatus == 'expired'))
        {
            if(($scope.expmonth == 'Select Month') || ($scope.expyear == '') || ($scope.cccode == '') || ($scope.ccnumber == ''))
            {
                console.log('To create new credit card, all fields must have values.');
                $scope.checkoutstatus = 'Complete all fields to add new credit card.';
                return true;
            }
            
            // Now check that ccnumber, cccode, expmonth and expyear are good.
            var intccnum = parseInt($scope.ccnumber,10);
            var intcode = parseInt($scope.cccode,10);
            var intexpmonth = parseInt($scope.expmonth,10);
            var intexpyear = parseInt($scope.expyear,10);
            console.log('Intccnum is: ', intccnum);
            console.log('Intcode is: ', intcode);
            console.log('Intexpmonth is: ', intexpmonth);
            console.log('Intexpyear is: ', intexpyear);
            
            if(isNaN($scope.ccnumber))
            {
                $scope.checkoutstatus = 'Credit card must have 15-16 digits.';
                return true;
            }
            else if(isNaN($scope.cccode))
            {
                $scope.checkoutstatus = 'Security code must have 3-4 digits.';
                return true;
            }
            else if(isNaN($scope.expyear))
            {
                $scope.checkoutstatus = 'Expiration year must have 4 digits.';
                return true;
            }

            if(intexpyear < $scope.cyear)
            {
                console.log('Entered expyear is less than current year.');
                $scope.checkoutstatus = 'Expiration year is invalid.';
                return true;
            }
            
            if((intexpyear == $scope.cyear) && (intexpmonth < $scope.cmonth))
            {
                console.log('Entered expyear matches current year.');
                console.log('Entered expmonth is less than current month');
                $scope.checkoutstatus = 'Expiration month for current year is invalid.';
                return true;
            }

            if($scope.ccmessage!='')
            {
                $scope.checkoutstatus = $scope.ccmessage;
                return false;
            }
            else
            {
                console.log('New create card data is OK.')
                $scope.checkoutstatus = 'New credit card data is valid.'
                return false;
            }
        }   
        
        if($scope.ccmessage!='')
        {
            $scope.checkoutstatus = $scope.ccmessage;
            return false;
        }
        else
        {
            console.log('New create card data is OK.')
            $scope.checkoutstatus = 'New credit card data is valid.'
            return false;
        }

    };
    
    
    // Send new credit card info. to the server for processing.
    $scope.registercc = function registercc() {

        // TEST
        console.log('Sending new credit card number: ', $scope.ccnumber);
        console.log('Sending new security code: ', $scope.cccode);
        console.log('Sending new expiration month: ', $scope.expmonth);
        console.log('Sending new expiration year: ', $scope.expyear);
        
        // Create a list.
        var localList = [];
        // Add data.
        localList[0] = $scope.ccnumber;
        localList[1] = $scope.cccode;
        localList[2] = $scope.expmonth;
        localList[3] = $scope.expyear;
        
        // // Send the info. to the server.
        socket.emit('updatecc', localList);
    };
    
    // Method that handles server emit for socketio credit card update from within game checkout.
    socket.on('updatestatus', function(updatestatus){
        // Add the status value to the local variable.
        $scope.ccmessage = updatestatus;
        // Debug message.
        console.log('Credit Card status: ', $scope.ccmessage);
        // Update the view for that variable.
        $scope.$apply();
    });
    
      // Method that disable/enables the 'Checkout' button
    // based on some BUT not all data checks.
    $scope.actualCheckout = function actualCheckout() {
        
        if((($scope.ccmessage != '') || ($scope.ccstatus == 'true') || ($scope.ccmessage == 'Successfully added credit card.') || ($scope.ccmessage == 'Successfully updated credit card.')) && ($scope.cartSize != 0))
        {
            //console.log('cartSize is: ', $scope.cartSize);
            return false;
        }
        return true;
    };
    
    
});