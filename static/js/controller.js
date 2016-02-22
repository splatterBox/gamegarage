// Create an angular application called 'GameGarage' with no dependencies.
var GameGarage = angular.module('GameGarage', []);

// Create a controller that will interact with the user to update the data model.
GameGarage.controller('GarageController', function($scope){
    // Create connection back to the flask application 'server.py'.
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/gg');
    
    
    // If connect on the socket, run a function.
    socket.on('connect', function(){
        console.log('connected');
    });
    
    
});