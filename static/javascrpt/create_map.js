function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });

    var city_list = {{ city_list | tojson }};

    for (var i = 0; i < city_list.length - 1; i++) {
        var directionsService = new google.maps.DirectionsService();
        var request = {
            origin: city_list[i],
            destination: city_list[i+1],
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                var directionsDisplay = new google.maps.DirectionsRenderer();
                directionsDisplay.setMap(map);
                directionsDisplay.setDirections(response);
            }
        });
    }
}


{/* <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script> */}
