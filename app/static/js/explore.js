"use strict";
let csrf_token = "{{ csrf_token() }}"; // the token is set by Jinja2


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token); // insert custom header
        }
    }
});

$(document).ready(function () {

    let selected_venues;
    let unselected_venues;

    $("#search_submit").on("click", function () {

        map.flyTo([autocomplete_data[1], autocomplete_data[0]], 13)
        fetchAndShow(selected_venues)

    });

    $("#venue-update").on("click", function () {
        selected_venues = [];
        unselected_venues = [];

        
        $("input.poi-checkbox").each(function () {

            if ($(this).is(":checked")) {
                selected_venues.push($(this).attr("name"));

            } else {
                unselected_venues.push($(this).attr("name"));
            }
        });

        fetchAndShow(selected_venues);

    });

    function getResults(query, page = 1, per_page = 10) {

        // Since other functions depend on the results of the query, it creates a
        // promise. If the query is retrieved with success, then it resolves with 
        // the data. Else, it rejects the resolution

        return new Promise(function (resolve, reject) {

            // Query params that will be sent with the Ajax request

            let json_req_payload = {
                "coordinates": [autocomplete_data[1], autocomplete_data[0]],
                "query": query,
                "page": parseInt(page),
                "per_page": parseInt(per_page),
            }

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/api/getpoi",
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

            function successHandler(data, textStatus, xhr) {

                var results = [
                    data["result"],
                    data["total_results"],
                    data["total_pages"],
                    data["current_page"]
                ]
                return resolve(results)
            };

            function errorHandler() {
                return reject(new Error("Could not fetch data!"))
            };
        })
    };

    function showResults(results) {

        // Flow: clears the results from the #results div, then iterates over the 
        // query results and displays the results in the #results div

        $("#results").empty();
        clearMarkersFromGroup();

        for (let i = 0; i < results.length; i++) {

            let index = i + 1
            $("#results").append($("<li></li>")
                            .text(results[i]["name"]));
            $("#results").append($("<button></button>")
                            .attr("class","btn btn-primary btn-sm btn-add-poi")
                            .attr("type","button")
                            .attr("oid",results[i]["oid"]+"."+results[i]["osm_type"])
                            .text("Add attraction"));
            
            addMarkerToGroup(
                results[i]["location"]["coordinates"][0],
                results[i]["location"]["coordinates"][1],
                results[i]["name"],
                results[i]["icon"],
                results[i]["color"],
                results[i]["shape"]
            );
        }
    };

    function paginateResults(total_pages) {

        $('#pagination').twbsPagination('destroy');

        $('#pagination').twbsPagination({
            totalPages: total_pages,
            visiblePages: 7,
            initiateStartPageClick: false,
            onPageClick: function (event, page) {
                getResults(selected_venues, page).then(results => {
                    showResults(results[0])
                });
            }
        });

    };

    function fetchAndShow(selected_venues) {
        if (selected_venues.length === 0) {

        } else {
            getResults(selected_venues).then(results => {
                // 0: data["result"],
                // 1: data["total_results"],
                // 2: data["total_pages"],
                // 3: data["current_page"]
                showResults(results[0]);
                paginateResults(results[2])

            });
        }
    }

    getRoutes().then( data => {
        updateRouteList(data);
    });

    $("#newRouteModalSave").on('click', function () {
        console.log($("#submitNewRouteModal").find("#new_route").val())
        let route_name = $("#submitNewRouteModal").find("#new_route").val()

        createRoute(route_name).then(() => {
            getRoutes().then( data => {
                updateRouteList(data);
            });
            $('#newRouteModal').modal('hide');
        });
    });

    $(".dropdown-menu").on('click', ".dropdown-item", function () {
        console.log($(this).text());
        current_selected_route_id = $(this).attr('value');
        current_selected_route_name = $(this).text();
        showRoute(current_selected_route_name);
    });
    
    $("#results").on('click', ".btn-add-poi", function () {
        console.log("clicked",$(this))
        let poi_oid = $(this).attr("oid")
        addPOIToRoute(poi_oid)
    });

    $("#delete_route").on('click', function () {
        deleteRoute(current_selected_route_id, current_selected_route_name).then(() => {
                getRoutes().then( data => {
                    updateRouteList(data);
                });
            });
    });

});