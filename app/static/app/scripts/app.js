(function(){
  'use strict';

  /**
   * @ngdoc overview
   * @name lordiumApp
   * @description
   * # lordiumApp
   *
   * Main module of the application.
   */
  angular
    .module('lordiumApp', [
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
})();