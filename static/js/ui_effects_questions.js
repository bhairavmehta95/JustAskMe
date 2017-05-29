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

function restoreCurrentVotes(unique_id, isUpvoted){
    fullPath = ".voting_tools#"+ unique_id.toString();
    var upvote_amt = 0;

    if (isUpvoted){
        $(fullPath).find(".voting_arrow_up").find("a").attr("pressed", "true");
        $(fullPath).find(".voting_arrow_up").find("a").css("color","green");
        upvote_amt = 1;
    }

    else{
        $(fullPath).find(".voting_arrow_down").find("a").attr("pressed", "true");
        $(fullPath).find(".voting_arrow_down").find("a").css("color","red");
        upvote_amt = -1;
    }
}

function updateCookies(unique_id, isUpvoted, isRemoved){
    var voteArray;
    var arrayString;

    if (isUpvoted){
        voteArray = JSON.parse(Cookies.get('upvotedIds'));
        arrayString = 'upvotedIds';
    }
    else{
        voteArray = JSON.parse(Cookies.get('downvotedIds'));
        arrayString = 'downvotedIds';
    }

    if (isRemoved){
        var index = voteArray.indexOf(unique_id.toString());
        if (index > -1) {
            voteArray.splice(index, 1);
            Cookies.set(arrayString, JSON.stringify(voteArray));
        }
    }

    else{
        voteArray.push(unique_id);
        Cookies.set(arrayString, JSON.stringify(voteArray));
    }
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
        e.preventDefault();
        unique_id = $(this).parent().attr('id');
        var upvote_amt = 0;
        var downvotedNew = true;
        var wasUpvoted = false;

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
            downvotedNew = false;

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

            wasUpvoted = true;
        }

        // update number
        var vote_count = parseInt($(this).parent().find(".vote_count").html());
        vote_count += upvote_amt;
        $(this).parent().find(".vote_count").html(vote_count.toString());

        if (downvotedNew){
            updateCookies(unique_id, false, false);
        }

        else{
            updateCookies(unique_id, false, true);
        }

        if (wasUpvoted){
            updateCookies(unique_id, true, true);
        }

    });

    $('.voting_arrow_up').hover(function(){
        $(this).find("a").css("color","green");
    }, function(){
        if ($(this).find("a").attr("pressed") == undefined) {
            $(this).find("a").css("color", "black");
        }
    });

    $('.voting_arrow_up').click(function(e){
        e.preventDefault();
        unique_id = $(this).parent().attr('id');

        var upvote_amt = 0;
        var upvotedNew = true;
        var wasDownvoted = false;

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
            upvotedNew = false;
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

            wasDownvoted = true;
        }

        // update number
        var vote_count = parseInt($(this).parent().find(".vote_count").html());
        vote_count += upvote_amt;
        $(this).parent().find(".vote_count").html(vote_count);

        if (upvotedNew){
            updateCookies(unique_id, true, false);
        }

        else{
            updateCookies(unique_id, true, true);
        }

        if (wasDownvoted){
            updateCookies(unique_id, false, true);
        }

    });

    $('.mark_answered').click(function(e){
        e.preventDefault();
        unique_id = $(this).parent().attr('id');

        var DataToSend = new Object();
        DataToSend = {
            unique_id: unique_id
        };

        $.ajax({
            headers: {"Content-Type": "application/json"},
            url: 'api/answerQuestion',
            type: 'POST',
            data: JSON.stringify(DataToSend),
            success: function (data) {},
            error: function(){},
        });

        var apiLocation = "api/getRowsChron";
        if (getCookie("ordering") == "top"){
            apiLocation = "api/getRowsTop";
        }
        callUpdate(apiLocation);
    });

    $('.trash').click(function(e){
        e.preventDefault();
        unique_id = $(this).parent().attr('id');

        var DataToSend = new Object();
        DataToSend = {
            unique_id: unique_id
        };

        $.ajax({
            headers: {"Content-Type": "application/json"},
            url: 'api/deleteQuestion',
            type: 'POST',
            data: JSON.stringify(DataToSend),
            success: function (data) {},
            error: function(){},
        });

        var apiLocation = "api/getRowsChron";
        if (getCookie("ordering") == "top"){
            apiLocation = "api/getRowsTop";
        }
        callUpdate(apiLocation);
    });
}

function getCorrectDate(raw_date){
    formatted_date = (raw_date.getMonth()+1) + '/' + (raw_date.getDate()) + '/'
                         + raw_date.getFullYear() + " ";

    hours = ( (raw_date.getHours() % 12) < 10 ? "0" + raw_date.getHours() % 12 : raw_date.getHours() % 12);
    minutes = ( (raw_date.getMinutes() < 10) ? "0" + raw_date.getMinutes() : raw_date.getMinutes());

    formatted_date += hours + ":" + minutes;

    return formatted_date;
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
                    var raw_date = new Date(obj.timestamps[i]);
                    formatted_date = getCorrectDate(raw_date);
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
                    <a href="" onclick="return false;" title="Mark as answered"><i class="fa fa-check" aria-hidden="true"></i></a>\
                    </div>\
                    <div class="trash">\
                    <a href="" onclick="return false;" title="Delete permanently"><i class="fa fa-trash-o" aria-hidden="true"></i></a>\
                    </div>\
                    </div>'

                    if(currentUser != null && getCookie("ordering").toString() != "answered"){
                        html_to_add = html_to_add + second_var;
                    }



                    var content = '</div><div class="question_content"> ' + obj.questions[i] + '</div> <div class="timestamp">' + formatted_date + '</div> </div> </div> </div>';
                    $('.question_area').append(html_to_add + content); // append question_area

                }

                reupdateArrows();

                var upvoted_ids = JSON.parse(Cookies.get('upvotedIds'))
                for (i = 0; i < upvoted_ids.length; ++i){
                    restoreCurrentVotes(upvoted_ids[i], true);
                }

                var downvoted_ids = JSON.parse(Cookies.get('downvotedIds'))
                for (i = 0; i < downvoted_ids.length; ++i){
                    restoreCurrentVotes(downvoted_ids[i], false);
                }

            }

        }
    });
}

$(document).ready(function() {
    if (Cookies.get('upvotedIds') === undefined){
        var upvotedIds = [];
        Cookies.set('upvotedIds', JSON.stringify(upvotedIds));
    }

    if (Cookies.get('downvotedIds') === undefined){
        var downvotedIds = [];
        Cookies.set('downvotedIds', JSON.stringify(downvotedIds));
    }

    $("#key_button").click(function(){
        if ($(this).hasClass("activate")) { // TODO do not disactivate if user is an admin! This is "feedback" that user is admin
            $('#admin_code').css("display", "none");
            $(this).removeClass("activate");
            $("#submit_admin_button").css("display", "none");

            $("#view_options").css("display", "initial");

        } else {

            $(this).addClass("activate");
            $('#admin_code').animate({width: 'toggle'}, {duration: 200});
            $("#submit_admin_button").css("display", "inline");
            $("#submit_admin_button").addClass("activate");

            // remove all other options
            $("#view_options").css("display", "none");
        }
    });

    $("#new_question_button").click(function(){
        if ($(this).hasClass("activate")) {
            $(this).removeClass("activate");
            $('.write_new_question').animate({height: 'toggle'}, {duration: 200});
        } else {
            $(this).addClass("activate");
            $('.write_new_question').animate({height: 'toggle'}, {duration: 200});
        }
    });

    $("#submit_admin_button").click(function (){
        // Call API, on success, animate
        var DataToSend = {
            room : window.location.pathname.toString().substr(1),
            password : $('input#admin_code_input').val()
        }

        $.ajax({
            headers: { "Content-Type": "application/json"},
            url: '/api/verifyAdmin',
            type: 'POST',
            data: JSON.stringify(DataToSend),
            success: function(data) {
                if (JSON.parse(data)['verified'] == true) {
                    $(this).addClass("activate");
                    window.location.href = window.location.href;
                }
                else{
                    // TODO: wrong password, maybe CSS?
                }
            }
        });
    });

    $('#top_link').click(function(){
        document.cookie="ordering=top";
        callUpdate('api/getRowsTop');
    });

    $('#answered_link').click(function(){
        document.cookie="ordering=answered";
        callUpdate('api/getAnswered');
    });

    $('#newest_link').click(function(){
        document.cookie="ordering=chron";
        callUpdate('api/getRowsChron');
    });
});

// CSS descriptor section
$(document).ready(function() {
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

// Socket section
$(document).ready( function() {

    namespace = '/';

    var room_ = window.location.pathname.toString();

    // set title
    document.title = "JustAskMe" + room_;

    room_ = room_.substr(1, room_.length);
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // send join room command
    socket.emit('join', {room: room_});

    // connect
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    socket.on('my response', function(msg) {
        if (getCookie("ordering") =="top") {
            callUpdate('/api/getRowsTop');
        }
        else{
            callUpdate('/api/getRowsChron');
        }
    });

    $('#buttonSubmit').click(function(){
        var room_ = window.location.pathname.toString();
        room_ = room_.substr(1, room_.length);

        var new_question = $(this).parent().parent().find('.new_question_formulation').val();

        if (new_question != '') {
            socket.emit('my room event', {room: room_, data: new_question});

            $('.new_question_formulation').text('');
            $('.new_question_button').removeClass("activate");
            $('.write_new_question').animate({height: 'toggle'}, {duration: 10});

            $(this).parent().parent().find('.new_question_formulation').val("");
        }
    });


});

// Every five seconds, see if it is not in focus
// If not, reload the page cleanly
$(document).ready(function() {
    var window_focus;

    $(window).focus(function() {
        window_focus = true;
    })
    .blur(function() {
        window_focus = false;
    });

    setInterval(function() {
        if (window_focus == false){
            var ordering = getCookie("ordering");

            if (ordering == "top"){
                callUpdate('api/getRowsTop');
            }
            else if (ordering == "answered"){
                callUpdate('api/getAnswered');
            }
            else {
                callUpdate('api/getRowsChron');
            }
        }
    }, 5000);
});
