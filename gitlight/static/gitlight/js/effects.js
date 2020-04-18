$('#test-list').click(function (){
    $(this).css('background-color', 'green');
});
$(".side-nav-trigger").click(function() {
    var side_width = $(".sidebar").width();
  $( ".side-menu" ).animate({width: "toggle"});
});

$(".card-body").hover(function () {
    $(this).toggleClass("grey-background");
});
