let regionLayer // Will show the region boudaries
let POILayer // Will show the POI on the map

$(document).ready(function () {

    let searchBarTemplate_source = document.getElementById("search-bar-template").innerHTML;
    let searchBarTemplate = Handlebars.compile(searchBarTemplate_source);

    let poiSingleOptionsTemplate_source = document.getElementById("poi-option-template").innerHTML;
    let poiSingleOptionsTemplate = Handlebars.compile(poiSingleOptionsTemplate_source);

    let poiSingleResultTemplate_source = document.getElementById("poi-result-template").innerHTML;
    let poiSingleResultTemplate = Handlebars.compile(poiSingleResultTemplate_source);

    let paginationItemTemplate_source = document.getElementById("pagination-item-template").innerHTML;
    let paginationItemTemplate = Handlebars.compile(paginationItemTemplate_source);

    let paginationPreviousItemTemplate_source = document.getElementById("pagination-previous-item-template").innerHTML;
    let paginationPreviousItemTemplate = Handlebars.compile(paginationPreviousItemTemplate_source)

    let paginationNextItemTemplate_source = document.getElementById("pagination-next-item-template").innerHTML;
    let paginationNextItemTemplate = Handlebars.compile(paginationNextItemTemplate_source)

    mapCell = {
        $cell: true,
        id: "map",
        class: "align-stretch large-auto",

        _token: "pk.eyJ1Ijoic29yaW5iaXJpZXNjdSIsImEiOiJjajhuYXR1YmcxMXdrMnd1YWZzOG5nNXQwIn0.tY6DQoXnp_V88XSNlF2HdA",
        _default_location: [45.18, 5.72],
        _default_zoom: 12,
        _locationGeoJSON: "",
        _poiGeoJSON: "",

        _updatePOIMarkers: function (geojson) {
            this._poiGeoJSON = geojson
        },

        _updateLocationGeoJSON: function (geojson) {
            this._locationGeoJSON = geojson
        },

        _showLocation: function (geojson) {
            if (map.hasLayer(regionLayer)) {
                map.removeLayer(regionLayer);
            }

            if (geojson !== "") {
                regionLayer = L.geoJson(JSON.parse(geojson)).addTo(map);
                map.fitBounds(regionLayer.getBounds());
            }
        },

        _showPOIMarkers: function (geojson) {

            function onEachFeature(feature, layer) {
                let popupContent = "";
                if (feature.properties && feature.properties.name) {
                    popupContent += feature.properties.name;
                }
                layer.bindPopup(popupContent);
            }

            if (map.hasLayer(POILayer)) {
                map.removeLayer(POILayer)
            }

            if (geojson !== "") {
                POILayer = L.geoJson(geojson, {
                    onEachFeature: onEachFeature
                }).addTo(map);
            }
        },

        $init: function () {
            map = L.map('map').setView(this._default_location, this._default_zoom);

            let gl = L.mapboxGL({
                accessToken: this._token,
                style: 'mapbox://styles/mapbox/streets-v9'
            }).addTo(map);

        },

        $update: function () {
            this._showPOIMarkers(this._poiGeoJSON)
            this._showLocation(this._locationGeoJSON)
        }
    }

    document.querySelector("#options-dropdown-pane").addEventListener("mouseleave", function () {
        $(this).foundation('toggle')
    })

    searchBarCell = {
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
                    document.querySelector("#app")._locationUpdate(suggestion)
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

    // POI list factory
    let poi = ["museum", "hotel"]

    let poiItemMaker = function (item) {
        const context = {
            poi_type: item
        }
        return {
            $html: poiSingleOptionsTemplate(context),

            onchange: function () {

                let checkbox = this.querySelector(".poi-checkbox")
                let checkbox_value = this.querySelector(".poi-checkbox").getAttribute("value")
                let array = document.querySelector("#app")._locationSearchPOIOptions
                document.querySelector("#app")._currentPage = 1

                if ($(checkbox).prop("checked")) {
                    array.push(checkbox_value)
                } else {
                    const index = array.indexOf(checkbox_value)
                    if (index !== -1) {
                        array.splice(index, 1)
                    }

                }
            },

        }
    }

    poiOptionsCell = {
        $cell: true,
        $type: "div",
        class: "large-6 cell",
        id: "poi-options",

        $components: poi.map(poiItemMaker)
    }

    let resultItemMaker = function (item) {
        context = {
            result_name: item["properties"]["name"]
        }

        return {
            class: "card medium-6",
            $html: poiSingleResultTemplate(context)
        }
    }

    resultsCell = {
        $cell: true,
        $type: "div",
        class: "grid-x medium-cell-block-y large-cell-block-y grid-padding-x",
        id: "results",

        _poiResults: "",

        _updateResults: function (geojson) {
            this._poiResults = geojson
        },

        $components: "",

        $update: function () {
            if (this._poiResults !== "") {
                this.$components = this._poiResults.map(resultItemMaker)
            } else {
                this.$components = ""
            }
        }
    }

    let paginationPreviousItemMaker = function (active = true) {
        if (active === false) {
            return {
                $cell: true,
                $type: "li",
                class: "pagination-previous disabled",

                $text: "Previous"
            }
        } else {
            return {
                $cell: true,
                $type: "li",
                class: "pagination-previous",

                $html: paginationPreviousItemTemplate(),

                onclick: function () {
                    this._reducePagination()
                }
            }
        }

    }

    let paginationNextItemMaker = function (active = true) {
        if (active === false) {
            return {
                $cell: true,
                $type: "li",
                class: "pagination-next disabled",

                $text: "Next"
            }
        } else {
            return {
                $cell: true,
                $type: "li",
                class: "pagination-next",

                $html: paginationNextItemTemplate(),

                onclick: function () {
                    this._increasePagination()
                }
            }
        }

    }

    let paginationItemMaker = function (pageNumber, currentPage = false) {
        context = {
            pageNumber: pageNumber
        }
        if (currentPage === true) {
            return {
                $cell: true,
                $type: "li",
                class: "current",
                value: pageNumber,

                $html: pageNumber
            }
        } else {
            return {
                $cell: true,
                $type: "li",
                value: pageNumber,

                $html: paginationItemTemplate(context),

                onclick: function () {
                    let value = this.getAttribute("value")
                    this._requestNewPage(value)
                }
            }
        }
    }

    paginationCell = {
        $cell: true,
        $type: "ul",
        id: "results-pagination",
        class: "pagination",
        role: "navigation",

        _currentPage: "",
        _displayPages: 7,
        _totalPages: "",

        $components: [],

        _updatePagination: function (currentPage, totalPages) {
            this._currentPage = currentPage;
            this._totalPages = totalPages
        },

        _increasePagination: function () {
            value = this._currentPage + 1
            document.querySelector("#app")._updateCurrentPage(value)
        },

        _reducePagination: function () {
            value = this._currentPage - 1
            document.querySelector("#app")._updateCurrentPage(value)
        },

        _requestNewPage: function (value) {
            document.querySelector("#app")._updateCurrentPage(value)
        },

        $update: function () {
            if (this._currentPage === "" ||  this._totalPages === "") {
                this.$components = []
            } else {
                this.$components = [];
                let startPage
                let endPage

                displayMin = Math.min(this._displayPages, this._totalPages)
                displayMid = Math.floor(this._displayPages / 2)

                if (this._currentPage <= displayMid) {
                    startPage = 1
                    endPage = displayMin
                } else if (this._currentPage >= this._totalPages - displayMid) {
                    startPage = Math.max(this._totalPages - this._displayPages, 1)
                    endPage = this._totalPages
                } else {
                    startPage = this._currentPage - displayMid
                    endPage = this._currentPage + displayMid
                }

                if (this._currentPage === 1) {
                    this.$components.push(paginationPreviousItemMaker(false))
                } else {
                    this.$components.push(paginationPreviousItemMaker(true))
                }

                for (let i = startPage; i <= endPage; i++) {
                    if (i === this._currentPage) {
                        this.$components.push(paginationItemMaker(i, true))
                    } else {
                        this.$components.push(paginationItemMaker(i))
                    }
                }

                if (this._currentPage === this._totalPages) {
                    this.$components.push(paginationNextItemMaker(false))
                } else {
                    this.$components.push(paginationNextItemMaker(true))
                }
            }
        }
    }

    //App starts here
    app = {
        $cell: true,
        $type: "div",
        class: "grid-x",
        id: "app",

        _location: "",
        _locationID: "",
        _location_geojson: "",
        _locationSearchPOIOptions: [],
        _locationSearchOption: "",
        _currentPage: 1,
        _perPage: 10,

        _locationUpdate: function (data) {
            this._location = data.value;
            this._locationID = data.data["location_ID"]
            this._location_geojson = data.data["geojson"]
        },

        _updateCurrentPage: function (newPageNumber) {
            this._currentPage = newPageNumber
        },

        _getPOI: function getResults() {
            let request_payload = {
                "location_ID": parseInt(this._locationID),
                "query": this._locationSearchPOIOptions,
                "page": parseInt(this._currentPage),
                "per_page": parseInt(this._perPage),
            }

            return new Promise(function (resolve, reject) {
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
        },

        $update: function () {

            const hasLocationID = this._locationID !== "" ? true : false
            const hasPOIOptions = this._locationSearchPOIOptions.length !== 0 ? true : false

            switch ((hasLocationID, hasPOIOptions)) {
                case (true, true):
                    console.log("Option 1 passed", this._locationID, this._locationSearchPOIOptions);

                    document.querySelector("#map")._updateLocationGeoJSON(this._location_geojson);
                    this._getPOI().then(function (data) {
                        document.querySelector("#map")._updatePOIMarkers(data["result_geojson"]);
                        document.querySelector("#results")._updateResults(data["result_geojson"]["features"]);
                        document.querySelector("#results-pagination")._updatePagination(data["current_page"], data["total_pages"])
                        console.log("results passed", data)
                    })
                    break;

                case (true, false):
                    console.log("Option 2 passed")
                    document.querySelector("#map")._updateLocationGeoJSON(this._location_geojson);
                    document.querySelector("#map")._updatePOIMarkers("");
                    document.querySelector("#results")._updateResults("")
                    document.querySelector("#results-pagination")._updatePagination("", "")
                    break;

                case (false, true):
                    console.log("option 3")
                    break;

                case (false, false):
                    console.log("option 4")
                    break;
            }
        }
    }

});