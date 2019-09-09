// Select the submit button
// var submit = d3.select("#submit");
console.log("hello")
var button = d3.select("subbutt");


url = ("/api/all_tweets");
function getData(){
  d3.json(url).then(function(response) {

    var data = response;



  })
};

button.onclick = getData();


// button.on("click", function() {
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
