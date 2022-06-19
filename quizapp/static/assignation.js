const url = window.location.href
console.log(url)


const appBtn = document.getElementById('applyBtn')

appBtn.addEventListener('click', getData)


function getData() {
  var send_list = []
  $('#quiz-table').find(':checkbox:checked').each(function() {
    console.log("Ok")
    var dict = {};
    var key = $(this).val()
    var value = $(this).parent().parent().find("select option:checked").val();
    dict["id"] = key
    dict["assignation"] = value
    send_list.push(dict)
  });
  console.log(send_list);
}

// function getData(){
//   var send_list = []
//   $('#quiz-table').find(':checkbox:checked').each(getData() {
//     var dict = {};
//     var value = $(this).parent().find("select option:checked").val();
//   });
// };
  // var $checked = $('input[type="checkbox"]:checked');
  // const keys = Object.keys($checked)
  // keys.forEach((key, index) => {
  //   console.log(`${key}: ${$checked[key]}`);
  // });
  // $checked.forEach(item => console.log(item));



  // console.log('You have ' + $checked.length + ' checked checkboxes!');
// };



// if(quizId.checked == true){
//   console.log('ok');
// }
