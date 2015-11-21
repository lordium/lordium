(function(){
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
		  var sc = {}; // will contain all objects,
		  sc.init_config = {
		  							'client_id': undefined,
		  							'client_secret': undefined,
		  							'website_url': undefined};

		  sc.brand_detail = {'name': false};
		  sc.brand_image='/static/images/insta.png';
		  sc.single_post = {
		  	'imgage_url': 'http://i.imgur.com/1taT5sV.jpg',
		    'title': 'This is title',
		    'tags': ['awesome', 'amazing', 'cool'],
		    'description': 'lorem ipsum sadf adfll e hfasdl klek i asdf asdf akjsdhf',
		    'location': 'Stockholm, Sweden',
		    'location_link': ''};
		  sc.brand_post = {},
		  sc.inpage_messages = {
		  									'1': 'Gathering your awesome moments',
		  									'2': 'Login failed',
		  									'3': 'Something bad happened'}
		  sc.flagger = {'config': false,
		  							 'login': false,
		  							 'mesg': false,
		  							 'update': false };
		  sc.left_tunnel = []; // will show posts on left column
		  sc.middle_tunnel = []; // will show posts on middle column
		  sc.right_tunnel = []; // will show posts on right column
		  sc.last_index = ''; // will contain ids of last post for each tunnel
		  sc.tunnels = [[],[],[]]; //three main tunnels
		  // sc.tunnels = []; //three main tunnels
		  sc.tunnels_sizes = [0,0,0]; //keep the posts sizes for each tunnel
		  sc.single_tunnel_on = false;
		  sc.tunnels_mock = false;
		  sc.tunnel_swap = 0;


		                            // will be end product of this factory
		  sc.get_posts = function(post_url){
		  	post_url = '/get_update';
	 		$http({
	           method: 'GET',
	           url: post_url,
	           headers: {
	               'Content-Type': undefined
	           },
	           data: {'index': sc.last_index}
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

		  sc.post_server = function(post_url,post_data, success_track, failure_track){
	 		return $http({
	           method: 'POST',
	           url: post_url,
	           headers: {
	               'Content-Type': undefined
	           },
	           data: post_data
		       })
		       .success(function (data) {
		       		success_track(data);
		       })
		       .error(function (data, status) {
		       		failure_track(data);
		       });
		  };

		  sc.get_server = function(get_url, data, success_track, failure_track){
		  	console.log('get_server:CALLED');
	 		return $http({
	           method: 'GET',
	           url: get_url,
	           headers: {
	               'Content-Type': undefined
	           },
	           params: data
		       })
		       .success(function (data) {
		       		console.log('get_server:SUCCESS');
		       		success_track(data);
		       })
		       .error(function (data, status) {
		       		failure_track(data, status);
		       });
		  }

		  sc.fetch_success = function(data){
		  	console.log(data.status);
		  	if(data.status == 'success'){
		  		if(data.fetch_status == 'completed'){
	  				sc.flagger.mesg = false;
	  				sc.flagger.config = true;
	  				sc.flagger.update = true;
	  				sc.poke();

		  		}
		  	}
		  	if(data.status == 'failed'){
		  		if(data.fetch_status == 'not_completed'){
		  			//prompt for login if not able to fetch, easiest way for now
	  				sc.flagger.mesg = false;
	  				sc.flagger.config = false;
	  				sc.flagger.update = false;
	  				sc.flagger.login = true;

	  				// sc.poke();

		  		}
		  	}
		  }

		  sc.fetch_status = function(){
		  	//make calls to server using timeout and so on
		  	var data = {};
		  	var check_fetching_process = $timeout(function(){
		  											sc.get_server( '/login_status',
		  																		data,
		  																		sc.fetch_success,
		  																		sc.common_failure_track
		  																		);
		  													}, 2000);
		  }

		  sc.login_success_track = function(data){
		  	sc.response_manager(data);
		  }

		  sc.common_failure_track = function(data, error){
		  	console.log('Something Went wrong...');
		  	console.log(error);
		  }

		  sc.poke = function(){
		  	//1- get data from server
		  	//2- show suitable response

		  	//get posts
		  	console.log('Poke called!')
		  	var data = {'last_id': sc.last_index}
		  	console.log(data);
	  		sc.get_server('/update/',
	  									data,
	  									sc.update_tunnels,
	  									sc.common_failure_track); //will return promise


		  }

		  sc.update_response_filter = function(data){
		  	var result = false;
		  	var data = data; // parse if needed
		  	/*""" Filter the data and send predefined responses
		  	0: if account is not setup (show login)
		  	1: account setup but not fetched yet
		  	2: account setup and fetching (show message)
		  	3: account setup but no posts (show bottom message)
		  	4: there are posts
		  	5: exception (show bottom meessage/error)
		  	"""*/
		  	console.log("update response filter");
		  	console.log(data.hasOwnProperty('account_status'));

		  	function checkStatus(data){
		  		// alert(data);
		  		if(data.hasOwnProperty('account_status'))
			  	{
		  			var account_status = data.account_status;
		  			// alert(account_status);
			  		if(account_status)
			  		{
			  			if(account_status == 'no_account'){
			  				return 'no_account'  // no account
			  			}
			  			if(account_status == 'new_account'){
			  				return 'new_account' //new account/needs fetch
			  			}

			  			if(account_status == 'fetching'){
			  				return 'fetching' // fetching data
			  			}

			  			if(account_status == 'fetch_completed'){
			  				return 'fetch_completed'

			  			}

			  			if(account_status == 'creation_failed'){
			  				return 'creation_failed'
			  			}
			  		}
			  	}
		  	}

		  	// alert('sdf');

		  	if(data.hasOwnProperty('success') && data.success == true){
		  		if(data.hasOwnProperty('account_status')){
		  			return checkStatus(data)
		  		}

		  	}

		  	if(data.hasOwnProperty('success') && data.success == false){
		  		if(data.hasOwnProperty('account_status')){
		  			return checkStatus(data)
		  		}

		  	}


		  	if(data.hasOwnProperty('login_status') && data.login_status == true){
		  		if(data.hasOwnProperty('account_status')){
		  			return checkStatus(data)
		  		}

		  	} else if(data.hasOwnProperty('login_status') && data.login_status == false){

		  		return checkStatus(data)
		  	}
		  	return result
		  }

		  sc.response_manager = function(data){
		  	//TODO: check, if not posts then perform suitable action

		  	//first check the negative responses
		  	//check positive responses below
		  	function extractPosts(data){
				if(data.hasOwnProperty('data_type')){
					if(data.data_type == 'posts'){
						return data.posts
					}
					else{
						return 'no_posts' //fetched but no posts
					}
				}
		  	}

		  	var result = sc.update_response_filter(data); //parse, if needed
		  	console.log('response filter result');
		  	console.log(result);

		  	if(result !== false){
		  		if(result == 'no_account'){ //show login
		  			sc.flagger.config=false;
		  			sc.flagger.login = true;
		  			sc.flagger.update = false;
		  			sc.flagger.mesg = false;
		  		}
		  		else if(result == 'new_account'){
		  			sc.flagger.config=true;
		  			sc.flagger.login = false;
		  			sc.flagger.update = false;
		  			sc.flagger.mesg = true;
		  			//ping server to initiate fetching
		  			//TODO: write ping here
		  			sc.initiate_fetch();
		  		}
		  		else if(result == 'fetching'){
		  			sc.flagger.config=true;
		  			sc.flagger.login = false;
		  			sc.flagger.update = false;
		  			sc.flagger.mesg = true;
		  		}
		  		else if(result == 'no_posts'){
		  			sc.flagger.config=true;
		  			sc.flagger.login = false;
		  			sc.flagger.update = false;
		  			sc.flagger.mesg = false;
		  		}
		  		else if(result == 'exception'){
		  			//TODO: check exception here
		  		}
		  		else if(result == 'creation_failed'){
		  			sc.flagger.config=false;
		  			sc.flagger.login = true;
		  			sc.flagger.update = false;
		  			sc.flagger.mesg = false;
		  		}
		  		else if( result == 'login_failed'){
		  			sc.flagger.config=true;
		  			sc.flagger.login = true;
		  			sc.flagger.update = false;
		  			sc.flagger.mesg = false;
		  		}
		  		else{ //if there are posts
		  			sc.flagger.config=true;
		  			sc.flagger.login = false;
		  			sc.flagger.update = true;
		  			sc.flagger.mesg = false;
		  		}

		  	} else {
		  		alert('ERROR....');
		  	}
		  };

		  sc.login = function(){
		  	sc.get_server('/login/',
		  							   {'mesg': 'letmein'},
		  							    sc.login_success_track,
		  							    sc.common_failure_track
		  							    );
		  }

		  sc.app_setup = function(){
		  	sc.get_server('/login/',
		  							   sc.init_config,
		  							    console.log,
		  							    sc.common_failure_track
		  							    );
		  }

		  sc.initiate_fetch = function(){
		  	sc.get_server('/fetch',
		  							   {'fetch': 'fetch'},
		  							    sc.fetch_success,
		  							    sc.common_failure_track
		  							    );
		  }

		  sc.posts_mocks = function(){
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

		  sc.init = function(){

		  	//file the frame with mocks
		  	// check width and setup tunnels process

		  	sc.update_tunnels(sc.posts_mocks(), 'dum');
		  	sc.tunnels_mock = true;
		  	sc.poke(); // call for initial images

		  }

		  sc.update_tunnels = function(posts, utype){

		  	if(posts.brand_post){
		  		sc.brand_post = posts.brand_post;
		  		console.log(sc.brand_post);
		  	}
		  	if(posts.brand_info){
		  		sc.brand_detail.name = posts.brand_info;
		  	}

		  	if(posts.lucky_image){
		  		sc.brand_image = posts.lucky_image;
		  		console.log('lucky_image');
		  		console.log(sc.brand_image);
		  	}
		  	console.log('Update Tunnels Called');
		  	console.log(posts);
		  	var iposts = posts;
		  	if(utype !='dum'){
		  		sc.response_manager(iposts);
		  	}

		  	if(utype=='dum' || sc.flagger.update){

		  		if(sc.tunnels_mock == true){
		  			sc.flush_tunnels();
		  			sc.tunnels_mock = false;
		  		}
		  		angular.forEach(iposts.posts, function(post){
		  				if(sc.single_tunnel_on == true){
		  					sc.tunnels[0].push(post);
		  				} else{
			  					sc.tunnels[sc.tunnel_swap].push(post);
				  				sc.tunnel_swap +=1;
				  				if(sc.tunnel_swap > 2){
				  					sc.tunnel_swap = 0;
				  				}

			  				}

			  				// console.log('Tunnel Swap');
			  				// console.log(sc.tunnel_swap);

			  				sc.last_index = post.id;
			  				// console.log('Last Index');
			  				// console.log(sc.last_index);
			  				// console.log('Flagger Config:' + String(sc.flagger.config));


		  		});
		  	}

		  }

		  sc.flush_tunnels = function(){

		  	if(sc.single_tunnel_on == true){
		  		sc.tunnels = [[]];
		  	}
		  	else{
		  		sc.tunnels = [[],[],[]];
		  	}

		  }

		  sc.shrink_tunnels = function(){
		  	var posts = [];
		  	posts = posts.concat(sc.tunnels[0]);
		  	posts = posts.concat(sc.tunnels[1]);
		  	posts = posts.concat(sc.tunnels[2]);
		  	sc.tunnels = [posts];
		  }

		  sc.expand_tunnels = function(){
		  	var no = sc.tunnels[0].length;
		  	var posts = [];
		  	var flag = 0;
		  	if(no > 0){
		  		posts = sc.tunnels[0];
		  		sc.tunnels = [[],[],[]];
		  		for(var i = 0; i < no; i++){
		  			sc.tunnels[flag].push(posts[i]);
		  			flag += 1;
		  			if(flag > 2){
		  				flag = 0;
		  			}
		  		}
		  	}
		  }

		 $(window).scroll(function() {
		     if($(window).scrollTop() + $(window).height() == $(document).height()) {
		     	sc.poke();
		     }
		  });

		 $(window).resize(function(){
		   var total_width = window.innerWidth;
		   if(total_width < 767){
		   		if(sc.single_tunnel_on != true){
		   			sc.single_tunnel_on = true;
		   			sc.shrink_tunnels();
		   		}

		   }
		   else{
		   		if(sc.single_tunnel_on != false){
		   			sc.single_tunnel_on = false;
		   			sc.expand_tunnels();
		   		}
		   }
		 });

		 var total_win_width = $(window).width();
		 if(total_win_width < 767){
		   		sc.single_tunnel_on = true;
		   		sc.shrink_tunnels();
		  }
		   else{
		   		sc.single_tunnel_on = false;
		   		sc.expand_tunnels();
		   }


		  return sc; // if everything is ok, send object else exception


		}]);
})();


