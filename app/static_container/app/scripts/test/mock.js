(function(){
	"use strict";
	angular.module('superMock',['ngMockE2E'])
	.config(function($provide) {
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
	      console.log('Mock Called');

	      var count = 0;
	      var phones = [{name: 'phone1'}, {name: 'phone2'}];

	      // returns the current list of phones
	      var json_data = JSON.stringify(phones);
	      // var login_json_data = JSON.stringify({'login': true, 'posts_status': 'fetching'});
	      // var login_json_data = {'login_status': false, 'account_status': 'permission_denied'};
	      // var login_json_data = {'login_status': false, 'account_status': 'creation_failed'};
	      // var login_json_data = {'login_status': true, 'account_status': 'new_account'};
	      // var login_json_data = {'login_status': true, 'account_status': 'fetching'};
	      var login_json_data = {'login_status': false, 'account_status': 'fetch_completed'};


	      $httpBackend.whenGET('/login').respond(JSON.stringify((login_json_data)));

	      // var fetch_json = {'status': 'failed', 'fetch_status': 'not_completed'};
	      var fetch_json = {'status': 'success', 'fetch_status': 'completed'};

	      $httpBackend.whenGET('/fetch').respond(JSON.stringify((fetch_json)));

	      // $httpBackend.whenGET('/get_update').respond(json_data);



	      // adds a new phone to the phones array
	      $httpBackend.whenGET('/update/').respond(function(method, url, data) {
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

	        // var result = {'posts': posts};
	        var result;

	        // if(Math.floor((Math.random() * 10) + 1) > 5){
	        //   result = {'account_setup': false};
	        // } else
	        if(true){
	          result = {
	                    'success': true,
	                    'data_type': 'no_posts',
	                    'account_status': 3,
	                    // 'posts': posts
	                  }
	        }
	        /////NO ACCOUNT SETUP/////
	        // var result = {'account_setup': false}
	        /////////

	        /////NO MORE POSTS//////
	        // var result = {'more_posts': false}
	        ///////////////////////


	        // var response = {'success': true, 'data_type': 'posts', 'account_status': 'fetch_completed', 'posts': posts};
	        // var response = {'success': true, 'data_type': 'no_posts', 'account_status': 'new_account'};
	        // var response = {'success': true, 'data_type': 'no_posts', 'account_status': 'fetching'};
	        // var response = {'success': true, 'data_type': 'no_posts', 'account_status': 'fetch_completed'};
	        var response = {'success': false, 'data_type': 'no_posts', 'account_status': 'no_account'};


	        return [200, angular.fromJson(response), {}];
	      });

	      $httpBackend.whenGET(/^\/templates\//).passThrough();
	      $httpBackend.whenGET(/^\/static\//).passThrough();
	      $httpBackend.whenGET(/^\/scripts\//).passThrough();
	      $httpBackend.whenGET(/^\/bower_components\//).passThrough();
	      $httpBackend.whenGET(/^\/styles\//).passThrough();
	      $httpBackend.whenGET(/.*/).passThrough();
	      //...
	    });

	var super_app = angular.module('staticContainerApp');
	super_app.requires[super_app.requires.length] = "superMock";

})();