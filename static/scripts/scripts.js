!function(){"use strict";angular.module("lordiumApp",["ngAnimate","ngAria","ngCookies","ngMessages","ngResource","ngRoute","ngSanitize","ngTouch"]).config(function($interpolateProvider){$interpolateProvider.startSymbol("{$").endSymbol("$}")}).run(["$http",function($http){$http.defaults.xsrfHeaderName="X-CSRFToken",$http.defaults.xsrfCookieName="csrftoken"}])}(),function(){"use strict";Object.prototype.hasOwnProperty=function(prop){return void 0!==this[prop]},angular.module("lordiumApp").factory("SuperFactory",["$http","$q","$timeout",function($http,$q,$timeout){var sc={};sc.brand_detail={name:!1},sc.brand_image="/static/images/insta.png",sc.brand_post={},sc.inpage_messages={1:"Gathering your awesome moments",2:"Login failed",3:"Something bad happened"},sc.flagger={config:!1,login:!1,mesg:!1,update:!1},sc.last_index="",sc.tunnels=[[],[],[]],sc.single_tunnel_on=!1,sc.tunnels_mock=!1,sc.tunnel_swap=0,sc.post_server=function(post_url,post_data,success_track,failure_track){return $http({method:"POST",url:post_url,headers:{"Content-Type":void 0},data:post_data}).success(function(data){success_track(data)}).error(function(data,status){failure_track(data)})},sc.post_server_url=function(post_url,post_data,success_track,failure_track){return $http({method:"POST",url:post_url,headers:{"Content-Type":"application/x-www-form-urlencoded"},data:post_data}).success(function(data){success_track(data)}).error(function(data,status){failure_track(data)})},sc.get_server=function(get_url,data,success_track,failure_track){return $http({method:"GET",url:get_url,headers:{"Content-Type":void 0},params:data}).success(function(data){success_track(data)}).error(function(data,status){failure_track(data,status)})},sc.fetch_success=function(data){"success"==data.status&&"completed"==data.fetch_status&&(sc.flagger.mesg=!1,sc.flagger.config=!0,sc.flagger.update=!0,sc.poke()),"failed"==data.status&&"not_completed"==data.fetch_status&&(sc.flagger.mesg=!1,sc.flagger.config=!1,sc.flagger.update=!1,sc.flagger.login=!0)},sc.login_success_track=function(data){sc.response_manager(data)},sc.common_failure_track=function(data,error){console.log("Something Went wrong..."),console.log(error)},sc.poke=function(){var data={last_id:sc.last_index,flag:"update"};sc.post_server_url("/update/",data,sc.update_tunnels,sc.common_failure_track)},sc.update_response_filter=function(data){function checkStatus(data){if(data.hasOwnProperty("account_status")){var account_status=data.account_status;if(account_status){if("no_account"==account_status)return"no_account";if("new_account"==account_status)return"new_account";if("fetching"==account_status)return"fetching";if("fetch_completed"==account_status)return"fetch_completed";if("creation_failed"==account_status)return"creation_failed"}}}var result=!1,data=data;if(data.hasOwnProperty("success")&&1==data.success&&data.hasOwnProperty("account_status"))return checkStatus(data);if(data.hasOwnProperty("success")&&0==data.success&&data.hasOwnProperty("account_status"))return checkStatus(data);if(data.hasOwnProperty("login_status")&&1==data.login_status){if(data.hasOwnProperty("account_status"))return checkStatus(data)}else if(data.hasOwnProperty("login_status")&&0==data.login_status)return checkStatus(data);return result},sc.response_manager=function(data){var result=sc.update_response_filter(data);result!==!1?"no_account"==result?(sc.flagger.config=!1,sc.flagger.login=!0,sc.flagger.update=!1,sc.flagger.mesg=!1):"new_account"==result?(sc.flagger.config=!0,sc.flagger.login=!1,sc.flagger.update=!1,sc.flagger.mesg=!0,sc.initiate_fetch()):"fetching"==result?(sc.flagger.config=!0,sc.flagger.login=!1,sc.flagger.update=!1,sc.flagger.mesg=!0):"no_posts"==result?(sc.flagger.config=!0,sc.flagger.login=!1,sc.flagger.update=!1,sc.flagger.mesg=!1):"exception"==result||("creation_failed"==result?(sc.flagger.config=!1,sc.flagger.login=!0,sc.flagger.update=!1,sc.flagger.mesg=!1):"login_failed"==result?(sc.flagger.config=!0,sc.flagger.login=!0,sc.flagger.update=!1,sc.flagger.mesg=!1):(sc.flagger.config=!0,sc.flagger.login=!1,sc.flagger.update=!0,sc.flagger.mesg=!1)):console.log("Check log, something wrong with server!")},sc.login=function(){sc.get_server("/login/",{mesg:"letmein"},sc.login_success_track,sc.common_failure_track)},sc.login_redirect=function(){window.location.replace("/login/"),window.location.href="/login/"},sc.initiate_fetch=function(){sc.post_server("/fetch/",{fetch:"fetch"},sc.fetch_success,sc.common_failure_track)},sc.posts_mocks=function(){for(var all_posts=[],i=0;5>i;i++){var mock_post={img_url:"",title:"Your awesome title"+String(i),tags:["awesome","amazing","cool"],description:"Breach your limits and show the world all you got! "+String(i),location:"Stockholm, Sweden"+String(i),location_link:"","class":"mock"};all_posts.push(mock_post)}return{posts:all_posts}},sc.init=function(){sc.update_tunnels(sc.posts_mocks(),"dum"),sc.tunnels_mock=!0,sc.poke()},sc.update_tunnels=function(posts,utype){posts.brand_post&&(sc.brand_post=posts.brand_post,$("#favicon").attr("href",sc.brand_post.img_url)),posts.brand_info&&(sc.brand_detail.name=posts.brand_info),posts.lucky_image&&(sc.brand_image=posts.lucky_image);var iposts=posts;"dum"!=utype&&sc.response_manager(iposts),("dum"==utype||sc.flagger.update)&&(1==sc.tunnels_mock&&(sc.flush_tunnels(),sc.tunnels_mock=!1),angular.forEach(iposts.posts,function(post){1==sc.single_tunnel_on?sc.tunnels[0].push(post):(sc.tunnels[sc.tunnel_swap].push(post),sc.tunnel_swap+=1,sc.tunnel_swap>2&&(sc.tunnel_swap=0)),sc.last_index=post.date_published}))},sc.flush_tunnels=function(){1==sc.single_tunnel_on?sc.tunnels=[[]]:sc.tunnels=[[],[],[]]},sc.shrink_tunnels=function(){var posts=[];posts=posts.concat(sc.tunnels[0]),posts=posts.concat(sc.tunnels[1]),posts=posts.concat(sc.tunnels[2]),sc.tunnels=[posts]},sc.expand_tunnels=function(){var no=sc.tunnels[0].length,posts=[],flag=0;if(no>0){posts=sc.tunnels[0],sc.tunnels=[[],[],[]];for(var i=0;no>i;i++)sc.tunnels[flag].push(posts[i]),flag+=1,flag>2&&(flag=0)}},sc.current_location=function(location){var current=window.location.href;if(!location)return current;var pathAr=window.location.href.split("/"),protocol=pathAr[0],host=pathAr[2],url=protocol+"//"+host;return url+location},$(window).scroll(function(){$(window).scrollTop()+$(window).height()==$(document).height()&&sc.poke();var brand_hide_flag=!1;$(window).scrollTop()>30?0==brand_hide_flag&&(brand_hide_flag=!0):1==brand_hide_flag&&(brand_hide_flag=!1),0==brand_hide_flag?($(".navbar-fixed-top-custom").removeClass("scrolled-down"),$(".thumbnail.super_brand_section").slideDown("fast")):($(".thumbnail.super_brand_section").slideUp("slow"),$(".navbar-fixed-top-custom").addClass("scrolled-down"))}),$(window).resize(function(){var total_width=window.innerWidth;767>total_width?1!=sc.single_tunnel_on&&(sc.single_tunnel_on=!0,sc.shrink_tunnels()):0!=sc.single_tunnel_on&&(sc.single_tunnel_on=!1,sc.expand_tunnels())});var total_win_width=$(window).width();return 767>total_win_width?(sc.single_tunnel_on=!0,sc.shrink_tunnels()):(sc.single_tunnel_on=!1,sc.expand_tunnels()),sc}])}(),function(){"use strict";angular.module("lordiumApp").controller("LordiumCtrl",["$scope","SuperFactory",function($scope,SuperFactory){$scope.sc=SuperFactory,$scope.sc.init(),$scope.update_tunnel=function(){var dt=new Date,single_post={img_url:"http://i.imgur.com/1taT5sV.jpg",title:"This is title"+dt.toString(),tags:["awesome","amazing","cool"],description:"lorem ipsum "+dt.toString(),location:"Stockholm, Sweden",location_link:""};$scope.sc.tunnels[0].push(single_post),$scope.sc.get_posts(""),$scope.sc.poke()}}]).directive("letmeIn",function(){return{restrict:"A",link:function(scope,element,attrs){element.on("click",function(){scope.sc.login()}),scope.$watch("sc.flagger.login",function(){1==scope.sc.flagger.login?(element.removeClass("finish-him"),element.html(login_template)):(element.addClass("finish-him"),element.html(""))})}}}).directive("messageInpage",function(){return{restrict:"A",link:function(scope,element,attrs){element.on("click",function(){scope.sc.login()}),scope.$watch("sc.flagger.mesg",function(){1==scope.sc.flagger.mesg?(element.removeClass("finish-him"),element.html(msg_remplate)):(element.addClass("finish-him"),element.html(""))})}}}).directive("luckyYou",function(){return{restrict:"A",link:function(scope,element,attrs){scope.$watch("sc.brand_image",function(){attrs.$set("src",scope.sc.brand_image)})}}}).directive("rightBar",function(){return{restrict:"A",link:function(scope,element,attrs){scope.brand_name=!1,scope.$watch("sc.brand_detail.name",function(){scope.sc.brand_detail.name!==!1&&(scope.brand_name=scope.sc.brand_detail.name)}),0==scope.sc.flagger.config?element.addClass("finish-him"):element.removeClass("finish-him"),scope.$watch("sc.flagger.config",function(){0==scope.sc.flagger.config?element.addClass("finish-him"):element.removeClass("finish-him")})}}}).directive("fixVidBug",function(){return{restrict:"A",link:function(scope,element,attrs){scope.$watch("im_post.img_url",function(){"undefined"!=typeof scope.im_post&&attrs.$set("src",scope.im_post.img_url)})}}});var login_template='<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12"><div><h1>Login from Instagram</h1><div><a href="/login"><img src="/static/images/insta.png"/></a></div></div></div>',msg_remplate='<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12"><div><h1>Gathering your amazing moments</h1></div></div>'}(),function(){"use strict";angular.module("adminApp",[]).run(["$http",function($http){$http.defaults.xsrfHeaderName="X-CSRFToken",$http.defaults.xsrfCookieName="csrftoken"}]).directive("fetchPosts",["$http",function($http){return{restrict:"EA",link:function(scope,element,attrs){element.bind("click",function(element){$(".fetch-text").html("Fetching"),$(".fetch-text").addClass("loading"),$http({method:"POST",url:"/fetch/",headers:{"Content-Type":void 0},data:{fetch:"fetch"}}).success(function(data){console.log(data),$(".fetch-text").removeClass("loading"),$(".fetch-text").html("Fetch Complete")}).error(function(data,status){$(".fetch-text").html("Fetch Failed"),$(".fetch-text").removeClass("loading")})})}}}])}(),function(){"use strict";$.fn.customerPopup=function(e,iWd,iHt,bresize){e.preventDefault(),iWd=iWd||"500",iHt=iHt||"400";var sresize=bresize?"yes":"no",strTitle="undefined"!=typeof this.attr("title")?this.attr("title"):"Lordium Share",strParam="width="+iWd+",height="+iHt+",resizable="+sresize;window.open(this.attr("href"),strTitle,strParam).focus()},$(document).ready(function($){$(".navbar-fixed-top-mobile .search-label").on("click",function(){$(".navbar-fixed-top-mobile .form-group").toggleClass("hide-slide")}),$(".navbar-fixed-top-mobile .navbar-toggle").on("click",function(){$(".navbar-fixed-top-mobile #top_menu_mobile").toggleClass("hide-slide")}),console.log("initi"),$(document.body).on("click",".social-icons li a",function(e){$(this).customerPopup(e)})}),$(".mini-bottom-top-director").click(function(){return $("html, body").animate({scrollTop:0},"slow"),!1})}();