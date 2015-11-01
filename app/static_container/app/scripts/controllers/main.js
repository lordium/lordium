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
	  	$scope.super_container = SuperFactory; // returns the object
	  	$scope.super_container.init();
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
	  		$scope.super_container.tunnels[0].push(single_post);

	  		$scope.super_container.get_posts('');
	  		$scope.super_container.poke();
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
	  				scope.super_container.login();
	  			});

	  			scope.$watch('super_container.flagger.login', function(){
	  				if(scope.super_container.flagger.login == true){
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
	  				scope.super_container.login();
	  			});

	  			scope.$watch('super_container.flagger.mesg', function(){
	  				if(scope.super_container.flagger.mesg == true){
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
				scope.$watch('super_container.brand_image', function(){
					attrs.$set('src', scope.super_container.brand_image);
				});
	  		}
	  	}
	  })
	  .directive('rightBar', function(){
	  	return{
	  		restrict: 'A',
	  		template: menu_tempate,
	  		link: function(scope, element, attrs){
	  			scope.brand_name = false;
	  			scope.$watch('super_container.brand_detail.name', function(){
	  				if(scope.super_container.brand_detail.name !== false){
	  					scope.brand_name = scope.super_container.brand_detail.name;
	  				}
				});

	  			if(scope.super_container.flagger.config == false){
	  				element.addClass('finish-him');
	  			}
	  			else{
	  				element.removeClass('finish-him');
	  			}

	  			scope.$watch('super_container.flagger.config', function(){

	  				if(scope.super_container.flagger.config == false){
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
	  				attrs.$set('src', scope.im_post.img_url);
	  			})

	  		}
	  	}
	  });

	  var menu_tempate = '<ul class="nav navbar-nav navbar-right">'+
	              '<li><a href="#">+</a></li>'+
	              '<li><a href="/login" ng-show="brand_name ==false">Login</a></li>'+
	              '<li class="" ng-show="brand_name != false">'+
	                '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{$ brand_name $}<span class="caret"></span></a>'+
	                '<ul class="dropdown-menu">'+
	                  '<li><a href="#">Dashboard</a></li>'+
	                  '<li role="separator" class="divider"></li>'+
	                  '<li><a href="#">Help</a></li>'+
	                  '<li role="separator" class="divider"></li>'+
	                  '<li><a href="/logout/">Logout</a></li>'+
	                '</ul>'+
	              '</li>'+
	            '</ul>';


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