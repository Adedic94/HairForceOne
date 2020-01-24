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
                $("<td></td>").text(option_list[i].tijdslot_omschrijving),
                $("<td></td>").text(option_list[i].dag),
                $("<td></td>").text(option_list[i].beschikbaarheid_code)
              )
            );
          }
      });
    });
  });