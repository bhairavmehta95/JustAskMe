$(document).ready(function() {
    $(".key_button").click(function(){
        if ($(this).hasClass("activate")) { // TODO do not disactivate if user is an admin! This is "feedback" that user is admin
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
            $('.write_new_question').animate({height: 'toggle'}, {duration: 200});
        } else {
            $(this).addClass("activate");
            $('.write_new_question').animate({height: 'toggle'}, {duration: 200});
        }
    });
});

$(function() {
    $( "#button" ).click(function() {
        $( "#button" ).addClass( "onclic", 250, validate);
    });

    function validate() {
        setTimeout(function() {
            $( "#button" ).removeClass( "onclic" );
            $( "#button" ).addClass( "validate", 450, callback );
        }, 2250 );
    }
    function callback() {
        setTimeout(function() {
            $( "#button" ).removeClass( "validate" );
        }, 1250 );
    }
});