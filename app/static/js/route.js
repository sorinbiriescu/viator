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

    getRoutes().then(data => {
        updateRouteList(data);
    })

    $("#newRouteModalSave").on('click', function () {

        let route_name = $("#submitNewRouteModal").find("#new_route").val()

        createRoute(route_name).then(() => {
            getRoutes().then(data => {
                updateRouteList(data);
            });
            $('#newRouteModal').modal('hide');
        });
    });

    $(".dropdown-menu").on('click', '.dropdown-item', function () {

        current_selected_route_id = $(this).attr('value');
        current_selected_route_name = $(this).text();
        showRoute(current_selected_route_name);
        showRoutePOI();
    })


    $("#delete_route").on('click', function () {
        deleteRoute(current_selected_route_id, current_selected_route_name).then(() => {
                getRoutes().then(data => {
                    updateRouteList(data);
                });
            }

        )
    });

    $("#route-poi-list").on('click', ".btn-rem-poi", function () {

        let poi_pos = $(this).prevAll("li").first().attr("pos");

        removePOIFromRoute(poi_pos).then(() => {
            showRoutePOI();
        });
    });

    $("#route-poi-list").on('click', ".btn-move-up-poi", function () {


        let poi_pos = $(this).prevAll("li").first().attr("pos");

        if (parseInt(poi_pos) === 0) {
            console.log("Cannot go any lower than this")

        } else {

            let poi_new_pos = (parseInt(poi_pos) - 1);

            changePOIPosInRoute(poi_pos, poi_new_pos).then(() => {
                showRoutePOI();
            });
        }
    });

    $("#route-poi-list").on('click', ".btn-move-down-poi", function () {


        let poi_pos = $(this).prevAll("li").first().attr("pos");
        let total_number_poi = $("#route-poi-list").find("li").length

        if (parseInt(poi_pos) === total_number_poi - 1) {
            console.log("Cannot go any higher than this")

        } else {

            let poi_new_pos = (parseInt(poi_pos) + 1);

            changePOIPosInRoute(poi_pos, poi_new_pos).then(() => {
                showRoutePOI();
            });
        }
    });

    function showRoutePOI() {
        let route_poi = $("#route-poi-list");
        route_poi.empty();

        getRoutePOI().then(data => {

            $.each(data["route"], function (key, value) {

                route_poi.append($("<li class='li-route-poi'></li>").append($("<h4></h4>").text(value.name)).attr("pos", value.poi_pos));
                // route_poi.append($("<li></li>").text(value.type));
                route_poi.append($("<button type='button' class='btn btn-info btn-sm btn-move-up-poi'>Move up</button>"));
                route_poi.append($("<button type='button' class='btn btn-info btn-sm btn-move-down-poi'>Move down</button>"));
                route_poi.append($("<button type='button' class='btn btn-danger btn-sm btn-rem-poi'>Remove</button>"));
            });

            function getWaypoints(data) {
                let waypoints = []

                $.each(data["route"], function (key, value) {
                    let coordinates = JSON.parse(value.coordinates)
                    waypoints.push(L.latLng(coordinates.coordinates[1], coordinates.coordinates[0]))
                });

                return waypoints
            };

            routingControl.setWaypoints(getWaypoints(data))

        });
    }
});