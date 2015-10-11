'use strict':

/**
 * @ngdoc function
 * @name staticContainerApp.service:SnapWrapper
 * @description
 * # AboutService
 * Factory for images
 */

angular.module('staticContainerApp')
	.factory('SnapWrapper', ['$scope', function($scope){
		var makhool = {};
		makhool.wrap = function(snap){
			//Filter object here
			//Check font size etc.
		}
	}])
	.factory('SnapBarrel', ['$scope', function($scope){
		var barrel = {};
		barrel.addMore = function(last_index, next_limit){ // get more images
			return {}
		}
	}])
	.factory('PokeServer',
		['$scope',
		 '$http',
		 function($scope, $http){
		 	var pigeon = {};
		 	pigeon.getSnaps = function(last_index, next_limit, post_url){
		 		$http({
		           method: 'POST',
		           url: post_url,
		           headers: {
		               'Content-Type': 'multipart/form-data'
		           },
		           data: 'somejsonhere'
			       })
			       .success(function (data) {
			       })
			       .error(function (data, status) {
			       });
		 	}

	}]);