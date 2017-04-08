function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function addUpvote(unique_id, upvote){
    var DataToSend = {
        unique_id : unique_id,
        add_upvote : upvote
    }

    $.ajax({
        headers: { "Content-Type": "application/json"},
        url: '/api/addUpvote',
        type: 'POST',
        data: JSON.stringify(DataToSend),
        success: function(data) {
            $(this).parent().find('vote_count').html(toString(parseInt($(this).parent().find('vote_count').html() )+ upvote));
        }
    });
}

function reupdateArrows(){
    $('.voting_arrow_down').hover(function(){
        $(this).find("a").css("color","red");
    }, function(){
        if ($(this).find("a").attr("pressed") === undefined) {
            $(this).find("a").css("color", "black");
        }
    });

    $('.voting_arrow_down').click(function(e){
        console.log($(this).parent().find(".voting_arrow_up").find("a").attr("pressed"));
        e.preventDefault();
        unique_id = $(this).parent().attr('id');
        var upvote_amt = 0;

        // Both up and down unactivated, send -1
        if ($(this).find("a").attr("pressed") === undefined &&
            $(this).parent().find(".voting_arrow_up").find("a").attr("pressed") === undefined){

            $(this).find("a").css("color", "red");
            $(this).find("a").attr("pressed", "true");

            addUpvote(unique_id, -1);
            upvote_amt = -1;
        }

        // Only down arrow activated, cancel out vote by sending +1
        else if ($(this).find("a").attr("pressed") !== undefined &&
            $(this).parent().find(".voting_arrow_up").find("a").attr("pressed") === undefined){

            $(this).find("a").css("color", "");
            $(this).find("a").removeAttr("pressed");

            addUpvote(unique_id, 1);
            upvote_amt = 1;

        }

        // Up arrow is activated, cancel out by sending -2
        else if ($(this).find("a").attr("pressed") === undefined &&
            $(this).parent().find(".voting_arrow_up").find("a").attr("pressed") !== undefined){

            // add color to down
            $(this).find("a").css("color", "red");
            $(this).find("a").attr("pressed", "true");

            // remove color from up
            $(this).parent().find(".voting_arrow_up").find("a").css("color","");
            $(this).parent().find(".voting_arrow_up").find("a").removeAttr("pressed");


            addUpvote(unique_id, -2);
            upvote_amt = -2;
        }

        // update number
        var vote_count = parseInt($(this).parent().find(".vote_count").html());
        vote_count += upvote_amt;
        $(this).parent().find(".vote_count").html(vote_count.toString());

    });

    $('.voting_arrow_up').hover(function(){
        $(this).find("a").css("color","green");
    }, function(){
        if ($(this).find("a").attr("pressed") === undefined) {
            $(this).find("a").css("color", "black");
        }
    });

    $('.voting_arrow_up').click(function(e){
        e.preventDefault();
        unique_id = $(this).parent().attr('id');

        var upvote_amt = 0;

        // Both up and down unactivated, send 1
        if ($(this).find("a").attr("pressed") === undefined &&
            $(this).parent().find(".voting_arrow_down").find("a").attr("pressed") === undefined){

            $(this).find("a").css("color", "green");
            $(this).find("a").attr("pressed", "true");

            addUpvote(unique_id, 1);
            upvote_amt = 1;

        }

        // Only up arrow activated, cancel out vote by sending -1
        else if ($(this).find("a").attr("pressed") !== undefined &&
            $(this).parent().find(".voting_arrow_down").find("a").attr("pressed") === undefined){

            $(this).find("a").css("color", "");
            $(this).find("a").removeAttr("pressed");

            addUpvote(unique_id, -1);
            upvote_amt = -1;
        }

        // Down arrow is activated, cancel out by sending +2
        else if ($(this).find("a").attr("pressed") === undefined &&
            $(this).parent().find(".voting_arrow_down").find("a").attr("pressed") !== undefined) {

            // add color to up
            $(this).find("a").css("color", "green");
            $(this).find("a").attr("pressed", "true");

            // remove color from down
            $(this).parent().find(".voting_arrow_down").find("a").css("color", "");
            $(this).parent().find(".voting_arrow_down").find("a").removeAttr("pressed");


            addUpvote(unique_id, 2);
            upvote_amt = 2;
        }

        // update number
        var vote_count = parseInt($(this).parent().find(".vote_count").html());
        vote_count += upvote_amt;
        $(this).parent().find(".vote_count").html(vote_count.toString());
    });
}

function callUpdate(apiLocation) {
    var room_ = window.location.pathname.toString();

    room_ = room_.substr(1, room_.length);

    var DataToSend = new Object();
    DataToSend = {
        namespace: room_
    };

    $.ajax({
        headers: {"Content-Type": "application/json"},
        url: apiLocation,
        type: 'POST',
        data: JSON.stringify(DataToSend),
        success: function (data) {
            obj = JSON.parse(data);
            $('.question_area').empty();

            // Do something with the result
            if (obj.questions.length) {
                for (i = 0; i < obj.questions.length; i++) {
                    // TODO: Make this into a function
                    var html_to_add = '<div class="question">\
                    <div class="question_tools">\
                    <div class="voting_tools" id="' + obj.unique_ids[i] + '">' +
                        '<div class="voting_arrow_up"><a href="" onclick="return false;" title="Upvote +1"><i class="fa fa-chevron-up" aria-hidden="true"></i></a></div>\
                        <div class="vote_count">' + obj.upvotes[i] + '</div>\
                        <div class="voting_arrow_down"><a href="" onclick="return false;"  title="Downvote -1"><i class="fa fa-chevron-down" aria-hidden="true"></i></a>\
                    </div>\
                    </div>'

                        var second_var = '<div class="admin_delete_centering" id="' + obj.unique_ids[i] + '">\
                    <div class="mark_answered">\
                    <a href="#" title="Mark as read"><i class="fa fa-check" aria-hidden="true"></i></a>\
                    </div>\
                    <div class="trash">\
                    <a href="#" title="Delete permanently"><i class="fa fa-trash-o" aria-hidden="true"></i></a>\
                    </div>\
                    </div>'

                    if(currentUser != null){
                        html_to_add = html_to_add + second_var;
                    }



                    var content = '</div><div class="question_content"> ' + obj.questions[i] + '</div> </div>';
                    $('.question_area').append(html_to_add + content); // append question_area
                }

                reupdateArrows();
            }

        }
    });
}

$(document).ready(function() {
    $(".key_button").click(function(){
        if ($(this).hasClass("activate")) { // TODO do not disactivate if user is an admin! This is "feedback" that user is admin
            $(this).removeClass("activate");
            $('.admin_code').animate({width: 'toggle'}, {duration: 200});
            $(".submit_admin_button").css("display", "none");
        } else {
            $(this).addClass("activate");
            $('.admin_code').animate({width: 'toggle'}, {duration: 200});
            $(".submit_admin_button").css("display", "inline");
            $(".submit_admin_button").addClass("activate");
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

    $(".submit_admin_button").click(function (){
        // Call API, on success, animate
        var DataToSend = {
            room : window.location.pathname.toString().substr(1),
            password : $('input#admin_code_input').val()
        }

        console.log(DataToSend);

        $.ajax({
            headers: { "Content-Type": "application/json"},
            url: '/api/verifyAdmin',
            type: 'POST',
            data: JSON.stringify(DataToSend),
            success: function(data) {
                if (JSON.parse(data)['verified'] == true) {
                    $(this).addClass("activate");
                    window.location.reload();
                }
                else{
                    console.log("wrong pw");
                }
            }
        });
    });

    $('form#emit').submit(function(event) {
        //socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });

    $('form#send_room').submit(function(event) {
        //socket.emit('my room event', {room: room_, data: $('#room_data').val()});
        return false;
    });

    $('form#close').submit(function(event) {
        //socket.emit('close room', {room: $('#close_room').val()});
        return false;
    });

    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect request');
        return false;
    });

    $('#top_link').click(function(){
        document.cookie="ordering=top";
        callUpdate('api/getRowsTop');
    });

    $('#answered_link').click(function(){
        callUpdate();
    });

    $('#newest_link').click(function(){
        document.cookie="ordering=chron";
        callUpdate('api/getRowsChron');
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

$(document).ready( function() {

    namespace = '/';

    var room_ = window.location.pathname.toString();

    room_ = room_.substr(1, room_.length);
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    socket.emit('join', {room: room_});


    socket.on('my response', function(msg) {
        if (getCookie("ordering")==="top") {
            callUpdate('/api/getRowsTop');
        }
        else{
            callUpdate('/api/getRowsChron');
        }
    });

    $('.buttonSubmitQuestion').click(function(){
        var room_ = window.location.pathname.toString();
        room_ = room_.substr(1, room_.length);

        var new_question = $(this).parent().parent().find('.new_question_formulation').val();
        console.log(new_question);
        socket.emit('my room event', {room: room_, data: new_question});

        $('new_question_formulation').text('');
    });


});

