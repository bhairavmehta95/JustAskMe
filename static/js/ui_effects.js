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
    });

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
                        $('#administrator_pass_id').text("Administor Passcode: " + obj.password);
                        $('#questionbank_name_id').text("Question Bank Name: " + obj.namespace);
                        $('.popup').show("slow");

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
                $(".user_instructions").text("Hover to find or to create a question bank");
            }

          }// sz =2
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