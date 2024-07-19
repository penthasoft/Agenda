odoo.define('pj_dashboard.SitradReport', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var _t = core._t;
    var session = require('web.session');
    var web_client = require('web.web_client');
    var abstractView = require('web.AbstractView');
     Chart.register(ChartDataLabels);
    // Otros imports necesarios

    var PjSitrad = AbstractAction.extend({
        template: 'PjSitrad',
        events: {
            'change #start_year_rf': '_onchangeFilter',
            'change #start_monthrf': '_onchangeFilter',
            'change #start_quarterrf': '_onchangeFilter',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['SitradReportFil', 'SitradReport'];
        },

        willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {});
        },

        start: function() {
            var self = this;
            this.set("title", 'Reportes Sitrad');
            return this._super().then(function() {
                self.render_dashboards();
                self.render_graphs();
                self.render_filter();
                self.loadCemData();
            });
        },

        render_dashboards: function() {
            var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_pj_dashboard').append(QWeb.render(template, {
                    widget: self
                }));
            });
        },

        render_filter: function() {
            // Realizar la solicitud RPC para obtener los datos iniciales
            ajax.rpc('/sitrad/filterrf').then(function(data) {
                var years = data[0];
                var quarters = data[1];
                var months = data[2];
                // Agregar opciones de años
                $(years).each(function(index, year) {
                    $('#start_year_rf').append("<option value='" + year.id + "'>" + year.name + "</option>");
                });

                $('#start_year_rf').on('change', function() {
                    var selectedYear = $(this).val();
                    $('#start_monthrf').empty();  // Limpiar las opciones de meses
                    $('#start_quarterrf').empty();  // Limpiar las opciones de trimestres
                    if (selectedYear) {
                        ajax.rpc('/sitrad/filterrf', {
                            selected_year: selectedYear
                        }).then(function(data) {
                            var months = data[2];
                            var quarters = data[1];
                            $('#start_monthrf').append("<option value='null'>Todos</option>");
                            $(months).each(function(index, month) {
                                $('#start_monthrf').append("<option value='" + month.id + "'>" + month.name + "</option>");
                            });
                            $('#start_quarterrf').append("<option value='null'>Todos</option>");
                            $(quarters).each(function(index, quarter) {
                                $('#start_quarterrf').append("<option value='" + quarter.id + "'>" + quarter.name + "</option>");
                            });
                        });
                    }
                });
            });
        },

        render_graphs: function() {
            var self = this;
            self.render_top_provincias_graph();
            self.render_top_comisarias_graph();
            self.render_top_juzgado_graph();
            self.render_top_grado_graph();
            self.render_top_violencia_graph();
            
        },

        on_reverse_breadcrumb: function() {
            var self = this;
            web_client.do_push_state({});
            this.then(function() {
                self.$('.o_pj_dashboard').empty();
                self.render_dashboards();
                self.render_graphs();
            });
        },

        loadCemData: function() {
            var self = this;
            rpc.query({
                model: 'sitrad.cem',
                method: 'get_cem_data',
                args: [],
            }).then(function(result) {
                self.initMap(result);
            }).catch(function(error) {
                console.error('Error fetching CEM data:', error);
            });
        },

        initMap: function(cemData) {
            async function initMap() {
                const mapContainer = document.getElementById("map");
                if (!mapContainer) {
                    console.error('Contenedor del mapa no encontrado');
                    return;
                }

                const map = new google.maps.Map(mapContainer, {
                    center: { lat: -17.5255638, lng: -70.7688586 },
                    zoom: 7,
                    mapId: "map", // Usa tu propio ID de mapa aquí
                    scrollwheel: false // Deshabilitar el zoom con el scroll del mouse
                });

                const iconBase = '/sitrad/static/description/';  // Ruta donde está tu imagen personalizada
                const icon = {
                    url: iconBase + 'pnp_ubi.png',  // URL completa de tu imagen personalizada
                    scaledSize: new google.maps.Size(52, 52),  // Tamaño del ícono (ajústalo según sea necesario)
                };

                const markers = [];
                const infoWindows = [];

                cemData.forEach(function(cem) {
                    const lat = parseFloat(cem.latitude);
                    const lng = parseFloat(cem.longitude);

                    if (!isNaN(lat) && !isNaN(lng)) {
                        const marker = new google.maps.Marker({
                            position: { lat: lat, lng: lng },
                            map: map,
                            title: "VER MÁS..",
                            icon: icon,  // Establecer la imagen personalizada como ícono del marcador
                            animation: google.maps.Animation.BOUNCE  // Añadir animación de rebote
                        });

                        const infoWindow = new google.maps.InfoWindow({
                            content: `
                            <div class="custom-infowindow">
                                <b>${cem.name}</b><br>
                                Dirección: ${cem.direccion}<br>
                                Télefono: ${cem.tel}<br>
                                Referencia: ${cem.direc}<br>
                            </div>`,
                        });

                        marker.addListener("click", function() {
                            infoWindow.open(map, marker);
                        });

                        markers.push({ marker, cem });
                        infoWindows.push(infoWindow);
                    } else {
                        console.error('Latitud o longitud inválidas para CEM:', cem);
                    }
                });

                const bounds = new google.maps.LatLngBounds();
                markers.forEach(function(markerObj) {
                    const lat = parseFloat(markerObj.cem.latitude);
                    const lng = parseFloat(markerObj.cem.longitude);

                    if (!isNaN(lat) && !isNaN(lng)) {
                        bounds.extend({ lat: lat, lng: lng });
                    }
                });
                map.fitBounds(bounds);

                // Servicio de Directions
                const directionsService = new google.maps.DirectionsService();
                const directionsRenderer = new google.maps.DirectionsRenderer({
                    polylineOptions: {
                        strokeColor: 'red',  // Color de la línea de la ruta
                        strokeWeight: 4      // Grosor de la línea de la ruta
                    }
                });
                directionsRenderer.setMap(map);

                // Función para encontrar la comisaría más cercana
                function findNearestComisaria(position) {
                    const userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

                    let nearestMarker = null;
                    let shortestDistance = Infinity;

                    markers.forEach(function(markerObj) {
                        const markerPosition = markerObj.marker.getPosition();
                        const distance = google.maps.geometry.spherical.computeDistanceBetween(userLocation, markerPosition);

                        if (distance < shortestDistance) {
                            shortestDistance = distance;
                            nearestMarker = markerObj;
                        }
                    });

                    if (nearestMarker) {
                        map.setCenter(nearestMarker.marker.getPosition());
                        map.setZoom(14); // Zoom in to the nearest marker
                        infoWindows.forEach(function(iw) {
                            iw.close();
                        });
                        const infoWindow = new google.maps.InfoWindow({
                            content: `
                            <div class="custom-infowindow">
                                <b>${nearestMarker.cem.name}</b><br>
                                Dirección: ${nearestMarker.cem.direccion}<br>
                                Télefono: ${nearestMarker.cem.tel}<br>
                                Referencia: ${nearestMarker.cem.direc}<br>
                            </div>`
                        });
                        infoWindow.open(map, nearestMarker.marker);

                        // Calcular y mostrar la ruta
                        directionsService.route({
                            origin: userLocation,
                            destination: nearestMarker.marker.getPosition(),
                            travelMode: google.maps.TravelMode.DRIVING
                        }, function(response, status) {
                            if (status === google.maps.DirectionsStatus.OK) {
                                directionsRenderer.setDirections(response);
                            } else {
                                console.error('Direcciones fallaron debido a ' + status);
                            }
                        });
                    }
                }

                // Event listener para el botón
                document.getElementById("find-nearest").addEventListener("click", function() {
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(findNearestComisaria, function(error) {
                            console.error("Error al obtener la ubicación:", error);
                        });
                    } else {
                        console.error("Geolocalización no es soportada por este navegador.");
                    }
                });
            }

            // Carga el script de Google Maps con la clave de API
            if (!window.google || !window.google.maps) {
                var script = document.createElement('script');
                script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyAhYWVml_4c9iOpsFUlKbyFQvcXEIUpq9Q&callback=initMap&libraries=geometry,places`;
                script.async = true;
                document.head.appendChild(script);
            } else {
                initMap();
            }
        },


        render_top_provincias_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_provincias");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_provincia',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los colores para las barras
                var colors = ["rgba(255, 0, 0, 1)", "rgba(255, 0, 255, 1)", "rgba(255, 128, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"];

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Denuncias",
                        data: denuncias,
                        backgroundColor: "rgba(31, 241, 91,1)",
                        borderColor: "rgba(31, 241, 91, 0.7)",
                        borderWidth: 4,
                        tension: 0.4
                    }]
                };

                var options = {
                    responsive: true,
                    scales: {
                        y: {
                            display: false
                        }
                    },
                    plugins: {
                        datalabels: {
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return Math.round(value); // Personaliza la función para formatear los valores de las etiquetas de datos según tus necesidades
                            },
                            anchor: 'end', // Posiciona las etiquetas de datos encima de las barras
                            align: 'end', // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    legend: {
                        display: false // Ocultar la leyenda
                    }
                };

                // Crear el gráfico usando Chart.js
                if (window.provinciasChart !== undefined) {
                    window.provinciasChart.destroy();
                }
                window.provinciasChart = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_comisarias_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_comisarias");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_comisarias',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de comisarías
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Denuncias",
                        data: denuncias,
                        backgroundColor: "rgba(31, 241, 91,1)",
                        borderColor: "rgba(31, 241, 91, 0.7)",
                        borderWidth: 4,
                        tension: 0.4
                    }]
                };

                var options = {
                    responsive: true,
                    scales: {
                        y: {
                            display: false
                        },
                        x: { // Configuración específica para el eje X
                            ticks: {
                                font: {
                                    size: 9 // Tamaño de la fuente del eje X
                                }
                            }
                        }
                    },
                    plugins: {
                        datalabels: {
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return Math.round(value); // Personaliza la función para formatear los valores de las etiquetas de datos según tus necesidades
                            },
                            anchor: 'end', // Posiciona las etiquetas de datos encima de las barras
                            align: 'end', // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    legend: {
                        display: true, // Mostrar la leyenda
                        labels: {
                            font: {
                                size: 12 // Ajusta el tamaño de la fuente de la leyenda
                            }
                        }
                    }
                };

                // Crear el gráfico usando Chart.js
                if (window.comisariasChart !== undefined) {
                    window.comisariasChart.destroy();
                }
                window.comisariasChart = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },


        render_top_juzgado_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_juzgado");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_medidas',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Medidas",
                        data: denuncias,
                        backgroundColor: ["rgba(190, 27, 75,0.5)", "rgba(255, 128, 0, 1)", "rgba(255, 255, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"],
                        borderColor: "rgba(190, 27, 75,0.7)",
                        borderWidth: 4,
                        tension: 0.4
                    }]
                };

                var options = {
                    responsive: true,
                    scales: {
                        y: {
                            display: false
                        }
                    },
                    plugins: {
                        datalabels: {
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return Math.round(value); // Personaliza la función para formatear los valores de las etiquetas de datos según tus necesidades
                            },
                            anchor: 'end',
                            align: 'end',
                        }
                    },
                };

                // Crear el gráfico usando Chart.js
                if (window.juzgadosChart !== undefined) {
                    window.juzgadosChart.destroy();
                }
                window.juzgadosChart = new Chart(ctx, {
                    type: 'line',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_grado_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_grado");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_grado',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de grados
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Gravedad",
                        data: denuncias,
                        backgroundColor: ["rgba(190, 27, 75,0.5)", "rgba(255, 128, 0, 1)", "rgba(255, 255, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"],
                        borderColor: "rgba(190, 27, 75,0.7)",
                        borderWidth: 4,
                        tension: 0.4
                    }]
                };

                var options = {
                    responsive: true,
                    scales: {
                        y: {
                            display: false
                        }
                    },
                    plugins: {
                        datalabels: {
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return Math.round(value); // Personaliza la función para formatear los valores de las etiquetas de datos según tus necesidades
                            },
                            anchor: 'end', // Posiciona las etiquetas de datos dentro de las porciones del pastel
                            align: 'end', // Alinea las etiquetas de datos al principio de las porciones del pastel
                        }
                    },
                    // legend: {
                    //     display: true, // Mostrar la leyenda
                    //     position: 'right' // Posición de la leyenda
                    // }
                };

                // Crear el gráfico usando Chart.js
                if (window.gradoChart !== undefined) {
                    window.gradoChart.destroy();
                }
                window.gradoChart = new Chart(ctx, {
                    type: 'line',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_violencia_graph: function(year, quarters, month_list) {
            var self = this;
            var ctx = self.$(".top_selling_violencia");
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_forma',
                args: [year, quarters, month_list],
            }).then(function(data) {
                var labels = data.labels;
                var denuncias = data.values;
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Tipo de Violencia",
                        data: denuncias,
                        backgroundColor: ["rgba(190, 27, 75,0.5)", "rgba(255, 128, 0, 1)", "rgba(255, 255, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"],
                        borderColor: "rgba(190, 27, 75,0.7)",
                        borderWidth: 4,
                        tension: 0.4
                    }]
                };

                var options = {
                    responsive: true,
                    scales: {
                        y: {
                            display: false
                        }
                    },
                    plugins: {
                        datalabels: {
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return Math.round(value);
                            },
                            anchor: 'end',
                            align: 'end',
                        }
                    },
                    // legend: {
                    //     display: true, // Mostrar la leyenda
                    //     position: 'right' // Posición de la leyenda
                    // },
                };

                // Crear el gráfico usando Chart.js
                if (window.formaChart !== undefined) {
                    window.formaChart.destroy();
                }
                window.formaChart = new Chart(ctx, {
                    type: 'line',
                    data: chartData,
                    options: options
                });
            });
        },

        _onchangeFilter: function() {
            var year = $('#start_year_rf').val();
            var month_list = $('#start_monthrf').val();
            var quarters = $('#start_quarterrf').val();
            this.render_top_provincias_graph(year, quarters, month_list);
            this.render_top_comisarias_graph(year, quarters, month_list);
            this.render_top_juzgado_graph(year, quarters, month_list);
            this.render_top_grado_graph(year, quarters, month_list);
            this.render_top_violencia_graph(year, quarters, month_list);
        },

    });
    core.action_registry.add('sitrad_report', PjSitrad);
    return PjSitrad;
});
