$( "#datepicker" ).datepicker({beforeShowDay: function(date) {
    var day = date.getDay();
    return [(day != 1)];
}});

  
    $("#datepicker").datepicker(
           { beforeShowDay: function(day) {
               var day = day.getDay();
               if (day == 0 || day == 1) {
                   return [false, "somecssclass"]
               } else {
                   return [true, "someothercssclass"]
               }
            }
           });
       