var csrf_token = "{{ 'csrf_token()' }}"; // the token is set by Jinja2

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token); // insert custom header
        }
    }
});
$(document).ready(function () {

    getRoutes();

    $("#newRouteModalSave").on('click', function () {
        console.log($("#submitNewRouteModal").find("#new_route").val())
        let route_name = $("#submitNewRouteModal").find("#new_route").val()

        createRoute(route_name).then(() => {
            getRoutes();
            $('#newRouteModal').modal('hide')
        });       
    });

    function getRoutes() {
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

            let dropdown = $('#route_list');

            dropdown.empty();
            $.each(data["results"], function (key, entry) {
                dropdown.append($('<option></option>').attr('value', entry.route_id).text(entry.route_name));
            })

            return true
        };

        function getRoutesErrorHandler() {
            error = new Error("Could not fetch data!")
            return error
        };

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

});