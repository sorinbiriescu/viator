"use strict";
$(document).ready(function () {

// Fly to location returned by autocomplete

$("#search_submit").on("click", function () {
    
    // For debug
    // console.log("Passed coordinates:", autocomplete_data)

    map.flyTo([autocomplete_data[1], autocomplete_data[0]], 13)

});

let selected_venues = [];
let unselected_venues = [];

$("#venue-update").on("click", function() {
    console.log("Update button clicked")

    $("input.poi-checkbox").each( function() {
        console.log($(this))
        if($(this).is(":checked")) {
            selected_venues.push($(this).attr("name"))
        }
        else {
            unselected_venues.push($(this).attr("name"))
        }
    });
    console.log("poi",selected_venues,unselected_venues)

    getResults(selected_venues).then(results => { 
                    // 0: data["result"],
                    // 1: data["total_results"],
                    // 2: data["total_pages"],
                    // 3: data["current_page"]
                    showResults(results[0]);
                    paginateResults(results[2])
                    
                });
});

function paginateResults(total_pages) {
    
    $('#pagination').twbsPagination({
        totalPages: total_pages,
        visiblePages: 7,
        onPageClick: function (event, page) {
            getResults(selected_venues, page).then(results => {showResults(results[0])})
        }
    });

};

function getResults(query,page=1,per_page=10) {

    // Since other functions depend on the results of the query, it creates a
    // promise. If the query is retrieved with success, then it resolves with 
    // the data. Else, it rejects the resolution

    return new Promise(function (resolve, reject) {
       
        // Query params that will be sent with the Ajax request

        let json_req_payload = {
            "coordinates":[autocomplete_data[1], autocomplete_data[0]],
            "query": query,
            "page":parseInt(page),
            "per_page":parseInt(per_page),
        }

        // Ajax request that will be sent. Takes query params from payload

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/_getpoi",
            data: JSON.stringify(json_req_payload),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            dataType: "json",
            success: successHandler,
            error: errorHandler,
            complete: () => {}
        });

        // On query success function

        function successHandler(data, textStatus, xhr) {
            console.log("Data from request", data)

            var results = [
                data["result"],
                data["total_results"],
                data["total_pages"],
                data["current_page"]
            ]
            return resolve(results)
        };

        // On query error function
        function errorHandler() {
            return reject(new Error("Could not fetch data!"))
        };
    })
};

function showResults(results) {
    console.log("received json", results);

    // Flow: clears the results from the #results div, then iterates over the 
    // query results and displays the results in the #results div

    $("#results").empty();
    clearMarkersFromGroup();

    for (let i = 0; i < results.length; i++) {

        let index = i+1
        $("#results").append("<p>" + index + ")." + results[i]["name"] + "</p>")
        addMarkerToGroup(
            results[i]["location"]["coordinates"][0],
            results[i]["location"]["coordinates"][1],
            results[i]["name"]
        );
    }
};

});