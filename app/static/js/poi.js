"use strict";
$(document).ready(function () {

// Fly to location returned by autocomplete

$("#search_submit").on("click", function () {
    
    // For debug
    // console.log("Passed coordinates:", autocomplete_data)

    map.flyTo([autocomplete_data[1], autocomplete_data[0]], 13)

});



$("#venue-update").on("click", function() {
    console.log("Update button clicked")

    let selected_venues = []
    let unselected_venues = []

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
                    showResults(results[0]);
                    paginateResults(results[1],results[2]);
                });
});

// $("input.poi-checkbox:checkbox").on("change" , () => {

//     // Get the name attribute of the child that triggered the event.
//     // As of now, it's the label that wraps the input:checkbox element

//     // Basic flow. When checkbox is checked, event .on("change") is triggered
//     // Then name of checkbox is passed to func getResults and results are 
//     // displayed with the func showResults()

    
//     let value = $(event.target).find("input.poi-checkbox").attr("name");
//     console.log("current value",value);

//     // If event.target detects status "checked", then gets results and shows
//     // markers on map. If "unchecked", it clears the markers from the map

//     if($("input.poi-checkbox").is(":checked")) {
        
//         // For debug
//         // console.log($value,jQuery.type($value),"checked");

//         // Calls getResults, then with the data (query results), calls showResults

//         checked_POI.push(value)
//         console.log("current values in checked_POI", checked_POI)

//         getResults(value).then(results => { 
//             showResults(results[0]);
//             paginateResults(results[1],results[2]);
//         });
//     }
//     else {
        
//         // For debug
//         // console.log($value,"unchecked");

//         // Clears the markers on the map for that POI / tag.
//         checked_POI.splice(value)
//         console.log("current values in checked_POI", checked_POI)
//         clearMarkersFromGroup();
//     }
    
// });

function getResults(query,page=1,per_page=20) {

    // Since other functions depend on the results of the query, it creates a
    // promise. If the query is retrieved with success, then it resolves with 
    // the data. Else, it rejects the resolution

    return new Promise(function (resolve, reject) {
       
        // Query params that will be sent with the Ajax request

        let json_req_payload = {
            "coordinates":[autocomplete_data[1], autocomplete_data[0]],
            "query": query,
            "page":page,
            "per_page":per_page,
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

            var results = [data["result"], data["total_results"],data["pages"]]
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

    for (let i = 1; i < results.length; i++) {

        $("#results").append("<p>" + i + ")." + results[i]["name"] + "</p>")
        addMarkerToGroup(
            results[i]["location"]["coordinates"][0],
            results[i]["location"]["coordinates"][1],
            results[i]["name"]
        );
    }
};

function paginateResults(total_results,pages) {

    $("ul.pagination").empty()
    $("ul.pagination").append('<li class="page-item-previous"><a class="page-link" href="#">Previous</a></li>')
    
    let total_pages = parseInt(pages)
    
    for (let i=1; i < total_pages; i++) {
        let page_link = 
        $("ul.pagination").append('<li class="page-item"><a class="page-link" href="#">'+i+'</a></li>')
    }
    
    $("ul.pagination").append('<li class="page-item-next"><a class="page-link" href="#">Next</a></li>')
};

});