$(function () {
  $("#accordion").accordion({
    heightStyle: "content"
  });
});

// When the DOM is ready, run this function
$(document).ready(function () {
  //Set the carousel options
  $('#quote-carousel').carousel({
    pause: true,
    interval: 4000,
  });
});

function getOption(id) {
  selectElement = document.querySelector("#" + id);
  console.log(id)
  output = selectElement.value;

  document.querySelector("." + id + "_o").textContent = output;

}

// input fields gelinked aan dropdowns vullen voor form.request reserveren db
$("#dienst_input").click(function () {
  $('#dienst_input2').attr('value', $(this).val());
});

$("#medewerker_input").click(function () {
  $('#medewerker_input2').attr('value', $(this).val());
});

$("#tijdslot_input").click(function () {
  $('#tijdslot_input2').attr('value', $(this).val());
});



function getInput(val) {
  console.log("clickedItem " + val);
}


function makeEditable(element) {
  // selectElement = document.querySelector(".editable");
  element.contenteditable = "true";

  console.log("click!" + this)
}
// enabled tijdsloten als medewerker wordt geselecteerd
function enableTijdsloten() {
  tijdslot_dropdown = document.querySelector('#tijdslot_input');
  tijdslot_dropdown.disabled = false;
  console.log("tijdslot activated");
}

function addRowOnclick() {
  // Find a <table> element with id="services":
  var table = document.getElementById("services");

  // Clone first diensten row in table and append to table
  var node = table.rows[1].cloneNode(true);

  tablebody = table.getElementsByTagName('tbody')[0];
  tablebody.appendChild(node);
}

function getDataFromTable() {
  var table = document.getElementById("services");

  var dict = [];

  for (i = 1; i < table.rows.length; i++) {

    var cellData = [];

    for (j = 0; j < table.rows[i].cells.length - 1; j++) {

      cellData.push(table.rows[i].cells[j].innerHTML);
    }

    dict.push(cellData);
  }

  var data_gestringified = JSON.stringify(dict);
  var diensten_tabel_input = document.getElementById("diensten_tabel_input");
  diensten_tabel_input.value = data_gestringified;

}

$('#diensten_form').submit(function () {
  getDataFromTable();
  return true; // return false to cancel form action
});

$("#datepicker").datepicker({
  minDate: 0,
  dateFormat: "dd-mm-yy",
  beforeShowDay: function (day) {
    var day = day.getDay();
    if (day == 0 || day == 1) {
      return [false, "somecssclass"]
    } else {
      return [true, "someothercssclass"]
    }
  },
  onSelect: function () {
    var selected = $(this).val();
    $("#selected_date").text(selected);
    $('#datum_input').attr('value', $(this).val());

    var medewerker = $("#medewerker_input").val();
    var datum = $("#datum_input").val();

    // send value via GET to URL /<medewerker, datum>
    var get_request = $.ajax({
      type: 'POST',
      data: 'JSON.stringify([medewerker, datum])',
      url: '/reserveren/submit/' + medewerker + '/' + datum,
    });

    // handle response
    get_request.done(function (data) {

      // data
      console.log("changing data")
      // console.log(data)

      // add values to list 9
      var option_list = data;

      $("#tijdslot_input").empty();
      for (var i = 0; i < option_list.length; i++) {
        $("#tijdslot_input").append(
          $("<option></option>").attr("value", option_list[i]).text(option_list[i]));
      }
    });

  }
});



  // test to ensure jQuery is working

$("#medewerker_input").change(function () {
  // grab value
  var medewerker = $("#medewerker_input").val();
  console.log(medewerker) // log voor debuggen
  var datum = $("#datum_input").val();
  console.log(datum) // log voor debuggen

  // send value via GET to URL /<medewerker, datum>
  var get_request = $.ajax({
    type: 'POST',
    data: 'JSON.stringify([medewerker, datum])',
    url: '/reserveren/submit/' + medewerker + '/' + datum,
  });

  // handle response
  get_request.done(function (data) {
    // data
    console.log("changing data")
    // add values to list 
    var option_list = data;

    $("#tijdslot_input").empty();
    for (var i = 0; i < option_list.length; i++) {
      $("#tijdslot_input").append(
        $("<option></option>").attr("value", option_list[i]).text(option_list[i]));
    }
  });
});


function getDataFromProductTable() {
  var dict = [];

  var table = document.getElementsByName("producten_test");

  for (h = 0; h < table.length; h++) {
    for (i = 1; i < table[h].rows.length; i++) {

      var cellData = [];

      for (j = 0; j < table[h].rows[i].cells.length - 1; j++) {

        cellData.push(table[h].rows[i].cells[j].innerHTML);
      }

      dict.push(cellData);
    }
  }

  console.log(JSON.stringify(dict));
  var data_gestringified = JSON.stringify(dict);
  var diensten_tabel_input = document.getElementById("producten_tabel_input");
  diensten_tabel_input.value = data_gestringified;

}

$('#producten_form').submit(function () {
  console.log("onsubmit jquery")
  getDataFromProductTable();
  return true; // return false to cancel form action
});