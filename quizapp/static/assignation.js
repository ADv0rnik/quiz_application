const url = window.location.href
console.log(url)

const appBtn = document.getElementById('applyBtn')

appBtn.addEventListener('click', getData)


function getData() {
  var send_list = []
  $('#quiz-table').find(':checkbox:checked').each(function() {
    var dict = {};
    var key = $(this).val()
    var value = $(this).parent().parent().find("select option:checked").val();
    dict["id"] = key
    dict["assignation"] = value
    send_list.push(dict)
  });
  console.log(send_list);
  SendData(send_list)
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
