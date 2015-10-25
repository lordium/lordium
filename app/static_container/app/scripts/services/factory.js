'use strict';

/**
 * @ngdoc function
 * @name staticContainerApp.service:SnapWrapper
 * @description
 * # AboutService
 * Factory for images
 */
Object.prototype.hasOwnProperty = function(prop){
	return this[prop]!== undefined;
}
angular.module('staticContainerApp')
	.factory('SuperFactory', ['$http', '$q', '$timeout', function($http, $q, $timeout){
	  var super_container = {}; // will contain all objects,

	  super_container.single_post = {
	  	'imgage_url': 'http://i.imgur.com/1taT5sV.jpg',
	    'title': 'This is title',
	    'tags': ['awesome', 'amazing', 'cool'],
	    'description': 'lorem ipsum sadf adfll e hfasdl klek i asdf asdf akjsdhf',
	    'location': 'Stockholm, Sweden',
	    'location_link': ''};

	  super_container.flagger = {'config': false,
	  							 'login': false,
	  							 'mesg': false,
	  							 'update': false };
	  super_container.left_tunnel = []; // will show posts on left column
	  super_container.middle_tunnel = []; // will show posts on middle column
	  super_container.right_tunnel = []; // will show posts on right column
	  super_container.last_index = ''; // will contain ids of last post for each tunnel
	  super_container.tunnels = [[],[],[]]; //three main tunnels
	  super_container.tunnels_sizes = [0,0,0]; //keep the posts sizes for each tunnel
	  super_container.tunnels_mock = false;
	  super_container.tunnel_swap = 0;


	                            // will be end product of this factory

	  super_container.get_posts = function(post_url){
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

	  super_container.post_server = function(post_data, success_track, failure_track){
 		return $http({
           method: 'POST',
           url: '/get_update',
           headers: {
               'Content-Type': undefined
           },
           data: post_data
	       })
	       .success(function (data) {
	       		success_track(data, 'real');
	       })
	       .error(function (data, status) {
	       		failure_track(data);
	       });
	  };

	  super_container.get_server = function(get_url, data, success_track, failure_track){
 		return $http({
           method: 'GET',
           url: get_url,
           headers: {
               'Content-Type': undefined
           },
           data: data
	       })
	       .success(function (data) {
	       		success_track(data);
	       })
	       .error(function (data, status) {
	       		failure_track(data);
	       });
	  }

	  super_container.fetch_success = function(data){
	  	if(data.posts_status == 'fetching'){
	  		if(typeof data.progress !== 'undefined'){

	  			if(data.progress == '100'){
	  				super_container.flagger.mesg = false;
	  				super_container.flagger.config = true;
	  				super_container.flagger.update = true;
	  				super_container.poke();
	  			}
	  		}
	  	}
	  }

	  super_container.fetch_status = function(){
	  	//make calls to server using timeout and so on
	  	var data = {};
	  	var check_fetching_process = $timeout(function(){
	  											super_container.get_server( '/login_status',
	  																		data,
	  																		super_container.fetch_success,
	  																		super_container.common_failure_track
	  																		);
	  													}, 2000);
	  }

	  super_container.login_success_track = function(data){
	  	super_container.response_type(data);
	  }

	  super_container.common_failure_track = function(data){
	  	alert('login failure');
	  }

	  super_container.poke = function(){
	  	//1- get data from server
	  	//2- show suitable response

	  	//get posts

  		super_container.post_server({},
  									super_container.update_tunnels,
  									super_container.common_failure_track); //will return promise


	  }

	  super_container.response_type = function(data){
	  	//TODO: check, if not posts then perform suitable action

	  	//first check the negative responses
	  	//check positive responses below
	  	if(data.hasOwnProperty('account_setup')){
	  		//TODO: launch the login button
	  		if(data.account_setup == true){
	  			super_container.flagger.config=true;
	  			super_container.flagger.update = false;
	  		}
	  		else{
	  			super_container.flagger.config=false;
	  			super_container.flagger.login = true;
	  			super_container.flagger.update = false;
	  			return;
	  		}

	  		return;
	  	}
	  	if(data.hasOwnProperty('posts_status') && data.posts_status == 'fetching'){
	  		super_container.flagger.mesg = true;
	       	super_container.flagger.login = false;

	       	super_container.fetch_status();
	       	//TODO: awake a method to communicate for updates
	       	// var promise = $q.defer();
	       	// post to server for update
	       	// get the update
	       	// if update complete, hide the meessage
	       	// start displaying images
	       	return;
	  	}

	  	if(data.hasOwnProperty('posts')){
	  		super_container.flagger.mesg = false;
	  		super_container.flagger.login = false;
	  		super_container.flagger.update = true;
	  		super_container.flagger.config = true;
	  	}

	  }

	  super_container.login = function(){
	  	super_container.get_server('/login',
	  							   'letmein',
	  							    super_container.login_success_track,
	  							    super_container.common_failure_track
	  							    );
	  }

	  super_container.posts_mocks = function(){
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
  	  	return {'posts': all_posts}
	  }

	  super_container.init = function(){

	  	//file the frame with mocks
	  	// check width and setup tunnels process

	  	super_container.update_tunnels(super_container.posts_mocks(), 'dum');
	  	super_container.tunnels_mock = true;
	  	super_container.poke(); // call for initial images

	  }

	  super_container.update_tunnels = function(posts, utype){
	  	var iposts = posts;
	  	if(utype !='dum'){
	  		super_container.response_type(iposts);
	  	}

	  	if(utype=='dum' || super_container.flagger.update){

	  		if(super_container.tunnels_mock == true){
	  			super_container.flush_tunnels();
	  			super_container.tunnels_mock = false;
	  		}
	  		angular.forEach(iposts.posts, function(post){
	  				super_container.tunnels[super_container.tunnel_swap].push(post);
	  				super_container.tunnel_swap +=1;
	  				if(super_container.tunnel_swap > 2){
	  					super_container.tunnel_swap = 0;
	  				}
	  		});
	  	}

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