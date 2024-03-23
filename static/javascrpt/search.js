function sendRequest() {
    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/driver_searching', true);

    xhr.send();
}

sendRequest();


setInterval(sendRequest, 2000);
