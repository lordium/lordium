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
	  	$scope.update_tunnel = function(){
	  		var dt = new Date();

	  		var single_post = {
					  	'img_url': 'http://i.imgur.com/1taT5sV.jpg',
					    'title': 'This is title' + dt.toString(),
					    'tags': ['awesome', 'amazing', 'cool'],
					    'description': 'lorem ipsum ' + dt.toString(),
					    'location': 'Stockholm, Sweden',
					    'location_link': ''
					};
	  		$scope.sc.tunnels[0].push(single_post);

	  		$scope.sc.get_posts('');
	  		$scope.sc.poke();
	  	}

	  }])
	  .directive('letmeIn', function(){
	  	return {
	  		restrict: 'A',
	  		link: function(scope, element, attrs){
	  			element.on('click', function(){
	  				scope.sc.login();
	  			});

	  			scope.$watch('sc.flagger.login', function(){
	  				if(scope.sc.flagger.login == true){

	  					element.removeClass('finish-him');
	  					element.html(login_template);
	  				}
	  				else{
	  					element.addClass('finish-him');
	  					element.html('');
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
	  					element.html(msg_remplate);
	  				}
	  				else{
	  					element.addClass('finish-him');
	  					element.html('');
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
	  });

	var login_template = ""+
	  			'<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">'+
			    "<div>"+
			      "<h1>Login from Instagram</h1>"+
			      "<div>"+
			      '<a href="/login"><img src="/static/images/insta.png"/></a>'+
			      '</div>'+
			    "</div>"+
			  "</div>";

	var msg_remplate= '<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">'+
        				'<div>'+
          					'<h1>Gathering your amazing moments</h1>'+
        				'</div>'+
      					'</div>';
})();