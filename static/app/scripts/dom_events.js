(function(){
	"use strict";
	$.fn.customerPopup = function (e, iWd, iHt, bresize) {

	  e.preventDefault();
	  iWd = iWd || '500';
	  iHt = iHt || '400';
	  var sresize = (bresize ? 'yes' : 'no');
	  var strTitle = ((typeof this.attr('title') !== 'undefined') ? this.attr('title') : 'Lordium Share'),
	      strParam = 'width=' + iWd + ',height=' + iHt + ',resizable=' + sresize,
	      objWindow = window.open(this.attr('href'), strTitle, strParam).focus();
	}

	$(document).ready(function($){
		$(".navbar-fixed-top-mobile .search-label").on('click', function(){
			$('.navbar-fixed-top-mobile .form-group').toggleClass('hide-slide');
		});

		$(".navbar-fixed-top-mobile .navbar-toggle").on('click', function(){
			$('.navbar-fixed-top-mobile #top_menu_mobile').toggleClass('hide-slide');
		});
		console.log('initi');
		$(document.body).on('click', '.social-icons li a', function(e){
			$(this).customerPopup(e);
		});
	});

	$(".mini-bottom-top-director").click(function() {
	  $("html, body").animate({ scrollTop: 0 }, "slow");
	  return false;
	});
})();