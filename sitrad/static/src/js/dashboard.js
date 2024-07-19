odoo.define('pj_dashboard.Dashboard', function(require) {
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
    var flag = 0;
    var tot_project = []
    var PjDashboard = AbstractAction.extend({
        template: 'PjDashboard',
        cssLibs: [
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
        ],
        jsLibs: [
            'https://html2canvas.hertzen.com/dist/html2canvas.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.3/html2pdf.bundle.min.js',
        ],
        events: {
            'change #start_year': '_onchangeFilter',
            'change #project_selection': '_onchangeFilter',
            'change #juggados_selection': '_onchangeFilter',
            'change #comisaria_list': '_onchangeFilter',
            'change #start_month': '_onchangeFilter',
            'change #start_quarter': '_onchangeFilter',
            'click #downloadPdf': 'downloadPdf',
            'click #downloadTablePdf': 'downloadTablePdf',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['DashboardProject', 'DashboardChart'];
            this.today_sale = [];
        },


        willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {
                return self.fetch_data();
            });
        },

        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_dashboards();
                self.render_graphs();
                self.render_filter();
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
            ajax.rpc('/sitrad/filter').then(function(data) {
                var projects = data[0];
                var comisarias = data[1];
                var years = data[2];
                var juzgados = data[3];

                // Agregar opciones de años
                $(years).each(function(year) {
                    $('#start_year').append("<option value=" + years[year].id + ">" + years[year].name + "</option>");
                });

                $('#start_year').on('change', function() {
                    var selectedYear = $(this).val();
                    var selectedMonth = $('#start_month').val();  // Obtener el mes seleccionado
                    $('#start_month').empty();
                    if (selectedYear) {
                        ajax.rpc('/sitrad/filter', {
                            selected_year: selectedYear,
                            selected_month: selectedMonth  // Agregar el mes seleccionado al objeto enviado al servidor
                        }).then(function(data) {
                            var months = data[4];
                            var quarters = data[5];
                            $('#start_month').append("<option value=null>Todos</option>");
                            $(months).each(function(month) {
                                $('#start_month').append("<option value=" + months[month].id + ">" + months[month].name + "</option>");
                            });
                            $('#start_quarter').empty();
                            $('#start_quarter').append("<option value=null>Todos</option>");
                            $(quarters).each(function(quarter) {
                                $('#start_quarter').append("<option value=" + quarters[quarter].id + ">" + quarters[quarter].name + "</option>");
                            });
                        });
                    }
                });

                // Agregar opciones de proyectos
                $('#project_selection').append("<option value=null>Todos</option>");
                $(projects).each(function(project) {
                    $('#project_selection').append("<option value=" + projects[project].id + ">" + projects[project].name + "</option>");
                });

                // Agregar Juzgados
                $('#juggados_selection').append("<option value=null>Todos</option>");
                $(juzgados).each(function(juzgado) {
                    $('#juggados_selection').append("<option value=" + juzgados[juzgado].id + ">" + juzgados[juzgado].name + "</option>");
                });

                // Agregar Comisarías
                $('#comisaria_list').append("<option value=null>Todos</option>");
                $(comisarias).each(function(comisaria) {
                    $('#comisaria_list').append("<option value=" + comisarias[comisaria].id + ">" + comisarias[comisaria].name + "</option>");
                });

                // Manejar el cambio en la selección de provincia
                $('#project_selection').on('change', function() {
                    var provinciaSeleccionadaId = $(this).val();

                    // Limpiar las opciones anteriores de juzgados y comisarías
                    $('#juggados_selection').empty();
                    $('#comisaria_list').empty();

                    // Agregar la opción "Todos" o null en juzgados_selection y comisaria_list
                    $('#juggados_selection').append("<option value=null>Todos</option>");
                    $('#comisaria_list').append("<option value=null>Todos</option>");

                    // Realizar la solicitud RPC con el ID de la provincia seleccionada
                    ajax.rpc('/sitrad/filter', {
                        provincia_seleccionada_id: provinciaSeleccionadaId
                    }).then(function(data) {
                        var juzgados = data[3];
                        var comisarias = data[1];

                        // Agregar nuevas opciones de juzgados
                        $(juzgados).each(function(juzgado) {
                            $('#juggados_selection').append("<option value=" + juzgados[juzgado].id + ">" + juzgados[juzgado].name + "</option>");
                        });

                        // Agregar nuevas opciones de comisarías
                        $(comisarias).each(function(comisaria) {
                            $('#comisaria_list').append("<option value=" + comisarias[comisaria].id + ">" + comisarias[comisaria].name + "</option>");
                        });
                    });
                });
            });
        },

        render_graphs: function() {
            var self = this;
            self.render_top_employees_graph();

        },

        on_reverse_breadcrumb: function() {
            var self = this;
            web_client.do_push_state({});
            this.fetch_data().then(function() {
                self.$('.o_pj_dashboard').empty();
                self.render_dashboards();
                self.render_graphs();
            });
        },

        render_top_employees_graph: function(year, project_selection, juggados_selection, comisaria_list, month_list, quarters) {
            var self = this;

            // Obtener el contexto del gráfico
            var ctx = self.$(".top_selling_employees");

            // Hacer una llamada RPC para obtener los datos del servidor
            rpc.query({
                model: "sitrad.denuncias",
                method: 'get_top_timesheet_employees',
                args: [year, project_selection, juggados_selection, comisaria_list, month_list, quarters],
            }).then(function(data) {
                // Extraer los datos de la respuesta
                var months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

                // Obtener los datos de la respuesta
                var labels = data[0]; // Lista de fechas
                var denuncias = data[1]; // Lista de número de denuncias
                var medidas_proteccion = data[2]; // Lista de número de medidas de protección

                // Crear un objeto para almacenar los datos completos de los meses
                var fullData = {};

                // Iterar sobre los meses y completar los datos
                months.forEach(function(month) {
                    var index = labels.indexOf(month);
                    if (index !== -1) {
                        fullData[month] = {
                            'Denuncias': denuncias[index],
                            'Medidas de protección': medidas_proteccion[index]
                        };
                    } else {
                        fullData[month] = {
                            'Denuncias': 0,
                            'Medidas de protección': 0
                        };
                    }
                });

                // Construir los arrays de datos completos para el gráfico
                var fullLabels = months;
                var fullDenuncias = fullLabels.map(function(month) {
                    return fullData[month]['Denuncias'];
                });
                var fullMedidasProteccion = fullLabels.map(function(month) {
                    return fullData[month]['Medidas de protección'];
                });

                // Configurar los datos y opciones del gráfico
                var chartData = {
                    labels: fullLabels,
                    datasets: [{
                        label: "Denuncias",
                        data: fullDenuncias,
                        backgroundColor: "rgba(31, 241, 91,1)",
                        borderColor: "rgba(31, 241, 91, 0.2)",
                        borderWidth: 5,
                        tension: 0.4,
                        datalabels: {
                            color: "rgba(31, 241, 91,1)", // Color de las etiquetas de datos
                            anchor: 'end',
                            align: 'end',
                            formatter: function(value) {
                                return Math.round(value);
                            }
                        }
                    }, {
                        label: "Medidas de protección",
                        data: fullMedidasProteccion,
                        backgroundColor: "rgba(190, 27, 75,1)",
                        borderColor: "rgba(190, 27, 75, 0.2)",
                        borderWidth: 5,
                        tension: 0.4,
                        datalabels: {
                            color: "rgba(190, 27, 75,1)", // Color de las etiquetas de datos
                            anchor: 'start',
                            align: 'start',
                            formatter: function(value) {
                                return Math.round(value);
                            }
                        }
                    }]
                };

                var options = {
                    responsive: true,
                    title: {
                        display: true,
                        position: "bottom",
                        // text: "Gráfico de Denuncias y Medidas de Protección",
                        fontSize: 18,
                        fontColor: "#111"
                    },
                    scales: {
                        y: {
                            display: false
                        },
                    },
                    plugins: {
                        datalabels: {
                            font: {
                                weight: 'bold'
                            },
                        },
                    },
                };

                // Crear el gráfico usando Chart.js
                if (window.myChart !== undefined) {
                    window.myChart.destroy();
                }
                window.myChart = new Chart(ctx, {
                    type: 'line',
                    data: chartData,
                    options: options
                });
            });
        },



        _onchangeFilter: function() {
            var year = $('#start_year').val();
            var project_selection = $('#project_selection').val();
            var juggados_selection = $('#juggados_selection').val();
            var comisaria_list = $('#comisaria_list').val();
            var month_list = $('#start_month').val();
            var quarters = $('#start_quarter').val();
            this.render_top_employees_graph(year, project_selection, juggados_selection, comisaria_list, month_list, quarters);
            this.fetch_data(year, project_selection, juggados_selection, comisaria_list, month_list, quarters);
        },


        fetch_data: function(year, project_selection, juggados_selection, comisaria_list, month_list, quarters) {
            var self = this;

            var def1 = this._rpc({
                model: 'sitrad.denuncias',
                method: 'get_tiles_data',
                args: [year, project_selection, juggados_selection, comisaria_list, month_list, quarters],
            }).then(function(result) {
                // Actualizar los valores en los elementos HTML correspondientes
                $('#tot_project').text(result['total_projects']);
                $('#total_hours').text(result['total_hours']);
                $('#project_stage_list').text(result['project_stage_list']);
                $('#total_general').text(result['total_general']);
            });
            
            var def5 = this._rpc({
                model: "sitrad.denuncias",
                method: "get_denuncias_data",
                args: [year, project_selection, juggados_selection, comisaria_list, month_list, quarters],
            }).then(function(res) {
                var denunciasData = res['denuncias'];
                var tableBody = $('#table_denuncias tbody');
                
                // Limpiar contenido existente de la tabla
                tableBody.empty();

                // Inicializar contadores
                var countUrls = 0;
                var countSldRqrObligatorio = 0;
                var countCemParticipaciones = 0;
                var countPjfBtnPnc = 0;

                // Iterar sobre los datos de denuncias y agregar filas a la tabla
                $.each(denunciasData, function(index, denuncia) {
                    var respuesta;
                    if (denuncia.pjf_acm) {
                        respuesta = 'Acum.';
                    } else if (denuncia.pjf_med_prot) {
                        respuesta = 'A lugar';
                    } else {
                        respuesta = 'No ha Lugar';
                    }

                    var sldRqrValue = '-';
                    if (denuncia.sld_rqr === 'Obligatorio') {
                        sldRqrValue = '<i class="fa fa-solid fa-circle" style="color: #42b3ff;"></i>';
                        countSldRqrObligatorio++;
                    }

                    var cemParticipation = denuncia.cem_legal || denuncia.cem_psicologica || denuncia.cem_tsocial ? '<i class="fa fa-solid fa-circle" style="color: red;"></i>' : '-';
                    if (denuncia.cem_legal || denuncia.cem_psicologica || denuncia.cem_tsocial) {
                        countCemParticipaciones++;
                    }

                    if (denuncia.pjf_btn_pnc) {
                        countPjfBtnPnc++;
                    }

                    if (denuncia.url_medida) {
                        countUrls++;
                    }

                    var row = '<tr>' +
                        '<td><center>' + denuncia.provincia + '</center></td>' +
                        '<td><center>' + denuncia.comisarias + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlv_fec_den ? (new Date(denuncia.ctrlv_fec_den).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlv_fec_den).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlv_fec_rempj ? (new Date(denuncia.ctrlv_fec_rempj).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlv_fec_rempj).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>'+
                        '<td style="color: rgba(0, 143, 53)"><center>' + denuncia.crtlv_contador + '</center></td>' +
                        '<td><center>' + denuncia.pjf_juzgado + '</center></td>' +
                        '<td><center>' + denuncia.pjf_exp.substring(0, 17) + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlpj_fec_den ? (new Date(denuncia.ctrlpj_fec_den).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlpj_fec_den).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlpj_fec_rempj ? (new Date(denuncia.ctrlpj_fec_rempj).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlpj_fec_rempj).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>'+
                        '<td style="color: rgba(190, 27, 75,1)"><center>' + denuncia.crtlpj_contador + '</center></td>' +
                        // '<td><center>' + (denuncia.ctrlmp_fec_den ? (new Date(denuncia.ctrlmp_fec_den).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlmp_fec_den).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>'+
                        // '<td style="color: rgba(0, 100, 244,1)"><center>' + denuncia.crtlmp_contador + '</center></td>' +
                        '<td><center>' + (denuncia.url_medida ? '<a href="#" class="download-link" data-url="' + denuncia.url_medida + '"><i class="fa fa-file-alt"></i></a>' : '-') + '</center></td>' +
                        '<td><center>' + cemParticipation + '</center></td>' +
                        '<td><center>' + sldRqrValue + '</center></td>' +
                        '<td><center>' + (denuncia.pjf_btn_pnc ? '<i class="fa fa-solid fa-circle" style="color: #b900ac;"></i>' : '-') + '</center></td>' +
                        '<td><center>' + (respuesta !== '-' ? '<b>' + respuesta + '</b>' : '-') + '</center></td>' +
                        '<td style="color:rgba(255, 51, 11,1)"><center>' + denuncia.crtlpjp_general + '</center></td>' +
                        '</tr>';
                    tableBody.append(row);
                });


                $('.download-link').click(function(e) {
                    e.preventDefault();
                    var urlMedida = $(this).data('url');
                    window.location.href = '/sitrad/download_file?url_medida=' + urlMedida;
                });


                // Calcular sumas para cada columna
                var sumCrtlv = 0;
                var sumCrtlpj = 0;
                var sumCrtlmp = 0;
                var sumCrtlpjp = 0;

                $.each(denunciasData, function(index, denuncia) {
                    sumCrtlv += parseFloat(denuncia.crtlv_contador);
                    sumCrtlpj += parseFloat(denuncia.crtlpj_contador);
                    sumCrtlmp += parseFloat(denuncia.crtlmp_contador);
                    sumCrtlpjp += parseFloat(denuncia.crtlpjp_general);
                });

                // Calcular promedios
                var avgCrtlv = sumCrtlv / denunciasData.length;
                var avgCrtlpj = sumCrtlpj / denunciasData.length;
                var avgCrtlmp = sumCrtlmp / denunciasData.length;
                var avgCrtlpjp = sumCrtlpjp / denunciasData.length;

                // Agregar filas para mostrar los promedios al final de la tabla
                var footerRow = '<tr>' +
                    '<td colspan="4"><center> <b>Promedios</b></center></td>' +
                    '<td style="color: rgba(0, 143, 53)"><center> <b>' + avgCrtlv.toFixed(0) + '</b></center></td>' +
                    '<td colspan="4"></td>' +
                    '<td style="color: rgba(190, 27, 75,1)"><center> <b>' + avgCrtlpj.toFixed(0) + '</b></center></td>' +
                    // '<td colspan="1"></td>' +
                    // '<td style="color: rgba(0, 100, 244,1)"><center> <b>' + avgCrtlmp.toFixed(0) + '</b></center></td>' +
                    '<td style="color: rgba(0, 143, 53)"><center> ' + countUrls + '</center></td>' +
                    '<td style="color: rgba(190, 27, 75,1)"><center> ' + countCemParticipaciones + '</center></td>' +
                    '<td style="color: rgba(0, 100, 244,1)"><center> ' + countSldRqrObligatorio + '</center></td>' +
                    '<td style="color: #b900ac;"><center> ' + countPjfBtnPnc + '</center></td>' +
                    '<td colspan="1"></td>' +
                    '<td style="color:rgba(255, 51, 11,1)"><center> <b>' + avgCrtlpjp.toFixed(0) + '</b></center></td>' +
                    '</tr>';

                // Agregar fila de promedios al final de la tabla
                tableBody.append(footerRow);
            });

            return $.when(def1, def5);

        },

        downloadPdf: function() {
            var self = this;
            document.getElementById('downloadPdf').addEventListener('click', function() {
                // Captura el contenido del canvas como una imagen base64
                var canvas = document.querySelector(".top_selling_employees");
                var canvasImg = canvas.toDataURL("image/png");

                // Obtiene los valores de los elementos HTML
                var totProjectValue = document.getElementById("tot_project").textContent;
                var totalHoursValue = document.getElementById("total_hours").textContent;
                var projectStageListValue = document.getElementById("project_stage_list").textContent;
                var totalGeneralValue = document.getElementById("total_general").textContent;

                // HTML para la sección de gráfico y datos
                var htmlContent = `
                    <div class="row main-section">
                        <div class="col-sm-9 col-lg-9">
                            <center>
                                <h4>Gráfico de Denuncias y Medidas de Protección</h4>
                            </center>
                            <hr/>
                            <div class="selling_product_graph_view">
                                <div class="oh-card text-color" style="background-color:#fff;">
                                   <img src="${canvasImg}" width="100%" height="100%" />
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-3 col-lg-3 tot_projects oh-payslip">
                            <div class="oh-card" style="width: 230px;">
                                <div class="oh-card-body tot_projects">
                                    <div class="stat-widget-one" style="display: flex; background-color: rgba(0, 143, 53);">
                                        <div class="stat-icon"><img src="/sitrad/static/description/pnp.png" style="padding: 20% 5%;height: 100%"/></div>
                                        <div class="stat-head" style="padding: 5%; width: 60%;font-size: 14px;color:#fff"><center><b>Tiempo Denuncias</b></center></div>
                                        <div class="stat_count" style="padding: 4%; width: 30%; color:#fff;" id="tot_project">${totProjectValue}</div>
                                    </div>
                                </div>
                            </div>

                            <div class="oh-card" style="width: 230px;">
                                <div class="oh-card-body tot_projects">
                                    <div class="stat-widget-one" style="display:flex; background-color: rgba(190, 27, 75,1);">
                                        <div class="stat-icon"><img src="/sitrad/static/description/pj.png" style="padding: 20%;height: 100%"/></div>
                                        <div class="stat-head" style="padding: 5%;width: 60%;font-size: 14px;color:#fff"><center><b>Tiempo Resolución</b></center></div>
                                        <div class="stat_count" style="padding: 4%;width: 30%; color:#fff" id="total_hours">${totalHoursValue}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="oh-card" style="width: 230px;">
                                <div class="oh-card-body tot_projects">
                                    <div class="stat-widget-one" style="display:flex; background-color: rgba(190, 27, 75,1);">
                                        <div class="stat-icon"><img src="/sitrad/static/description/pj.png" style="padding: 20%;height: 100%"/></div>
                                        <div class="stat-head" style="padding: 5%;width: 60%;font-size: 14px;color:#fff"><center><strong>Tiempo Notificación</strong></center></div>
                                        <div class="stat_count" style="padding: 4%;width: 30%;color:#fff" id="project_stage_list">${projectStageListValue}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="oh-card" style="width: 230px;">
                                <div class="oh-card-body tot_projects">
                                    <div class="stat-widget-one" style="display:flex; background-color: rgba(255, 51, 11,1);">
                                        <div class="stat-icon"><img src="/sitrad/static/description/icon.png" style="padding: 20%;height: 100%"/></div>
                                        <div class="stat-head" style="padding: 5%;width: 60%;font-size: 14px;color:#fff"><center><strong>Total Tiempo Promedio</strong></center></div>
                                        <div class="stat_count" style="padding: 4%;width: 30%;color:#fff" id="total_general">${totalGeneralValue}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`;

                // Configuración de opciones de html2pdf
                var opt = {
                    margin: 1,
                    filename: 'dashboard.pdf',
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 2 },
                    jsPDF: { unit: 'in', format: 'a4', orientation: 'landscape' }
                };

                // Genera el PDF desde el HTML
                html2pdf().from(htmlContent).set(opt).save();
            });
        },

        downloadTablePdf: function() {
            var self = this;

            // Obtiene los valores de los elementos HTML
            var year = document.getElementById("start_year").value;
            var project_selection = document.getElementById("project_selection").value;
            var juggados_selection = document.getElementById("juggados_selection").value;
            var comisaria_list = document.getElementById("comisaria_list").value;
            var month_list = document.getElementById("start_month").value;
            var quarters = document.getElementById("start_quarter").value;

            // Definir tableBody fuera de la función then para que esté disponible en todo el ámbito de downloadTablePdf
            var tableBody = $('#table_denuncias tbody');

            document.getElementById('downloadTablePdf').addEventListener('click', function() {
            
            var def5 = self._rpc({
                model: "sitrad.denuncias",
                method: "get_denuncias_data",
                args: [year, project_selection, juggados_selection, comisaria_list, month_list, quarters],
            }).then(function(res) {
                var denunciasData = res['denuncias'];
                
                // Limpiar contenido existente de la tabla
                tableBody.empty();

                // Iterar sobre los datos de denuncias y agregar filas a la tabla
                $.each(denunciasData, function(index, denuncia) {
                    var respuesta;
                    if (denuncia.pjf_acm) {
                        respuesta = 'Acum.';
                    } else if (denuncia.pjf_med_prot) {
                        respuesta = 'A lugar';
                    } else {
                        respuesta = 'No ha Lugar';
                    }

                    var row = '<tr>' +
                        '<td><center>' + denuncia.provincia + '</center></td>' +
                        '<td><center>' + denuncia.comisarias + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlv_fec_den ? (new Date(denuncia.ctrlv_fec_den).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlv_fec_den).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlv_fec_rempj ? (new Date(denuncia.ctrlv_fec_rempj).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlv_fec_rempj).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>'+
                        '<td style="color: rgba(0, 143, 53)"><center>' + denuncia.crtlv_contador + '</center></td>' +
                        '<td><center>' + denuncia.pjf_juzgado + '</center></td>' +
                        '<td><center>' + denuncia.pjf_exp.substring(0, 17) + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlpj_fec_den ? (new Date(denuncia.ctrlpj_fec_den).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlpj_fec_den).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlpj_fec_rempj ? (new Date(denuncia.ctrlpj_fec_rempj).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlpj_fec_rempj).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>'+
                        '<td style="color: rgba(190, 27, 75,1)"><center>' + denuncia.crtlpj_contador + '</center></td>' +
                        '<td><center>' + (denuncia.ctrlmp_fec_den ? (new Date(denuncia.ctrlmp_fec_den).toLocaleDateString('es-PE') ? new Date(denuncia.ctrlmp_fec_den).toLocaleDateString('es-PE') : '-') : '-') + '</center></td>'+
                        '<td style="color: rgba(0, 100, 244,1)"><center>' + denuncia.crtlmp_contador + '</center></td>' +
                        '<td><center>' + (denuncia.pjf_btn_pnc ? '<b>✓</b>' : '-') + '</center></td>' +
                        '<td><center>' + (respuesta !== '-' ? '<b>' + respuesta + '</b>' : '-') + '</center></td>' +
                        '<td style="color:rgba(255, 51, 11,1)"><center>' + denuncia.crtlpjp_general + '</center></td>' +
                        '</tr>';
                    tableBody.append(row);
                });

                // Calcular sumas para cada columna
                var sumCrtlv = 0;
                var sumCrtlpj = 0;
                var sumCrtlmp = 0;
                var sumCrtlpjp = 0;

                $.each(denunciasData, function(index, denuncia) {
                    sumCrtlv += parseFloat(denuncia.crtlv_contador);
                    sumCrtlpj += parseFloat(denuncia.crtlpj_contador);
                    sumCrtlmp += parseFloat(denuncia.crtlmp_contador);
                    sumCrtlpjp += parseFloat(denuncia.crtlpjp_general);
                });

                // Calcular promedios
                var avgCrtlv = sumCrtlv / denunciasData.length;
                var avgCrtlpj = sumCrtlpj / denunciasData.length;
                var avgCrtlmp = sumCrtlmp / denunciasData.length;
                var avgCrtlpjp = sumCrtlpjp / denunciasData.length;

                // Agregar filas para mostrar los promedios al final de la tabla
                var footerRow = '<tr>' +
                    '<td colspan="4">Promedio</td>' +
                    '<td style="color: rgba(0, 143, 53)"><center>' + avgCrtlv.toFixed(0) + '</center></td>' +
                    '<td colspan="3"></td>' +
                    '<td style="color: rgba(190, 27, 75,1)"><center>' + avgCrtlpj.toFixed(0) + '</center></td>' +
                    '<td colspan="2"></td>' +
                    '<td style="color: rgba(0, 100, 244,1)"><center>' + avgCrtlmp.toFixed(0) + '</center></td>' +
                    '<td colspan="3"></td>' +
                    '<td style="color:rgba(255, 51, 11,1)"><center>' + avgCrtlpjp.toFixed(0) + '</center></td>' +
                    '</tr>';
                // Agregar fila de promedios al final de la tabla
                tableBody.append(footerRow);
            });

                
            // Obtener el contenido HTML de la tabla
            var tableContent = `<div class="col-xs-12 col-sm-12 col-lg-12 col-md-12">
                                    <div class="hr_notification_head" style="font-size: 15px;text-align: center;padding: 12px 0;color: #fff;font-weight: 300;background:rgba(190, 27, 75,1);margin-bottom: 9px;  position: sticky;top: 0;z-index: 1000;">Detalles de denuncias
                                    </div>
                                    <div class="col-sm-12 col-lg-12" style="padding:0;">
                                            <table class="table table-sm" id="table_denuncias" name="table_denuncias">
                                                <thead style="border: 1px solid black; position: sticky;top: 0;z-index: 1000; background:rgba(255,255,255)">
                                                    <tr style="border: 1px solid black; position: sticky;top: 0;z-index: 1000; background:rgba(255,255,255)">
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Provincia</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Operador</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Denuncia</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Presentación</th>
                                                        <th style="color: rgba(0, 143, 53); border: 1px solid black; text-align: center; vertical-align: middle;">
                                                            <i class="fa fa-clock-o"></i>
                                                        </th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Juzgado</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Expediente</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Recepción</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Pron.Med.P</th>
                                                        <th style="color: rgba(190, 27, 75,1); border: 1px solid black; text-align: center; vertical-align: middle;">
                                                            <i class="fa fa-clock-o"></i>
                                                        </th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Fecha</th>
                                                        <th style="color: rgba(0, 100, 244,1);border: 1px solid black; text-align: center; vertical-align: middle;">
                                                            <i class="fa fa-clock-o"></i>
                                                        </th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Btn. Pánico</th>
                                                        <th style="border: 1px solid black; text-align: center; vertical-align: middle;">Estado</th>
                                                        <th style="color:rgba(255, 51, 11,1);border: 1px solid black; text-align: center; vertical-align: middle;"> 
                                                            <i class="fa fa-clock-o"> Gral.</i>
                                                        </th>
                                                    </tr>
                                                </thead>
                                                ${tableBody.html()}
                                            </table>
                                        </div>
                                    </div>
                                    </div>`;

                    // Configuración de opciones de html2pdf
                    var opt = {
                        margin: [1, 1, 1, 1], // Margen superior, derecho, inferior e izquierdo respectivamente en centímetros
                        filename: 'table_report.pdf',
                        image: { type: 'jpeg', quality: 0.98 },
                        html2canvas: { scale: 2 },
                        jsPDF: { 
                            unit: 'in', 
                            format: 'a4', 
                            orientation: 'landscape',
                            fontSize: 8 // Tamaño de la fuente en puntos
                        }
                    };
                    // Genera el PDF desde el contenido de la tabla
                    html2pdf().from(tableContent).set(opt).save();
                });
            },

        // downloadTablePdf: function() {
        //     var self = this;
        //     document.getElementById('downloadTablePdf').addEventListener('click', function() {
        //         // Obtener el contenido HTML de la tabla
        //         var tableContent = document.getElementById('table_denuncias').outerHTML;

        //         // Configuración de opciones de html2pdf
        //         var opt = {
        //             margin: [1, 1, 1, 1], // Margen superior, derecho, inferior e izquierdo respectivamente en centímetros
        //             filename: 'table_report.pdf',
        //             image: { type: 'jpeg', quality: 0.98 },
        //             html2canvas: { scale: 2 },
        //             jsPDF: { unit: 'in', format: 'a4', orientation: 'landscape' }
        //         };

        //         // Genera el PDF desde el contenido de la tabla
        //         html2pdf().from(tableContent).set(opt).save();
        //     });
        // },


    });

    core.action_registry.add('project_dashboard', PjDashboard);
    return PjDashboard;
});