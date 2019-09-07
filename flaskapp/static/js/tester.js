// Select the submit button
// var submit = d3.select("#submit");
console.log("hello")
var button = document.getElementById("search-button");

function getUserTweets () {
    var text = document.getElementById("username-search").value;
    window.location.replace("/pull/" + text);
}

// var searchbutton = document.getElementById("submit");
// searchbutton.onclick = function () {
//     var text = document.getElementById("search-form-input").value;
//     window.open("/api/search/" + text);
// }

function getData(text) {
  var text = document.getElementById("search-form-input").value;
  console.log(text);

  
    /* data route */
  var url = "/api/" + text;
  console.log(url);


  d3.json(url).then(function(response) {

    console.log(response);

    var data = response;



  });
}



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
