$(document).ready(function() {
    $(document).keydown(function(event) {
        var sz = $("#inpt_search").val().length;

        if (sz > 2){
            var b = $("#inpt_search").val().replace(/[^a-z0-9]/gi,'');

            if (event.keyCode == 13 && b != ''){
                var DataToSend = new Object();
                DataToSend = {
                    namespace : $("#inpt_search").val()
                } // datatosend

                $.ajax({
                    headers: { "Content-Type": "application/json"},
                    url: '/api/genAdminPw',
                    type: 'POST',
                    data: JSON.stringify(DataToSend),
                    success: function(data) {
                        obj = JSON.parse(data);

                        if (obj.exists == true){
                            window.location = window.location.href + obj.namespace;
                        }

                        else {
                            $('#administrator_pass_id').text("Administor Passcode: " + obj.password);
                            $('#questionbank_name_id').text("Question Bank Name: " + obj.namespace);
                            $('.popup').show("slow");
                        }

                        $('#button').click(function() {
                                var DataToSend = new Object();
                                DataToSend = {
                                    namespace : obj.namespace,
                                    password : obj.password
                                }

                                $.ajax({
                                    headers: { "Content-Type": "application/json"},
                                    url: '/api/addAdmin',
                                    type: 'POST',
                                    data: JSON.stringify(DataToSend),
                                    success: function(data) {
                                        window.location = window.location.href + obj.namespace;
                                    },
                                    error: function(data, status){
                                        return_val = '';
                                    },
                                });
                            });
                        },
                    error: function(data, status){
                        return_val = '';
                    },
                }); // ajax
            } // if kc == 13

            else if (b == ''){
                $(".user_instructions").text("Oops, only alphanumeric characters!");
            }

            else{
                $(".user_instructions").text("Whenever you're ready!");
            }

        }// sz =2

        else{
            $(".user_instructions").text("Search for a question bank")
        }

    });

    $("#close_popup").click(function(event){
        event.preventDefault();
        $(".popup").css("display", "none");
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