'use strict';
$(document).ready(function () {

    // Fly to location returned by autocomplete
    document.getElementById('search_submit').addEventListener('click', function () {
        console.log('Passed coordinates:', autocomplete_data)

        map.flyTo([autocomplete_data[1], autocomplete_data[0]], 13)
        map.once('moveend', () => getJsonPOI().then(data => showResults(data)));

    });


function getJsonPOI() {
    return new Promise(function (resolve, reject) {
        $.ajax({
            type: 'POST',
            url: "http://127.0.0.1:5000/_getpoi",
            data: JSON.stringify({
                "coordinates": [autocomplete_data[1], autocomplete_data[0]]
            }),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType('application/json;charset=utf-8');
                }
            },
            dataType: 'json',
            success: successHandler,
            error: errorHandler,
            complete: () => {}
        });

        function successHandler(data, textStatus, xhr) {
            console.log('Data from request', data)
            return resolve(data)
        };

        function errorHandler() {
            return reject(new Error('Could not fetch data!'))
        };
    })
};

function showResults(json) {
    console.log('received json', json);

    // Stupid thing adds results on each small map move
    $("#results").empty();
    clearMarkersFromGroup();
    for (let i = 0; i < json["result"].length; i++) {

        $("#results").append("<p>" + i + ")." + json["result"][i]["name"] + "</p>")
        addMarkerToGroup(
            json["result"][i]["location"]["coordinates"][0],
            json["result"][i]["location"]["coordinates"][1],
            json["result"][i]["name"]
        );
    }
};

});