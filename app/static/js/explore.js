// let mapCell
// let searchCell
// let app

$(document).ready(function () {

    var searchBarTemplate_source = document.getElementById("search-bar-template").innerHTML;
    var searchBarTemplate = Handlebars.compile(searchBarTemplate_source);

    let regionLayer // Will show the region boudaries

    mapCell = {
        $cell: true,
        id: "map",
        _token: "pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA",
        _default_location: [45.18, 5.72],
        _default_zoom: 12,

        _show_location: function (geojson) {
            if (map.hasLayer(regionLayer)) {
                map.removeLayer(regionLayer);
            }

            regionLayer = L.geoJson(JSON.parse(geojson)).addTo(map);
            map.fitBounds(regionLayer.getBounds());
        },

        $init: function () {
            map = L.map('map').setView(this._default_location, this._default_zoom);

            let gl = L.mapboxGL({
                accessToken: this._token,
                style: 'mapbox://styles/mapbox/streets-v9'
            }).addTo(map);

        }
    }

    // POI list factory
    let poi = ["Museum", "Hotel"]

    // let poiItemMaker = function (item) {
    //     const context = {
    //         poiType: item
    //     }
    //     return {
    //         $cell: true,
    //         $type: "label",
    //         class: "btn btn-primary",

    //         $html: [poiSingleOptionsTemplate(context)],

    //         onchange: function () {
    //             val = this.querySelector("#poi-checkbox")
    //             console.log("checkbox clicked", this._locationSearchPOIOptions.push(this.querySelector(".poi-checkbox").getAttribute("value")))
    //         },
    //     }
    // }

    // let poiOptionsCell = {
    //     $cell: true,
    //     $type: "div",
    //     class: "form-group",
    //     id: "poi-options",
    //     _poioptionstest: "test",

    //     $components: [{
    //         $cell: true,
    //         $type: "div",
    //         class: "btn-group",
    //         id: "poi-option-list",

    //         $init: function () {
    //             this.setAttribute("data-toggle", "buttons")

    //         },

    //         $components: poi.map(poiItemMaker)
    //     }]
    // }

    var searchBarCell = {
        $cell: true,
        $type: "div",
        class: "input-group",
        id: "search-bar",

        $html: [searchBarTemplate()],

        $init: function () {
            $("#search-location-input").devbridgeAutocomplete({
                serviceUrl: 'http://127.0.0.1:5000/api/autocomplete',
                minChars: 4,
                deferRequestBy: 200,
                onSelect: function (suggestion) {
                    // this._location = suggestion.value;
                    document.querySelector("#search-cell")._locationUpdate(suggestion)

                }
            })
        }
    }

    //Search options factory
    // let searchZoneOptions = ["City", "Region"]

    // let searchOptionMaker = function (item) {
    //     const context = {
    //         searchZone: item
    //     }
    //     return {
    //         $cell: true,
    //         $type: "label",
    //         class: "btn btn-primary",
    //         $html: [searchSingleOptionTemplate(context)]
    //     }
    // }

    // var searchOptionsCell = {
    //     $cell: true,
    //     $type: "div",
    //     class: "form-group",
    //     id: "search-options",

    //     $components: [{
    //         $cell: true,
    //         $type: "div",
    //         class: "btn-group",
    //         role: "group",
    //         id: "search-option-list",

    //         $init: function () {
    //             this.setAttribute("data-toggle", "buttons")
    //         },

    //         $components: searchZoneOptions.map(searchOptionMaker)
    //     }]
    // }

    searchCell = {
        $cell: true,
        $type: "form",
        id: "search-cell",

        _location: "",
        _locationID: "",
        _locationSearchPOIOptions: ["Test2"],
        _locationSearchOption: "City",

        _location_geojson: "",

        _locationUpdate: function (data) {
            this._location = data.value;
            this._locationID = data.data["location_ID"]
            this._location_geojson = data.data["geojson"]
        },

        _poiUpdate: function (data) {
            this._locationSearchPOIOptions.push(data)
        },



        // $components: [searchBarCell, searchOptionsCell, poiOptionsCell],
        $components: [searchBarCell],

        $update: function () {
            console.log("Location data", this._locationSearchPOIOptions)
            document.querySelector("#map")._show_location(this._location_geojson)

        }
    }



    //App starts here
    app = {
        $cell: true,
        $components: []
    }

});