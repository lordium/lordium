(function(){
  'use strict';

  /**
   * @ngdoc overview
   * @name staticContainerApp
   * @description
   * # staticContainerApp
   *
   * Main module of the application.
   */
  angular
    .module('staticContainerApp', [
      'ngAnimate',
      'ngAria',
      'ngCookies',
      'ngMessages',
      'ngResource',
      'ngRoute',
      'ngSanitize',
      'ngTouch'
    ])
    .config(function($interpolateProvider){
      $interpolateProvider.startSymbol('{$').endSymbol('$}');
  }).run(['$http', function($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }]);


    // .config(function ($routeProvider) {
    //   $routeProvider
    //     .when('/', {
    //       templateUrl: 'views/main.html',
    //       controller: 'MainCtrl',
    //       controllerAs: 'main'
    //     })
    //     .when('/about', {
    //       templateUrl: 'views/about.html',
    //       controller: 'AboutCtrl',
    //       controllerAs: 'about'
    //     })
    //     .otherwise({
    //       redirectTo: '/'
    //     });
    // });

})();