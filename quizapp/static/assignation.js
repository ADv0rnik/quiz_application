const url = window.location.href
console.log(url)

const appBtn = document.getElementById('applyBtn')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

appBtn.addEventListener('click', getData)


function getData() {
  var send_data = {}
  send_data['csrfmiddlewaretoken'] = csrf[0].value
  $('#quiz-table').find(':checkbox:checked').each(function() {
    var key = $(this).val()
    var value = $(this).parent().parent().find("select option:checked").val();
    send_data[key] = value
  });
  console.log(send_data);
  SendData(send_data)
}

function SendData(data) {
  console.log(data)
  $.ajax({
    type: 'POST',
    url: `${url}/save`,
    data: data,
    success: function(response){
      console.log(response)
    },
    error: function(error){
      console.log(error)
    }
  });
}
