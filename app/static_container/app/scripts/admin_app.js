(function(){
	"use strict";

	angular.module('adminApp',[])
	.run(['$http', function($http){
    	$http.defaults.xsrfHeaderName = 'X-CSRFToken';
    	$http.defaults.xsrfCookieName = 'csrftoken';
  	}])
	.directive('fetchPosts', ['$http', function($http){
		return{
			restrict: 'EA',
			link: function fetch_posts(scope, element, attrs){
				element.bind('click', function poke_server(element){
					$('.fetch-text').html('Fetching');
					$('.fetch-text').addClass('loading');
					$http({
						method: 'GET',
						url: '/fetch/',
						headers: {
							'Content-Type': undefined
							},
							data: {'fetch': 'fetch'}
							})
							.success(function (data) {
								console.log(data);
								$('.fetch-text').removeClass('loading');
								$('.fetch-text').html('Fetch Complete');
							})
							.error(function (data, status) {
								$('.fetch-text').html('Fetch Failed');
								$('.fetch-text').removeClass('loading');
							});
				});
			}
		}
	}]);




})();