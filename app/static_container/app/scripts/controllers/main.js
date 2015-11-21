(function(){
	'use strict';

	/**
	 * @ngdoc function
	 * @name staticContainerApp.controller:MainCtrl
	 * @description
	 * # MainCtrl
	 * Controller of the staticContainerApp
	 */
	angular.module('staticContainerApp')
	  .controller('MakhoolCtrl', ['$scope','SuperFactory', function ($scope, SuperFactory) {
	  	$scope.sc = SuperFactory; // returns the object
	  	$scope.sc.init();
	  	$scope.test = "asdfasd";

	  	$scope.update_tunnel = function(){
	  		var dt = new Date();

	  		var single_post = {
					  	'img_url': 'http://i.imgur.com/1taT5sV.jpg',
					    'title': 'This is title' + dt.toString(),
					    'tags': ['awesome', 'amazing', 'cool'],
					    'description': 'lorem ipsum sadf adfll e hfasdl klek i asdf asdf akjsdhf' + dt.toString(),
					    'location': 'Stockholm, Sweden',
					    'location_link': ''
					};
	  		$scope.sc.tunnels[0].push(single_post);

	  		$scope.sc.get_posts('');
	  		$scope.sc.poke();
	  	}

	  }])
	  .directive('superPost', function(){
	  	return{
	  		'restrict': 'A',
	  		// replace: true,
	  		// template: superPostTemplate,
	  		link: function(scope, element, attrs){
	  			scope.video_type = false;
	  			attrs.$observe('superPost', function(flavor) {
			        scope.superPost = superPost;
			        if(superPost.post_tyle == 'video'){
			        	scope.video_type = true;
			        }
			    });
	  		}
	  	}
	  })
	  .directive('letmeIn', function(){
	  	return {
	  		restrict: 'A',
	  		link: function(scope, element, attrs){
	  			//redirect user to login page/instagram
	  			element.on('click', function(){
	  				scope.sc.login();
	  			});

	  			scope.$watch('sc.flagger.login', function(){
	  				if(scope.sc.flagger.login == true){
	  					element.removeClass('finish-him');
	  				}
	  				else{
	  					element.addClass('finish-him');
	  				}
	  			});
	  		}
	  	}
	  })
	  .directive('messageInpage', function(){
	  	return {
	  		restrict: 'A',
	  		link: function(scope, element, attrs){
	  			//redirect user to login page/instagram
	  			element.on('click', function(){
	  				scope.sc.login();
	  			});

	  			scope.$watch('sc.flagger.mesg', function(){
	  				if(scope.sc.flagger.mesg == true){
	  					element.removeClass('finish-him');
	  				}
	  				else{
	  					element.addClass('finish-him');
	  				}
	  			});
	  		}
	  	}
	  })
	  .directive('luckyYou', function(){
	  	return {
	  		restrict: 'A',
	  		link: function(scope, element, attrs){
				scope.$watch('sc.brand_image', function(){
					attrs.$set('src', scope.sc.brand_image);
				});
	  		}
	  	}
	  })
	  .directive('rightBar', function(){
	  	return{
	  		restrict: 'A',
	  		// template: menu_tempate,
	  		link: function(scope, element, attrs){
	  			scope.brand_name = false;
	  			scope.$watch('sc.brand_detail.name', function(){
	  				if(scope.sc.brand_detail.name !== false){
	  					scope.brand_name = scope.sc.brand_detail.name;
	  				}
				});

	  			if(scope.sc.flagger.config == false){
	  				element.addClass('finish-him');
	  			}
	  			else{
	  				element.removeClass('finish-him');
	  			}

	  			scope.$watch('sc.flagger.config', function(){

	  				if(scope.sc.flagger.config == false){
	  					element.addClass('finish-him');
	  				}
	  				else{
	  					element.removeClass('finish-him');
	  				}
	  			});

	  		}
	  	}
	  })
	  .directive('fixVidBug', function(){
	  	return{
	  		'restrict': 'A',
	  		link: function(scope,element, attrs){
	  			scope.$watch('im_post.img_url', function(){
	  				if(typeof scope.im_post != 'undefined')
	  					attrs.$set('src', scope.im_post.img_url);
	  			})

	  		}
	  	}
	  }).directive('configForm', function(){
	  	return {
	  		'restrict': 'A',
	  		link: function(scope, element, attrs){
	  			element.bind('click', function(){
	  				scope.sc.app_setup();
	  				console.log('app called');
	  			})
	  		}
	  	}
	  });

	  // var menu_tempate = '<ul class="nav navbar-nav navbar-right">'+
	  //             '<li><span class="glyphicon glyphicon-search" aria-hidden="true"></span>'+
	  //             '<div class="form-group">'+
   //  			  '<input type="text" class="form-control" ng-model="search" placeholder="">'+
  	// 			  '</div></li>'+
	  //             '<li><a href="/login" ng-show="brand_name ==false">Login</a></li>'+
	  //             '<li class="" ng-show="brand_name != false">'+
	  //               '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{$ brand_name $}<span class="caret"></span></a>'+
	  //               '<ul class="dropdown-menu">'+
	  //                 '<li><a href="/dashboard">Dashboard</a></li>'+
	  //                 '<li role="separator" class="divider"></li>'+
	  //                 '<li><a href="#">Help</a></li>'+
	  //                 '<li role="separator" class="divider"></li>'+
	  //                 '<li><a href="/logout/">Logout</a></li>'+
	  //               '</ul>'+
	  //             '</li>'+
	  //           '</ul>';


	var superPostTemplate = '<img ng-hide={$ video_type $} src="{$ superPost.img_url $}" alt="">'+
							'<video ng-show={$ video_type $} controls width height="150"><source type="video/mp4" src="%s"/></video>'+
         					'<div class="caption">'+
          					'<div class="tags-container">'+
            				'<span ng-repeat="label in superPost.tags">{$ label $}</span>'+
            				'</div>'+
           					'<h3>{$ superPost.title $}</h3>'+
           					'<p>{$ superPost.description $}</p>'+
           					'<p class="location-container">' +
              				'<span class="glyphicon glyphicon-map-marker"></span>' +
              				'<span>{$ superPost.location $}</span>'+
              				'</p>'+
              				'</div>';
})();