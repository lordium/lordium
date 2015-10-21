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
    'ngTouch',
    'ngMockE2E'
  ])
  .config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}).config(function($provide) {
    $provide.decorator('$httpBackend', function($delegate) {
        var proxy = function(method, url, data, callback, headers) {
            var interceptor = function() {
                var _this = this,
                    _arguments = arguments;
                setTimeout(function() {
                    callback.apply(_this, _arguments);
                }, 3000);
            };
            return $delegate.call(this, method, url, data, interceptor, headers);
        };
        for(var key in $delegate) {
            proxy[key] = $delegate[key];
        }
        return proxy;
    });
})
  .run(function($httpBackend, $timeout) {
    var phones = [{name: 'phone1'}, {name: 'phone2'}];

    // returns the current list of phones
    var json_data = JSON.stringify(phones);
    $httpBackend.whenGET('/get_update').respond(json_data);

    $httpBackend.whenGET('/login').respond(json_data);

    // adds a new phone to the phones array
    $httpBackend.whenPOST('/get_update').respond(function(method, url, data) {
      var posts = [];
      for(var i=0; i< 5; i++){
        var single_post = {
              'img_url': 'http://i.imgur.com/1taT5sV.jpg',
              'title': 'Your awesome title' + String(i) + String(new Date()),
              'tags': ['awesome', 'amazing', 'cool'],
              'description': 'Breach your limits and show the world all you got! ' + String(i),
              'location': 'Stockholm, Sweden' + String(i),
              'location_link': '',
              'class': ''
          };
          posts.push(single_post);
        }

      // data = [{name: 'phone1'}, {name: 'phone2'}];
      // var phone = angular.fromJson(data);
      // phones.push(phone);

      return [200, angular.fromJson(posts), {}];
    });

    $httpBackend.whenGET(/^\/templates\//).passThrough();
    $httpBackend.whenGET(/^\/static\//).passThrough();
    $httpBackend.whenGET(/^\/scripts\//).passThrough();
    $httpBackend.whenGET(/^\/bower_components\//).passThrough();
    $httpBackend.whenGET(/^\/styles\//).passThrough();
    $httpBackend.whenGET(/.*/).passThrough();
    //...
  });

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
