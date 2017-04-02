$("#inpt_search").on('focus', function () {
    $(this).parent('label').addClass('active');
});

$("#inpt_search").on('blur', function () {
    if($(this).val().length == 0)
        $(this).parent('label').removeClass('active');
});

$(document).ready(function() {
    $(".search").on('mouseover', function() {
        $(".user_instructions").text("Type the question bank name to join or to create");
    });
    $(".search").on('mouseout', function() {
        $(".user_instructions").text("Hover to find or to create a question bank");
    });

    $('a.close').click(function (event) {
        event.preventDefault();
        $('.popup').hide("slow");
        // $('.popup').show("slow"); // TODO to show the popup window again!
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