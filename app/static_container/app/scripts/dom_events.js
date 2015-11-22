(function(){
	"use strict";
	$(document).ready(function(){
		$(".navbar-fixed-top-mobile .search-label").on('click', function(){
			$('.navbar-fixed-top-mobile .form-group').toggleClass('hide-slide');
		});

		$(".navbar-fixed-top-mobile .navbar-toggle").on('click', function(){
			$('.navbar-fixed-top-mobile #top_menu_mobile').toggleClass('hide-slide');
		});

	});

	$(".mini-bottom-top-director").click(function() {
	  $("html, body").animate({ scrollTop: 0 }, "slow");
	  return false;
	});
})();