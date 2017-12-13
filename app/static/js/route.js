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
        console.log($("#submitNewRouteModal").find("#new_route").val())
        let route_name = $("#submitNewRouteModal").find("#new_route").val()

        createRoute(route_name).then(() => {
            getRoutes().then(data => {
                updateRouteList(data);
            });
            $('#newRouteModal').modal('hide');
        });
    });

    $(".dropdown-menu").on('click', '.dropdown-item', function () {
        console.log($(this).text());
        current_selected_route_id = $(this).attr('value');
        current_selected_route_name = $(this).text();
        showRoute(current_selected_route_name);

    })


    $("#delete_route").on('click', function () {
        deleteRoute(current_selected_route_id, current_selected_route_name).then(() => {
                getRoutes().then(data => {
                    updateRouteList(data);
                });
            }

        )
    });


    function showRoute(name) {
        let route_name = $("#route-name");
        let route_poi = $("#route-poi-list");

        route_name.empty();
        route_poi.empty();
        route_name.append($("<h1></h1>").text(name));

        getRoutePOI().then(data => {
            
            console.log("poi data", data)

            $.each(data["route"], function (key, value) {
                console.log("data value",value.name)
                route_poi.append($("<li></li>").text(value.name));
                // route_poi.append($("<li></li>").text(value.type));
            });
        });

    }

    function updateRouteList(data) {
        let dropdown = $("#dropdown-menu-items")
        let route_content = $("#route-name")

        route_content.empty();
        dropdown.empty();
        $.each(data["results"], function (key, entry) {
            dropdown.append($("<button class='dropdown-item' type='button'></button>").attr("value", entry.route_id).text(entry.route_name));
        })
    }

});