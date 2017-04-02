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

// bhairav //
$(document).ready(function(){
    var room_ = window.location.pathname.toString();

    room_ = room_.substr(1, room_.length);
    
    // Add old questions:
    // Call API
    // Add them to Queue with timestamps, upvotes (use log.append)
    var DataToSend = new Object();
    DataToSend = {
        namespace : room_
    }

    $.ajax({
        headers: { "Content-Type": "application/json"},
        url: '/api/getRowsChron',
        type: 'POST',
        data: JSON.stringify(DataToSend),
        success: function(data) {
            obj = JSON.parse(data);
            $('.question_area').empty();
            // Do something with the result
            if (obj.questions.length){
                for (i = 0; i < obj.questions.length; i++) {
                    // TODO: Make this into a function
                    var html_to_add ='<div class="question">\
                            <div class="question_tools">\
                                <div class="voting_tools" id="'
                                    + obj.unique_ids[i] + 
                                     '">\
                                    <div class="voting_arrow_up"><a href="#" title="Upvote +1"><i class="fa fa-chevron-up" aria-hidden="true"></i></a></div>\
                                    <div class="vote_count">15</div>\
                                    <div class="voting_arrow_down"><a href="#" title="Downvote -1"><i class="fa fa-chevron-down" aria-hidden="true"></i></a></div>\
                                </div>\
                            </div>\
                            <div class="question_content"> ' + obj.questions[i] + '</div>'
                        '</div>'
                        // long string
                    $('.question_area').append(html_to_add); 
                }
            }
       },
        error: function(data, status){
            return_val = '';
        },
    });

});


$(document).ready( function() {
    // Sort Chronologically
    $('#sort_chron').click(function(){
        room = window.location.pathname.toString();

        room = room.substr(1, room.length);
    
        
        var DataToSend = new Object();
        DataToSend = {
            namespace : room
        }

        $.ajax({
            headers: { "Content-Type": "application/json"},
            url: '/api/getRowsChron',
            type: 'POST',
            data: JSON.stringify(DataToSend),
            success: function(data) {
                obj = JSON.parse(data);
                
                $(".log").empty();
                console.log('emptied div, refilling with chronological data');

                // Do something with the result
                if (obj.questions.length){
                    for (i = 0; i < obj.questions.length; i++) {
                        // TODO: Make this into a function
                        $('.log').append(
                            '<div class = "question"> <br> ' + obj.questions[i] + ' ' + obj.timestamps[i] + ' ' + obj.upvotes[i] +
                            '<button class="up" id="' + obj.questions[i] + '_up"> Up </button> <button class="down" id="' + obj.questions[i] + '_down"> Down </button> <button class ="del" id="' + obj.questions[i] + '_del"> Del </button></div>'
                             );
                    }
                }
            },
            error: function(data, status){
                return_val = '';
            },
        });
    });

    // Sort by Top
    $('#sort_top').click(function(){
        room = window.location.pathname.toString();

        room = room.substr(1, room.length);
    
        
        var DataToSend = new Object();
        DataToSend = {
            namespace : room
        }

        $.ajax({
            headers: { "Content-Type": "application/json"},
            url: '/api/getRowsChron',
            type: 'POST',
            data: JSON.stringify(DataToSend),
            success: function(data) {
                obj = JSON.parse(data);
                
                $(".log").empty();
                console.log('emptied div, refilling with top');

                // Do something with the result
                if (obj.questions.length){
                    for (i = 0; i < obj.questions.length; i++) {
                        // TODO: Make this into a function
                        $('.log').append(
                            '<div class = "question"> <br> ' + obj.questions[i] + ' ' + obj.timestamps[i] + ' ' + obj.upvotes[i] +
                            '<button class="up" id="' + obj.questions[i] + '_up"> Up </button> <button class="down" id="' + obj.questions[i] + '_down"> Down </button> <button class ="del" id="' + obj.questions[i] + '_del"> Del </button></div>'
                             );
                    }
                }
            },
            error: function(data, status){
                return_val = '';
            },
        });
    });


 });
        

