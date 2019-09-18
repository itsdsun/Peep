// Select the submit button
// var submit = d3.select("#submit");
console.log("hello")
// var searchTable = d3.select("#mytable");

var submit = d3.select("#subbutt");

//TESTING TO LOAD ALL TWEETS
url = "/api/all_tweets";
d3.json(url).then(function(response) {
    console.log(response);
    if (response.length > 0){
      var temp = "";
      response.forEach((u)=>{
        temp += "<tr>";
        temp += "<td>"+u.tweet+"</td>";
        temp += "<td>"+u.date+"</td></tr>";
      })

      document.getElementById("data").innerHTML = temp;
    }
});

$("#myInput").keyup(function () {
    var value = this.value.toLowerCase().trim();

    $("table tr").each(function (index) {
        if (!index) return;
        $(this).find("td").each(function () {
            var id = $(this).text().toLowerCase().trim();
            var not_found = (id.indexOf(value) == -1);
            $(this).closest('tr').toggle(!not_found);
            return not_found;
        });
    });
});
