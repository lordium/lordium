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

  }]);
