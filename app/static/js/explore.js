"use strict";

let selected_venues;
let unselected_venues;
let regionLayer;
let POILayer;
let currentLocationID;

$(document).ready(function () {

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

    getRoutes().then(data => {
        updateRouteList(data);
    });

    $("#newRouteModalSave").on('click', function () {
        console.log($("#submitNewRouteModal").find("#new_route").val())
        let route_name = $("#submitNewRouteModal").find("#new_route").val()

        createRoute(route_name).then(() => {
            getRoutes().then(data => {
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
        console.log("clicked", $(this))
        let poi_oid = $(this).attr("oid")
        addPOIToRoute(poi_oid)
    });

    $("#delete_route").on('click', function () {
        deleteRoute(current_selected_route_id, current_selected_route_name).then(() => {
            getRoutes().then(data => {
                updateRouteList(data);
            });
        });
    });

});


function searchResults() {
    if (map.hasLayer(regionLayer)) {
        map.removeLayer(regionLayer);
    }

    currentLocationID = autocomplete_data["location_ID"];
    regionLayer = L.geoJson(JSON.parse(autocomplete_data["geo_json"])).addTo(map);
    map.fitBounds(regionLayer.getBounds());
    $("#venueSelector").show();
    fetchAndShow(selected_venues);
}

function getResults(query, page = 1, per_page = 10) {

    return new Promise(function (resolve, reject) {

        let request_payload = {
            "location_ID": parseInt(currentLocationID),
            "query": query,
            "page": parseInt(page),
            "per_page": parseInt(per_page),
        }

        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/api/getpoi",
            data: {
                parameters: JSON.stringify(request_payload)
            },
            success: successHandler,
            error: errorHandler,
        });

        function successHandler(data, textStatus, xhr) {
            return resolve(data)
        };

        function errorHandler() {
            return reject(new Error("Could not fetch data!"))
        };
    })
};

function showResults(results) {

    $("#results").empty();

    for (let i = 0; i < results.length; i++) {

        let index = i + 1
        $("#results").append($("<li></li>")
            .text(results[i]["properties"]["name"]));
        $("#results").append($("<button></button>")
            .attr("class", "btn btn-primary btn-sm btn-add-poi")
            .attr("type", "button")
            .text("Add attraction"));

    }
};

function paginateResults(total_pages) {

    $('#pagination').twbsPagination('destroy');

    $('#pagination').twbsPagination({
        totalPages: total_pages,
        visiblePages: 7,
        initiateStartPageClick: false,
        onPageClick: function (event, page) {
            fetchAndShow(selected_venues, page, false)
        }
    });

};

function showPOIOnMap(geojson) {
    console.log(geojson)
    if (map.hasLayer(POILayer)) {
        map.removeLayer(POILayer)
    }
    POILayer = L.geoJson(geojson, {
        onEachFeature: onEachFeature
    }).addTo(map);

    // map.fitBounds(POILayer.getBounds());
}

function fetchAndShow(selected_venues, page, paginate = true) {
    if (selected_venues == null) {

    } else {
        getResults(selected_venues, page).then(data => {
            console.log("Data received", data)
            showResults(data["result_geojson"]["features"]);
            showPOIOnMap(data["result_geojson"]["features"]);
            if (paginate === true) {
                paginateResults(data["total_pages"]);
            }

        });
    }
}