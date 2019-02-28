
function validate_endpoint(input_text)
{
   var endpoint_format = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(:[0-9]+)?$/;
   return input_text.match(endpoint_format)
}

function add_event_handlers() {
    $('body').on('click','#noise_add', function(){
        console.log("noise_add");
                $( "#confirm-noise" ).dialog({
                      resizable: false,
                      height: "auto",
                      width: 520,
                      modal: true,
                      buttons: {
                        "Accept": function() {
                           noise = {};
                           $('#confirm-noise > .message > #endpoint')
                           endpoint = $('#confirm-noise > .message > #endpoint').val().split(":");
                           if (validate_endpoint(endpoint[0])) {
                               noise.endpoint_ip = endpoint[0];
                               if (endpoint.length === 2) {
                                 noise.endpoint_port = parseInt(endpoint[1]);
                               }
                           }
                           else{
                               alert("Noise endpoint should be in the format IPv4 or IPv4:port");
                               return;
                           }
                           if ($('#confirm-noise > .message > #bw').val() != '') {
                             noise.bw = $('#confirm-noise > .message > #bw').val() +
                             $('#confirm-noise > .message > #bw_units').val();
                           }
                           if ($('#confirm-noise > .message > #timeout').val() != '') {
                                  noise.timeout = parseInt($('#confirm-noise > .message > #timeout').val())
                           }
                           console.log(noise)
                            $.ajax({
                                    url: "/api/noises",
                                    type: 'POST',
                                    contentType: 'application/json',
                                    data: JSON.stringify(noise),
                                    timeout: 1000
                                    }).done(function() {
                                       console.log('updated');
                                       show_noises();
                                       })
                                    .fail(function() {
                                        console.error( "error from server" );
                                     });
                                $( this ).dialog( "close" );
                        },
                        Cancel: function() {
                          $( this ).dialog( "close" );
                        }
                      }
                    });
               });
}


function delete_noise(endpoint) {
    $.ajax({
         url: "/api/noises/"+endpoint,
            type: 'DELETE',
             }).done(function() {
                       console.log('deleted noise');
                       show_noises();
                       });
        }

function stop_noise(endpoint) {
    $.ajax({
         url: "/api/noises/"+endpoint+"/stop",
            type: 'POST',
             }).done(function() {
                       console.log('noise stopped');
                       show_noises();
                       });
        }

function show_noises() {
     $.ajax({
            url: "/api/noises"
        }).then(
          function(data) {
           $('#noise_info').find('tbody').text('');
           data.noises.forEach( noise => {
           noise.end = noise.end || '-';
           noise.bw = noise.bw || '-';
           noise.timeout = noise.timeout || '-';
           noise.out = noise.out || '-';
               $('#noise_info').find('tbody').append('<tr><td>'
                            +noise.id
                            +'<i class="fa fa-remove" onclick=delete_noise("'
                            +noise.id+'")></i></td>' +
                            '<td>'+noise.endpoint_ip + ':' + noise.endpoint_port + '</td>' +
                            '<td>'+noise.bw+'</td>' +
                            '<td>'+noise.status+'<i class="fa fa-stop-circle" onclick=stop_noise("'
                            +noise.id+'")></i></td>' +
                            '<td>'+noise.start+'</td>' +
                            '<td>'+noise.timeout+'</td>' +
                            '<td>'+noise.out+'</td></tr>')

           })
       });
 }

$(document).ready(function() {
    console.log("ready")
    add_event_handlers();
});
