function getOption(id) {
  selectElement = document.querySelector("#" + id);
  console.log(id);
  output = selectElement.value;

  document.querySelector("." + id + "_o").textContent = output;

}

$(function() {
    // test to ensure jQuery is working
    $("#medewerker_input").click(function() {
      // grab value
      var medewerker = $("#medewerker_input").val();
      // send value via GET to URL /<category_id>
      var get_request = $.ajax({
        dataType: "json",
        type: 'POST',
        data: 'JSON.stringify([medewerker])',
        url: '/rooster/submit/' + medewerker,
      });
  
      // handle response
      get_request.done(function(data){
        // data
        console.log("changing data");
        // add values to list 
        var option_list = data;
        // console.log(option_list[1]);
        // console.log(option_list[7].dag);
        $("#rooster_body").empty();
          for (var i = 0; i < option_list.length; i++) {
            $("#rooster_body").append(
              $("<tr></tr>").append(
                $("<td></td>").text(option_list[i].medewerker_naam),
                $("<td></td>").text(option_list[i].medewerker_achternaam),
                $("<td></td>").text(option_list[i].tijdslot_omschrijving),
                $("<td></td>").text(option_list[i].dag),
                $("<td contenteditable='true'></td>").text(option_list[i].beschikbaarheid_code)
            )
          );
        }
    });
  });
});


function getDataFromTable(){
  var table = document.getElementById("rooster_table");

  var dict = [];

  for (i = 1; i < table.rows.length; i++){

      var cellData = [];

      for (j = 0; j < table.rows[i].cells.length; j++){

          cellData.push(table.rows[i].cells[j].innerHTML);
      }

      dict.push(cellData);
  }

  console.log(JSON.stringify(dict));
  var data_gestringified= JSON.stringify(dict);
  var rooster_tabel_input = document.getElementById("rooster_tabel_input");
  rooster_tabel_input.value=data_gestringified;

}

$('#rooster_edit_form').submit(function() {
  console.log("onsubmit jquery")
  getDataFromTable();
  return true; // return false to cancel form action
});