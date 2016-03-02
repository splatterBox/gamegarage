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
    
    
    // If connect on the socket, run a function.
    socket.on('connect', function(){
        console.log('connected');
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
        
        // TEST
        //console.log('Registered list values are:');
        //var index;
        //var maxindex = $scope.registerList.length - 1;
        //for(index=0; index < maxindex; index++)
        //{
        //    console.log($scope.registerList[index])
        //}
        
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
    
    
    
});