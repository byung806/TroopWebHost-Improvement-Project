console.log("background.js running");


// // Listener function for GET requests on troopwebhost.org
// chrome.webRequest.onBeforeRequest.addListener(
//     function(details) {
//         console.log('Received GET request:', details.url);
//     },
//     { urls: ["<all_urls>"] },
//     ["requestBody"]
// );

// Listener for completed GET requests on troopwebhost.org
chrome.webRequest.onCompleted.addListener(
    function(details) {
        if (details.method === 'GET') {
            console.log('GET request completed:', details.url);
        }
    },
    { urls: ['<all_urls>'] },
    []
);
