odoo.define('pj_dashboard.SitradReportCem', function(require) {
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

    var PjSitradCem = AbstractAction.extend({
        template: 'PjSitradCem',
        events: {
            'change #start_year_rf': '_onchangeFilter',
            'change #start_monthrf': '_onchangeFilter',
            'change #start_quarterrf': '_onchangeFilter',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['SitradReportFil', 'SitradReportCem'];
        },

        willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {});
        },

        start: function() {
            var self = this;
            this.set("title", 'Reportes Sitrad CEM Y EE.SS');
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
            self.render_top_cems_graph();
            self.render_top_violencia_graph();
            self.render_top_cs_graph();
            self.render_top_provinciascs_graph();
            self.render_top_cstip_graph();
            self.render_top_intervencionescem_graph();
            self.render_top_intervencion_cs_graph();      
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
                method: 'get_cem_data_true',
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


        render_top_cems_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_cems");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_cems',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Intervenciones",
                        data: denuncias,
                        backgroundColor: "rgba(255, 0, 255, 1)",
                        borderColor: "rgba(255, 0, 255, 0.7)",
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
                if (window.myChart1Cems !== undefined) {
                    window.myChart1Cems.destroy();
                }
                window.myChart1Cems = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_provincias_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_cemprov");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_cemprov',
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
                        label: "Intervenciones",
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
                if (window.myChartProvincias !== undefined) {
                    window.myChartProvincias.destroy();
                }
                window.myChartProvincias = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_violencia_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_tipcem");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_tipcem',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de categorías
                var porcentajes = data.values; // Lista de porcentajes de intervenciones
                var totalDenuncias = data.total_denuncias; // Total de denuncias
                var totalIntervenciones = data.total_intervenciones; // Total de denuncias con al menos una intervención

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Distribución de Intervenciones",
                        data: porcentajes,
                        backgroundColor: ["rgba(255, 0, 255, 1)", "rgba(31, 241, 91,1)"], // Magenta y gris
                        borderColor: ["rgba(255, 0, 255, 0.7)", "rgba(128, 128, 128, 0.7)"], // Magenta y gris con transparencia
                    }]
                };

                var options = {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        datalabels: {
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return value.toFixed(1) + '%'; // Mostrar valores como porcentajes con un decimal
                            },
                            anchor: 'center', // Posiciona las etiquetas de datos dentro de las porciones del pastel
                            align: 'center', // Alinea las etiquetas de datos al principio de las porciones del pastel
                        }
                    },
                };

                // Crear el gráfico usando Chart.js
                if (window.myChartViolencia !== undefined) {
                    window.myChartViolencia.destroy();
                }
                window.myChartViolencia = new Chart(ctx, {
                    type: 'pie',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_cs_graph: function(year, quarters, month_list) {
                var self = this;

                // Obtener el contexto del gráfico
                var ctx = self.$(".top_selling_cs");

                // Hacer una llamada RPC para obtener los datos del servidor
                rpc.query({
                    model: "sitrad.denuncias",
                    method: 'get_top_cs',
                    args: [year, quarters, month_list],
                }).then(function(data) {
                    // Extraer los datos de la respuesta
                    var labels = data.labels; // Lista de provincias
                    var denuncias = data.values; // Lista de número de denuncias

                    // Configurar los datos y opciones del gráfico
                    var chartData = {
                        labels: labels,
                        datasets: [{
                            label: "Intervenciones",
                            data: denuncias,
                            backgroundColor: "rgba(128, 0, 0, 1)",
                            borderColor: "rgba(128, 0, 0, 0.7)",
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
                                        size: 8 // Tamaño de la fuente del eje X
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
                                    size: 10 // Ajusta el tamaño de la fuente de la leyenda
                                }
                            }
                        }
                    };

                    // Crear el gráfico usando Chart.js
                    if (window.myChartComisarias !== undefined) {
                        window.myChartComisarias.destroy();
                    }
                    window.myChartComisarias = new Chart(ctx, {
                        type: 'bar',
                        data: chartData,
                        options: options
                    });
                });
        },

        render_top_provinciascs_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_csprov");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_csprov',
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
                        label: "Intervenciones",
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
                if (window.myChartProvincias1 !== undefined) {
                    window.myChartProvincias1.destroy();
                }
                window.myChartProvincias1 = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_cstip_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_cstip");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_cstip',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de grados
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Especialidad",
                        data: denuncias,
                        backgroundColor: ["rgba(190, 27, 75,1)", "rgba(255, 0, 255, 0.7)", "rgba(255, 0, 0, 1)"],
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
                            color: 'white',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return value.toFixed(1) + '%'; // Personaliza la función para formatear los valores de las etiquetas de datos según tus necesidades
                            },
                            anchor: 'center', // Posiciona las etiquetas de datos dentro de las porciones del pastel
                            align: 'center', // Alinea las etiquetas de datos al principio de las porciones del pastel
                        }
                    },
                };

                // Crear el gráfico usando Chart.js
                if (window.ChartViolencia !== undefined) {
                    window.ChartViolencia.destroy();
                }
                window.ChartViolencia = new Chart(ctx, {
                    type: 'pie',
                    data: chartData,
                    options: options
                });

            });
        },

        render_top_intervencionescem_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".get_top_intervenciones_cem");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_intervenciones_cem',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Meses del año en orden
                var months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

                // Obtener los datos de la respuesta
                var labels = data.months; // Lista de meses
                var denuncias = data.total_denuncias; // Lista de número de denuncias
                var intervenciones = data.total_intervenciones; // Lista de número de intervenciones

                // Crear un objeto para almacenar los datos completos de los meses
                var fullData = {};

                // Iterar sobre los meses y completar los datos
                months.forEach(function(month) {
                    var index = labels.indexOf(month);
                    if (index !== -1) {
                        fullData[month] = {
                            'Denuncias': denuncias[index],
                            'Intervenciones': intervenciones[index]
                        };
                    } else {
                        fullData[month] = {
                            'Denuncias': 0,
                            'Intervenciones': 0
                        };
                    }
                });

                // Construir los arrays de datos completos para el gráfico
                var fullLabels = months;
                var fullDenuncias = fullLabels.map(function(month) {
                    return fullData[month]['Denuncias'];
                });
                var fullIntervenciones = fullLabels.map(function(month) {
                    return fullData[month]['Intervenciones'];
                });

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: fullLabels,
                    datasets: [{
                        label: "Denuncias",
                        data: fullDenuncias,
                        backgroundColor: "rgba(31, 241, 91, 1)",
                        borderColor: "rgba(31, 241, 91, 0.2)",
                        borderWidth: 2,
                        tension: 0.4
                    }, {
                        label: "Intervenciones CEM",
                        data: fullIntervenciones,
                        backgroundColor: "rgba(255, 0, 255, 1)",
                        borderColor: "rgba(255, 0, 255, 0.7)",
                        borderWidth: 2,
                        tension: 0.4
                    }]
                };

                var options = {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
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
                                return Math.round(value); // Mostrar valores sin decimales
                            },
                            anchor: 'end', // Posiciona las etiquetas de datos encima de las barras
                            align: 'end' // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    title: {
                        display: true,
                        position: "bottom",
                        text: "Gráfico de Denuncias e Intervenciones CEM",
                        fontSize: 18,
                        fontColor: "#111"
                    }
                };

                // Crear el gráfico usando Chart.js
                if (window.ChartIntervCem !== undefined) {
                    window.ChartIntervCem.destroy();
                }
                window.ChartIntervCem = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_intervencion_cs_graph: function(year, quarters, month_list) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_interv_cs");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_intervenciones_cs',
                args: [year, quarters, month_list],
            }).then(function(data) {
                // Meses del año en orden
                var months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
                var labels = data.months; // Lista de meses

                // Obtener los datos de la respuesta
                var medidas_proteccion = data.total_medidas_proteccion;
                var facultativo = data.total_facultativo;
                var obligatorio = data.total_obligatorio;
                
                // Crear un objeto para almacenar los datos completos por mes
                var fullData = {};
                months.forEach(function(month) {
                    var index = labels.indexOf(month);
                    if (index !== -1) {
                        fullData[month] = {
                            'Medidas de Protección': medidas_proteccion[index],
                            'Facultativo': facultativo[index],
                            'Obligatorio': obligatorio[index]
                        };
                    } else {
                        fullData[month] = {
                            'Medidas de Protección': 0,
                            'Facultativo': 0,
                            'Obligatorio': 0
                        };
                    }
                });

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: months,
                    datasets: [{
                        label: "Medidas de Protección",
                        data: months.map(month => fullData[month]['Medidas de Protección']),
                        backgroundColor: "rgba(190, 27, 75,1)",
                        borderColor: "rgba(190, 27, 75, 0.2)",
                        borderWidth: 2,
                        tension: 0.4
                    }, {
                        label: "Facultativo",
                        data: months.map(month => fullData[month]['Facultativo']),
                        backgroundColor: "rgba(255, 0, 255, 0.7)",
                        borderColor: "rgba(255, 0, 255, 1)",
                        borderWidth: 2,
                        tension: 0.4,
                        stack: 'Stack 0',
                    }, {
                        label: "Obligatorio",
                        data: months.map(month => fullData[month]['Obligatorio']),
                        backgroundColor: "rgba(255, 0, 0, 0.7)",
                        borderColor: "rgba(255, 0, 0, 1)",
                        borderWidth: 2,
                        tension: 0.4,
                        stack: 'Stack 0',
                    }]
                };

                var options = {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            display: false,
                            stacked: true
                        },
                        x: {
                            stacked: true,
                        },
                    },
                    plugins: {
                        datalabels: {
                            color: 'white',
                            font: {
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                return value.toFixed(0); // Mostrar valores sin decimales
                            },
                            anchor: 'center', // Posiciona las etiquetas de datos encima de las barras
                            align: 'center' // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    title: {
                        display: true,
                        position: "bottom",
                        text: "Medidas de Protección, Facultativo y No Requerido",
                        fontSize: 18,
                        fontColor: "#111"
                    },
                    legend: {
                        display: true,
                        position: "top"
                    }
                };

                // Crear el gráfico usando Chart.js
                if (window.ChartIntervEEss !== undefined) {
                    window.ChartIntervEEss.destroy();
                }
                window.ChartIntervEEss = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        _onchangeFilter: function() {
            var year = $('#start_year_rf').val();
            var month_list = $('#start_monthrf').val();
            var quarters = $('#start_quarterrf').val();
            this.render_top_cems_graph(year, quarters, month_list);
            this.render_top_provincias_graph(year, quarters, month_list);
            this.render_top_violencia_graph(year, quarters, month_list);
            this.render_top_cs_graph(year, quarters, month_list);
            this.render_top_provinciascs_graph(year, quarters, month_list);
            this.render_top_cstip_graph(year, quarters, month_list);
            this.render_top_intervencionescem_graph(year, quarters, month_list);
            this.render_top_intervencion_cs_graph(year, quarters, month_list);
        },

    });

    core.action_registry.add('sitrad_reportcem', PjSitradCem);

    return PjSitradCem;

});
