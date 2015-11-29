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
		.factory('SuperFactory', ['$http', '$q', '$timeout', function(
			$http, $q, $timeout){

		  var sc = {}; // namespace,
		  sc.brand_detail = {'name': false};
		  sc.brand_image='/static/images/insta.png';
		  sc.brand_post = {},
		  sc.inpage_messages = {
								'1': 'Gathering your awesome moments',
								'2': 'Login failed',
								'3': 'Something bad happened'};

		  sc.flagger = {'config': false,
						 'login': false,
						 'mesg': false,
						 'update': false };

		  sc.last_index = ''; // contains id of last post
		  sc.tunnels = [[],[],[]]; //three main tunnels
		  sc.single_tunnel_on = false; // flag for screen size
		  sc.tunnels_mock = false;
		  sc.tunnel_swap = 0; // tunnels swaper => 0,1,2

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

		  sc.post_server_url = function(post_url,post_data, success_track, failure_track){
	 		return $http({
	           method: 'POST',
	           url: post_url,
	           headers: {
	               'Content-Type': 'application/x-www-form-urlencoded'
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
	 		return $http({
	           method: 'GET',
	           url: get_url,
	           headers: {
	               'Content-Type': undefined
	           },
	           params: data
		       })
		       .success(function (data) {
		       		success_track(data);
		       })
		       .error(function (data, status) {
		       		failure_track(data, status);
		       });
		  }

		  sc.fetch_success = function(data){
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
	  				sc.flagger.mesg = false;
	  				sc.flagger.config = false;
	  				sc.flagger.update = false;
	  				sc.flagger.login = true;
		  		}
		  	}
		  }

		  sc.login_success_track = function(data){
		  	sc.response_manager(data);
		  }

		  sc.common_failure_track = function(data, error){
		  	console.log('Something Went wrong...');
		  	console.log(error);
		  }

		  sc.poke = function(){

		  	var data = {'last_id': sc.last_index, 'flag':'update'}
	  		sc.post_server_url('/update/',
	  									data,
	  									sc.update_tunnels,
	  									sc.common_failure_track);

		  }

		  sc.update_response_filter = function(data){
		  	var result = false;
		  	var data = data;

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
		  		console.log('Check log, something wrong with server!');
		  	}
		  };

		  sc.login = function(){
		  	sc.get_server('/login/',
	  							   {'mesg': 'letmein'},
	  							    sc.login_success_track,
	  							    sc.common_failure_track
	  							    );
		  }

		  sc.login_redirect = function(){
		  	window.location.replace("/login/");
		  	window.location.href = "/login/";
		  }

		  sc.initiate_fetch = function(){
		  	sc.post_server('/fetch/',
		  							   {'fetch': 'fetch'},
		  							    sc.fetch_success,
		  							    sc.common_failure_track
		  							    );
		  }

		  sc.posts_mocks = function(){
	  	  	var all_posts = [];
	  	  	for(var i=0; i< 5; i++){
	  	  		var mock_post = {
	  					  	'img_url': '',
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
		  		$("#favicon").attr("href",sc.brand_post.img_url);
		  	}
		  	if(posts.brand_info){
		  		sc.brand_detail.name = posts.brand_info;
		  	}

		  	if(posts.lucky_image){
		  		sc.brand_image = posts.lucky_image;

		  	}
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
			  				// id of last post
			  				sc.last_index = post.date_published;
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

		     var brand_hide_flag = false;

		     if($(window).scrollTop() > 30){
		     	if(brand_hide_flag == false){
		     		brand_hide_flag = true;
		     	}
		     }
		     else{
		     	if(brand_hide_flag == true){
		     		brand_hide_flag = false;
		     	}
		     }

		     if(brand_hide_flag == false){
		     	$('.navbar-fixed-top-custom').removeClass('scrolled-down');
		     	$('.thumbnail.super_brand_section').slideDown('fast');
		     }else{
		     	$('.thumbnail.super_brand_section').slideUp('slow');
		     	$('.navbar-fixed-top-custom').addClass('scrolled-down');
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

		  return sc;

		}]);
})();


