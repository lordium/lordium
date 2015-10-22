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
  .directive('letmeIn', function(){
  	return {
  		restrict: 'A',
  		link: function(scope, element, attrs){
  			//redirect user to login page/instagram
  			element.on('click', function(){
  				scope.super_container.login();
  			});

  			scope.$watch('super_container.show_login', function(){
  				if(scope.super_container.show_login == true){
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

  			scope.$watch('super_container.show_message', function(){
  				if(scope.super_container.show_message == true){
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
			scope.$watch('super_container.account_configured', function(){
				if(scope.super_container.account_configured == false){
					attrs.$set('src',"images/insta.png");
					// element.addClass('finish-him');
				}
				else{
					// element.removeClass('finish-him');
					attrs.$set('src',"images/insta.png");
				}
			});
  		}
  	}
  })
  .directive('rightBar', function(){
  	return{
  		restrict: 'A',
  		template: menu_tempate,
  		link: function(scope, element, attrs){
  			if(scope.super_container.account_configured == false){
  				element.addClass('finish-him');
  			}
  			else{
  				element.removeClass('finish-him');
  			}

  			scope.$watch('super_container.account_configured', function(){
  				if(scope.super_container.account_configured == false){
  					element.addClass('finish-him');
  				}
  				else{
  					element.removeClass('finish-him');
  				}
  			});

  		}
  	}
  });

  var menu_tempate = '<ul class="nav navbar-nav navbar-right finish-him">'+
              '<li><a href="#">About</a></li>'+
              '<li class="something">'+
                '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Login<span class="caret"></span></a>'+
                '<ul class="dropdown-menu">'+
                  '<li><a href="#">Action</a></li>'+
                  '<li><a href="#">Another action</a></li>'+
                  '<li><a href="#">Something else here</a></li>'+
                  '<li role="separator" class="divider"></li>'+
                  '<li><a href="#">Separated link</a></li>'+
                  '<li role="separator" class="divider"></li>'+
                  '<li><a href="#">One more separated link</a></li>'+
                '</ul>'+
              '</li>'+
            '</ul>';
