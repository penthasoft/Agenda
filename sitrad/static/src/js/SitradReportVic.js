odoo.define('pj_dashboard.SitradReportVic', function(require) {
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

    var SitradReportVic = AbstractAction.extend({
        template: 'SitradReportVic',
        // Define eventos o acciones específicas para esta página si es necesario

        start: function() {
            var self = this;
            this.set("title", 'Reporte 3 - Víctimas');
            return this._super().then(function() {
                self.render_graphs();
            });
        },

        render_graphs: function() {
            var self = this;
            self.render_top_provvic_graph();
            self.render_top_sexvic_graph();
            self.render_top_genvic_graph();
            self.render_top_vicstatus_graph();
            self.render_top_vicedad_graph();
            self.render_top_distvic_graph();
            self.render_top_hijosvic_graph();
                             
        },

        render_top_provvic_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vicprov");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vicprov',
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
                        label: "Victimas por Provincias",
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
                var myChartProvincias = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_sexvic_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vicsex");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vicsex',
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Victimas por Sexo",
                        data: denuncias,
                        backgroundColor: ["rgba(255, 0, 0, 1)", "rgba(255, 0, 255, 1)", "rgba(255, 128, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"], // Magenta y gris con transparencia
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
                            anchor: 'center', // Posiciona las etiquetas de datos encima de las barras
                            align: 'center', // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    legend: {
                        display: false // Ocultar la leyenda
                    }
                };

                // Crear el gráfico usando Chart.js
                var myChartProvincias = new Chart(ctx, {
                    type: 'pie',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_genvic_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vicgen");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vicgen',
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Victimas por Sexo",
                        data: denuncias,
                        backgroundColor: ["rgba(255, 0, 0, 1)", "rgba(255, 0, 255, 1)", "rgba(255, 128, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"], // Magenta y gris con transparencia
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
                            anchor: 'center', // Posiciona las etiquetas de datos encima de las barras
                            align: 'center', // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    legend: {
                        display: false // Ocultar la leyenda
                    }
                };

                // Crear el gráfico usando Chart.js
                var myChartProvincias = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_vicstatus_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vicsstatus");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vicestado',
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Victimas por Estado Civil",
                        data: denuncias,
                        backgroundColor: "rgba(0, 128, 255, 1)", // Magenta y gris
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
                var myChartProvincias = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_vicedad_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vicedad");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vicedad',
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Victimas por Edad",
                        data: denuncias,
                        backgroundColor: "rgba(255, 128, 0, 1)", // Magenta y gris
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
                var myChartProvincias = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },


        render_top_distvic_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vicdist");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vicedistrito',
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
                        label: "Victimas por Provincias",
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
                var myChartProvincias = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: options
                });
            });
        },

        render_top_hijosvic_graph: function() {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_vichijos");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_vichijos',
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var labels = data.labels; // Lista de provincias
                var denuncias = data.values; // Lista de número de denuncias

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: labels,
                    datasets: [{
                        label: "Victimas Indirectas",
                        data: denuncias,
                        backgroundColor: ["rgba(255, 128, 0, 1)", "rgba(0, 128, 255, 1)", "rgba(128, 255, 0, 1)"], // Magenta y gris con transparencia
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
                            anchor: 'center', // Posiciona las etiquetas de datos encima de las barras
                            align: 'center', // Alinea las etiquetas de datos al final de las barras
                        }
                    },
                    legend: {
                        display: false // Ocultar la leyenda
                    }
                };

                // Crear el gráfico usando Chart.js
                var myChartProvincias = new Chart(ctx, {
                    type: 'pie',
                    data: chartData,
                    options: options
                });
            });
        },

    });

    core.action_registry.add('sitrad_reportvic', SitradReportVic);

    return SitradReportVic;

});
