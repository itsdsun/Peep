// Select the submit button
// var submit = d3.select("#submit");

var button = document.getElementById("searchUser");

button.onclick = function () {
    var text = document.getElementById("username-search").value;
    window.open("/pull/" + text);
}

// var searchbutton = document.getElementById("submit");
// searchbutton.onclick = function () {
//     var text = document.getElementById("search-form-input").value;
//     window.open("/api/search/" + text);
// }

var text = document.getElementById("search-form-input").value;
function getdata() {
    /* data route */
  var url = "/api/" + text;
  d3.json(url).then(function(response) {

    console.log(response);

    var data = response;

    var layout = {
      scope: "usa",
      title: "Pet Pals",
      showlegend: false,
      height: 600,
            // width: 980,
      geo: {
        scope: "usa",
        projection: {
          type: "albers usa"
        },
        showland: true,
        landcolor: "rgb(217, 217, 217)",
        subunitwidth: 1,
        countrywidth: 1,
        subunitcolor: "rgb(255,255,255)",
        countrycolor: "rgb(255,255,255)"
      }
    };

    Plotly.newPlot("plot", data, layout);
  });
}

buildPlot();



// submit.on("click", function() {
//
//   // Prevent the page from refreshing
//   d3.event.preventDefault();
//
//   // Select the input element and get the raw HTML node
//   var inputElement = d3.select("#example-form-input");
//
//   // Get the value property of the input element
//   var inputValue = inputElement.property("value");
//
//   var url = "/api/" + inputValue;
//   console.log(url);
//
//
//
//   // Set the span tag in the h1 element to the text
//   // that was entered in the form
//   d3.select("h1>span").text(inputValue);
// });
