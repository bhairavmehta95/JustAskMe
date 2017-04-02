$(document).ready(function() {
    $(".key_button").click(function(){
        if ($(this).hasClass("activate")) {
            $(this).removeClass("activate");
            $('.admin_code').animate({width: 'toggle'}, {duration: 200});
        } else {
            $(this).addClass("activate");
            $('.admin_code').animate({width: 'toggle'}, {duration: 200});
        }
    });
    $(".new_question_button").click(function(){
        if ($(this).hasClass("activate")) {
            $(this).removeClass("activate");
        } else {
            $(this).addClass("activate");
        }
    });
});