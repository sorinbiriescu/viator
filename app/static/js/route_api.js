let current_selected_route_id
let current_selected_route_name

function getRoutes() {

    return new Promise(function (resolve, reject) {
        $.ajax({
            url: "http://127.0.0.1:5000/api/route",
            type: "GET",
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            dataType: "json",
            success: getRoutesSuccessHandler,
            error: getRoutesErrorHandler,
            complete: () => {}
        });

        function getRoutesSuccessHandler(data, textStatus, xhr) {

            return resolve(data)
        };

        function getRoutesErrorHandler() {
            error = new Error("Could not fetch data!")
            return reject(new Error("Could not fetch data!"))
        };
    });

}

function createRoute(data) {
    return new Promise(function (resolve, reject) {
        let payload = {
            "route_name": data
        }
        $.ajax({
            url: "http://127.0.0.1:5000/api/route",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            dataType: "json",
            success: createRouteSuccessHandler,
            error: createRouteErrorHandler,
            complete: () => {}

        });

        function createRouteSuccessHandler(data, textStatus, xhr) {
            return resolve(true)
        };

        function createRouteErrorHandler() {
            return reject(new Error("Could not fetch data!"))
        };
    });
}

function deleteRoute(route_id, route_name) {
    return new Promise(function (resolve, reject) {

        let payload = {
            "route_id": route_id,
            "route_name": route_name
        }

        $.ajax({
            url: "http://127.0.0.1:5000/api/route",
            type: "DELETE",
            data: JSON.stringify(payload),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            dataType: "json",
            success: deleteRouteSuccessHandler,
            error: deleteRouteErrorHandler,
            complete: () => {}

        });

        function deleteRouteSuccessHandler(data, textStatus, xhr) {
            return resolve(true)
        };

        function deleteRouteErrorHandler() {
            return reject(new Error("Could not fetch data!"))
        };

    });
}

function addPOIToRoute(poi_oid, route_id = current_selected_route_id) {
    return new Promise(function (resolve, reject) {

        let payload = {
            "route_id": route_id,
            "poi_id": poi_oid
        }

        $.ajax({
            url: "http://127.0.0.1:5000/api/route_poi",
            type: "PUT",
            data: JSON.stringify(payload),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            dataType: "json",
            success: addPOITorouteSuccessHandler,
            error: addPOITorouteErrorHandler,
            complete: () => {}

        });

        function addPOITorouteSuccessHandler(data, textStatus, xhr) {
            return resolve(true)
        };

        function addPOITorouteErrorHandler() {
            return reject(new Error("Could not fetch data!"))
        };

    });
}

function removePOIFromRoute(poi_pos, route_id = current_selected_route_id) {
    return new Promise(function (resolve, reject) {

        let payload = {
            "poi_pos": poi_pos,
            "route_id": route_id
        }

        $.ajax({
            url: "http://127.0.0.1:5000/api/route_poi",
            type: "DELETE",
            data: JSON.stringify(payload),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            dataType: 'text',
            success: removePOIFromRouteSuccessHandler,
            error: removePOIFromRouteErrorHandler

        });

        function removePOIFromRouteSuccessHandler(data, textStatus, xhr) {
            return resolve(true)
        };

        function removePOIFromRouteErrorHandler() {
            return reject(new Error("Could not fetch data!"))
        };

    });
}

function getRoutePOI(route_id = current_selected_route_id) {
    return new Promise(function (resolve, reject) {

        let payload = {
            "route_id": route_id
        }

        $.ajax({
            url: "http://127.0.0.1:5000/api/route_poi",
            type: "GET",
            data: payload,
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr) {
                if (xhr && xhr.overrideMimeType) {
                    xhr.overrideMimeType("application/json;charset=utf-8");
                }
            },
            success: getRoutePOISuccessHandler,
            error: getRoutePOIErrorHandler,
            complete: () => {}

        });

        function getRoutePOISuccessHandler(data, textStatus, xhr) {
            return resolve(data)
        };

        function getRoutePOIErrorHandler() {
            return reject(new Error("Could not fetch data!"))
        };

    });

}

function showRoute(name) {
    let route_name = $("#route-name");

    route_name.empty();
    route_name.append($("<h1></h1>").text(name));

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