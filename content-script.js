console.log("content-script.js running");

// Function called when AJAX request is sent to navigate to a different page
var callback = function(details) {
    console.log("Before request: ", details);
}
var filter = {urls: ["https://www.troopwebhost.org/*"]};
var opt_extraInfoSpec = [];

chrome.webRequest.onBeforeRequest.addListener(callback, filter, opt_extraInfoSpec);

// const box = document.createElement("button");






// // https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver/observe#parameters


// var xhr = new XMLHttpRequest();

// // override the onreadystatechange event handler
// xhr.onreadystatechange = function() {
//   if (xhr.readyState == 4 && xhr.status == 200) {
//     // do something with the response
//     console.log(xhr.responseText);
//   }
// };

// // make a request
// xhr.open("GET", "https://www.troopwebhost.org/Troop1094Darnestown/", true);
// xhr.send();


// // var headings = document.getElementsByTagName("input");
// // for (var i = 0; i < headings.length; i++) {
// //     if (headings[i].type == "button") {
// //         console.log(headings[i].textContent);
// //     }
// // }
