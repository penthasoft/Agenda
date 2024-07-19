import datetime
from datetime import datetime
from odoo import api, fields, models, _
import json
from odoo import http
from odoo.http import request, content_disposition
import base64
import os
import werkzeug
import pytz
import calendar
timezone = 'America/Lima'

class ProjectFilter(http.Controller):

    @http.route('/sitrad/filter', auth='public', type='json')
    def project_filter(self, **kwargs):
        # Obtener el parámetro provincia_seleccionada_id del diccionario kwargs
        provincia_seleccionada_id = kwargs.get('provincia_seleccionada_id')

        project_list = []
        comisarias_list = []
        year_list = []
        juzgado_list = []
        month_list  = []
        quarters = []
        
        # Obtener una lista de provincias agrupadas
        provinces = request.env['sitrad.denuncias'].read_group(
            [], ['provincia'], ['provincia'])

        for province in provinces:
            dic = {'name': province['provincia'],
                   'id': province['provincia']}
            project_list.append(dic)

        # Obtener una lista de años distintos
        years = request.env['sitrad.denuncias'].search_read([], ['ctrlpj_fec_den'])
        unique_years = set()
        for record in years:
            if record.get('ctrlpj_fec_den'):
                year = fields.Datetime.from_string(record['ctrlpj_fec_den']).year
                unique_years.add(year)

        year_list = [{'name': str(year), 'id': str(year)} for year in sorted(unique_years)]

        # Obtener los trimestres correspondientes al año seleccionado
        selected_year = kwargs.get('selected_year')
        if selected_year and selected_year != 'null':
            for i in range(1, 13, 3):
                start_month = i
                end_month = i + 2
                quarter_name = f"Q{i//3 + 1} ({calendar.month_abbr[start_month]} - {calendar.month_abbr[end_month]})"
                quarters.append({'name': quarter_name, 'id': f"{str(start_month).zfill(2)}-{str(end_month).zfill(2)}"})

            # Obtener los meses correspondientes al año seleccionado
            months = request.env['sitrad.denuncias'].search_read(
                [('ctrlpj_fec_den', '>=', selected_year + '-01-01 00:00:00'),
                 ('ctrlpj_fec_den', '<=', selected_year + '-12-31 23:59:59')],
                ['ctrlpj_fec_den']
            )
            unique_months = set()
            for record in months:
                if record.get('ctrlpj_fec_den'):
                    month = fields.Datetime.from_string(record['ctrlpj_fec_den']).month
                    unique_months.add(month)
            month_list = [{'name': datetime.strptime(str(month), "%m").strftime("%B"), 'id': str(month).zfill(2)} for month in sorted(unique_months)]

        
        # Realizar una consulta para obtener los registros agrupados por 'comisarias'
        if provincia_seleccionada_id:
            comisarias_domain = [('provincia', '=', provincia_seleccionada_id)]
        else:
            comisarias_domain = []
        comisarias_data = request.env['sitrad.cem'].search_read(
            comisarias_domain, [])

        # Iterar sobre los resultados de la consulta
        for comisaria in comisarias_data:
            # Agregar el nombre del centro (sigla) al listado
            comisarias_list.append({
                'id': comisaria['id'],
                'name': comisaria['sigla'],  # Asumiendo que 'sigla' es el campo que contiene el nombre de la comisaría
                'count': 0  # Ajustar según sea necesario
            })

        # Realizar una consulta para obtener los registros agrupados por 'pjf_juzgado'
        if provincia_seleccionada_id:
            juzgados_domain = [('provincia', '=', provincia_seleccionada_id)]
        else:
            juzgados_domain = []
        juzgados_data = request.env['sitrad.instancias'].search_read(
            juzgados_domain, [])

        # Iterar sobre los resultados de la consulta
        for juzgado in juzgados_data:
            # Agregar el nombre del juzgado al listado
            juzgado_list.append({
                'id': juzgado['id'],
                'name': juzgado['sigla'],  # Asumiendo que 'sigla' es el campo que contiene el nombre del juzgado
                'count': 0  # Ajustar según sea necesario
            })

        return [project_list, comisarias_list, year_list, juzgado_list, month_list, quarters]

class Download_Pdf(http.Controller):
    @http.route('/download_pdf', type='json', auth="public")
    def download_pdf(self, **kwargs):
        # Obtenemos los datos necesarios del frontend
        html_content = kwargs.get('html_content', '')

        # Generamos el PDF utilizando render_qweb_pdf
        pdf_content, _ = request.env['ir.actions.report']._render_qweb_pdf(html_content)

        # Retornamos el PDF como una respuesta para la descarga
        pdf_response = werkzeug.wrappers.Response(
            pdf_content,
            content_type='application/pdf',
            direct_passthrough=True
        )
        pdf_response.headers['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return pdf_response


# class SitradControllerMaps(http.Controller):

#     @http.route('/get_all_cem', type='json', auth='user')
#     def get_all_cem(self):
#         cem_data = http.request.env['sitrad.cem'].get_all_cem()
#         return json.dumps(cem_data)


class SitradFilter(http.Controller):

    @http.route('/sitrad/filterrf', auth='public', type='json')
    def project_filter(self, **kwargs):
        year_list = []
        quarters = []
        month_list = []

        # Obtener una lista de años distintos
        years = request.env['sitrad.denuncias'].search_read([], ['ctrlpj_fec_den'])
        unique_years = set()
        for record in years:
            if record.get('ctrlpj_fec_den'):
                year = fields.Datetime.from_string(record['ctrlpj_fec_den']).year
                unique_years.add(year)

        year_list = [{'name': str(year), 'id': str(year)} for year in sorted(unique_years)]

        # Obtener los trimestres correspondientes al año seleccionado
        selected_year = kwargs.get('selected_year')
        if selected_year and selected_year != 'null':
            for i in range(1, 13, 3):
                start_month = i
                end_month = i + 2
                quarter_name = f"Q{i//3 + 1} ({calendar.month_abbr[start_month]} - {calendar.month_abbr[end_month]})"
                quarters.append({'name': quarter_name, 'id': f"{str(start_month).zfill(2)}-{str(end_month).zfill(2)}"})

            # Obtener los meses correspondientes al año seleccionado
            months = request.env['sitrad.denuncias'].search_read(
                [('ctrlpj_fec_den', '>=', selected_year + '-01-01 00:00:00'),
                 ('ctrlpj_fec_den', '<=', selected_year + '-12-31 23:59:59')],
                ['ctrlpj_fec_den']
            )
            unique_months = set()
            for record in months:
                if record.get('ctrlpj_fec_den'):
                    month = fields.Datetime.from_string(record['ctrlpj_fec_den']).month
                    unique_months.add(month)
            month_list = [{'name': datetime.strptime(str(month), "%m").strftime("%B"), 'id': str(month).zfill(2)} for month in sorted(unique_months)]

        return [year_list, quarters, month_list]

