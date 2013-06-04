/*
 AngularJS Scripler
*/

/* Controllers */
function ScriplerController($scope) {

    $scope.showResult = "show";

    $scope.chapters = [
    	{ChapterNumber:1, ChapterTitle:'One', ChapterText:'<h1>Header Chapter One</h1><p class="lead">Protoype GUI version 0.1, Cras justo odio, dapibus ac facilisis in, egestas eget quam. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>'},
    	{ChapterNumber:2, ChapterTitle:'Two', ChapterText:'<h1>Header Chapter Two</h1><p class="lead">Protoype GUI version 0.1, Cras justo odio, dapibus ac facilisis in, egestas eget quam. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>'},
    	{ChapterNumber:3, ChapterTitle:'Three', ChapterText:'<h1>Header Chapter Three</h1><p class="lead">Protoype GUI version 0.1, Cras justo odio, dapibus ac facilisis in, egestas eget quam. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>'},
    	{ChapterNumber:4, ChapterTitle:'Four', ChapterText:'<h1>Header Chapter Four</h1><p class="lead">Protoype GUI version 0.1, Cras justo odio, dapibus ac facilisis in, egestas eget quam. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>'},
    	{ChapterNumber:5, ChapterTitle:'Five', ChapterText:'<h1>Header Chapter Five</h1><p class="lead">Protoype GUI version 0.1, Cras justo odio, dapibus ac facilisis in, egestas eget quam. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>'}
    ];

    $scope.showResult = "hide";
};

/* DOM ready functions */
$(document).ready(function(){

	//Click and show content
	$('.step').on('click', function(event){
		
		if ($(this).hasClass('step-before-first')) {
			$('.content.first').show('slow');
			$('.content.second, .content.third').hide('slow');
		}
		else {
			$('.content.first, .content.second, .content.third').hide('slow');
		}

	});

	$('.chapter').on('click', function(event){
	
		var dataContent = $(this).data('content');
		$('#container .content').hide('slow', function() {
			$('#container .content').html(dataContent).show('slow');
		});

	});

	//Resize Actions
	function sizeContent() {
	    var newHeight = $(window).height() - 80;
	    var newHeightStepRight = $(window).height() - 60;
	    var newHeightStepLeft = ($(window).height() - 60) / 3;
	    $(".container-narrow").css("height", newHeight+"px");
	    $(".step-before-first, .step-before-second, .step-before-third").css("height", newHeightStepLeft+"px");
	    $(".step-before-second").css("top", newHeightStepLeft+"px");
	    $(".step-before-third").css("top", newHeightStepLeft*2+"px");
	    $(".step-after, .step-after-content, .step-before-content").css("height", newHeightStepRight+"px");
	}

	sizeContent();
	$(window).resize(sizeContent);

	//Fan Animations
	$('.left .step').on('click', function(event){
	  var thisElement = $(this);
	  var contentElement = $('.left .step-before-content');
	  var allElement = $('.left .step, .left .step-before-content');
	  var outerElement = $('.container-steps.left');
	  var outerElementContent = $('.container-steps.left .content');
	  if (allElement.hasClass('active')) {
	    if (thisElement.hasClass('active')) {

	      allElement.removeClass('active').addClass('show').animate({
	        left: '+=210px'
	      }, "slow", function() {
	        allElement.removeClass('show');
	        outerElement.removeClass('show');
	      });
	    }
	    else {
	      allElement.removeClass('active');
	      thisElement.addClass('active');
	      contentElement.addClass('active');
	    }
	  }
	  else {
	    outerElement.addClass('show');
	    allElement.addClass('show').animate({
	      left: '-=210'
	    }, "slow", function() {
	    });

	    thisElement.addClass('active');
	    contentElement.addClass('active');
	  }

	});

	$('.right .step').on('click', function(event){
	  var allElement = $('.right .step, .right .step-after-content');
	  if (allElement.hasClass('active')) {
	    allElement.addClass('show').animate({
	      right: '+=210'
	    }, "slow", function() {
	      allElement.removeClass('show');
	    });
	  }
	  else {
	    allElement.animate({
	      right: '-=210'
	    }, "slow", function() {
	      allElement.removeClass('show');
	    });
	  }

	  allElement.toggleClass('active');
	});

});