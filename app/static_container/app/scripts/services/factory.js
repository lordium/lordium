'use strict';

/**
 * @ngdoc function
 * @name staticContainerApp.service:SnapWrapper
 * @description
 * # AboutService
 * Factory for images
 */

angular.module('staticContainerApp')
	.factory('SuperFactory', ['$http', '$q', function($http, $q){
	  var super_container = {}; // will contain all objects,

	  super_container.single_post = {
	  	'imgage_url': 'http://i.imgur.com/1taT5sV.jpg',
	    'title': 'This is title',
	    'tags': ['awesome', 'amazing', 'cool'],
	    'description': 'lorem ipsum sadf adfll e hfasdl klek i asdf asdf akjsdhf',
	    'location': 'Stockholm, Sweden',
	    'location_link': ''};

	  super_container.left_tunnel = []; // will show posts on left column
	  super_container.middle_tunnel = []; // will show posts on middle column
	  super_container.right_tunnel = []; // will show posts on right column
	  super_container.last_index = ''; // will contain ids of last post for each tunnel
	  super_container.tunnels = [[],[],[]]; //three main tunnels
	  super_container.tunnels_sizes = [0,0,0]; //keep the posts sizes for each tunnel
	  super_container.tunnels_mock = false;
	  super_container.tunnel_swap = 0;


	                            // will be end product of this factory

	  super_container.get_posts = function get_posts(post_url){
	  	post_url = '/get_update';
 		$http({
           method: 'GET',
           url: post_url,
           headers: {
               'Content-Type': undefined
           },
           data: {'index': super_container.last_index}
	       })
	       .success(function (data) {
	       		//here I got the new posts
	       		console.log(data);
	       })
	       .error(function (data, status) {
	       		//these is something wrong
	       		console.log(data);
	       });
	  };

	  super_container.post_server = function post_server(post_data){
 		return $http({
           method: 'POST',
           url: '/get_update',
           headers: {
               'Content-Type': undefined
           },
           data: post_data
	       })
	       .success(function (data) {
	       		console.log(data);
	       		super_container.update_tunnels(data);
	       })
	       .error(function (data, status) {
	       		alert(data);
	       });
	  };

	  super_container.poke = function poke(){
	  	//1- get data from server
	  	//2- show suitable response

	  	//get posts
	  	console.log('POCKED');
	  	var server_obj = {}
	  	var server_response = super_container.post_server(server_obj); //will return promise
	  }

	  super_container.init = function(){

	  	//file the frame with mocks
	  	// check width and setup tunnels process
	  	var all_posts = [];
	  	for(var i=0; i< 5; i++){
	  		var mock_post = {
					  	'img_url': '',//'http://i.imgur.com/1taT5sV.jpg',
					    'title': 'Your awesome title' + String(i),
					    'tags': ['awesome', 'amazing', 'cool'],
					    'description': 'Breach your limits and show the world all you got! ' + String(i),
					    'location': 'Stockholm, Sweden' + String(i),
					    'location_link': '',
					    'class': 'mock'
					};
	  		all_posts.push(mock_post);

	  	}
	  	super_container.update_tunnels(all_posts);
	  	super_container.tunnels_mock = true;
	  	super_container.poke(); // call for initial images

	  }

	  super_container.update_tunnels = function(posts){
	  	if(super_container.tunnels_mock == true){
	  		super_container.flush_tunnels();
	  		super_container.tunnels_mock = false;
	  	}
	  	angular.forEach(posts, function(post){
	  			super_container.tunnels[super_container.tunnel_swap].push(post);
	  			console.log(super_container.tunnel_swap);
	  			super_container.tunnel_swap +=1;
	  			if(super_container.tunnel_swap > 2){
	  				super_container.tunnel_swap = 0;
	  			}

	  	});
	  }

	  super_container.flush_tunnels = function(){
	  	super_container.tunnels = [[],[],[]];
	  }


	 $(window).scroll(function() {
	     if($(window).scrollTop() + $(window).height() == $(document).height()) {
	     	//TODO: Start animation here
	     	super_container.poke(); //TODO: End animation in this function
	     }
	  });

	  return super_container; // if everything is ok, send object else exception


	}]);