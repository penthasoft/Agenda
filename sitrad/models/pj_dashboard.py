import calendar
import random
import pytz
from datetime import datetime
from calendar import monthrange
from statistics import mean
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class PosDashboard(models.Model):
    _inherit = 'sitrad.denuncias'
    
    @api.model
    def get_tiles_data(self, year, project_selection, juggados_selection, comisaria_list, month_list, quarters):
        filters = []
        crtlv_contador_values = 0
        crtlpj_contador_values = 0
        crtlpjp_general_values = 0
        total_projects = 0
        total_time = 0
        total_general = 0
        project_stage_list = 0

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))
    

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))
        
        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlpj_fec_den', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-28 23:59:59'))

        if project_selection =='null' or project_selection ==None:
            print('no hay dato2')
        else:
            filters.append(('provincia', '=', project_selection))

        if juggados_selection == 'null' or juggados_selection ==None:
            print('no hay dato3')
        else:
            filters.append(('pjf_juzgado.id', '=', juggados_selection))

        if comisaria_list == 'null' or comisaria_list ==None:
            print('no hay dato4')
        else:
            filters.append(('comisarias.id', '=', comisaria_list))

        all_projects = self.env['sitrad.denuncias'].search(filters)
        
        crtlv_contador_values = all_projects.mapped('crtlv_contador')
        crtlpj_contador_values = all_projects.mapped('crtlpj_contador')
        crtlpjp_general_values = all_projects.mapped('crtlpjp_general')
        crtlpjp_general_notifi = all_projects.mapped('crtlmp_contador')
        

        total_projects = round(sum(crtlv_contador_values) / len(crtlv_contador_values), 0) if crtlv_contador_values else 0
        total_time = round(sum(crtlpj_contador_values) / len(crtlpj_contador_values), 0) if crtlpj_contador_values else 0
        project_stage_list = round(sum(crtlpjp_general_notifi) / len(crtlpjp_general_notifi), 0) if crtlpjp_general_notifi else 0
        # total_general = (round(total_projects,0) + round(total_time,0) + round(project_stage_list,0))
        total_general = (round(total_projects,0) + round(total_time,0))

        return {
            'total_projects': total_projects,
            'total_hours': total_time,
            'project_stage_list': project_stage_list,
            'total_general': total_general,
        }


    @api.model
    def get_top_timesheet_employees(self, year, project_selection, juggados_selection, comisaria_list, month_list, quarters):
        filters = []

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlpj_fec_den', '>=', f'{year}-{month.zfill(2)}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month.zfill(2)}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month.zfill(2)}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month.zfill(2)}-29 23:59:59'))
                    else:
                        filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month.zfill(2)}-28 23:59:59'))

        # Verificar y agregar filtros de selección de proyecto, juzgados y comisarías
        if project_selection != 'null' and project_selection is not None:
            filters.append(('provincia', '=', project_selection))
        if juggados_selection != 'null' and juggados_selection is not None:
            filters.append(('pjf_juzgado', '=', juggados_selection))
        if comisaria_list != 'null' and comisaria_list is not None:
            filters.append(('comisarias', '=', comisaria_list))

        # Convertir los filtros a cláusulas SQL
        where_clauses = []
        for (field, operator, value) in filters:
            if operator == '=':
                where_clauses.append(f"{field} {operator} '{value}'")
            else:
                where_clauses.append(f"{field} {operator} '{value}'")

        # Construir la cláusula WHERE solo si hay filtros definidos
        where_clause = ""
        if where_clauses:
            where_clause = "WHERE " + " AND ".join(where_clauses)

        # Construir la consulta SQL
        query = f'''
            SET timezone = 'America/Lima';
            SELECT 
                CASE 
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 1 THEN 'Ene'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 2 THEN 'Feb'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 3 THEN 'Mar'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 4 THEN 'Abr'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 5 THEN 'May'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 6 THEN 'Jun'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 7 THEN 'Jul'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 8 THEN 'Ago'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 9 THEN 'Sep'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 10 THEN 'Oct'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 11 THEN 'Nov'
                    WHEN EXTRACT(MONTH FROM ctrlv_fec_rempj) = 12 THEN 'Dic'
                    ELSE 'S/F'
                END as mes,
                COUNT(*) as denuncias,
                COUNT(*) FILTER (WHERE ctrlpj_fec_rempj IS NOT NULL) as medidas_proteccion
            FROM 
                sitrad_denuncias
            {where_clause}
            GROUP BY 
                EXTRACT(MONTH FROM ctrlv_fec_rempj)
            ORDER BY 
                EXTRACT(MONTH FROM ctrlv_fec_rempj) ASC;
        '''
        
        # Ejecutar la consulta SQL
        self._cr.execute(query)
        top_product = self._cr.dictfetchall()

        # Procesar los resultados de la consulta
        unit = [record.get('mes') for record in top_product]
        employee = [record.get('denuncias') for record in top_product]
        medprot = [record.get('medidas_proteccion') for record in top_product]

        return [unit, employee, medprot]



    @api.model
    def get_denuncias_data(self, year, project_selection, juggados_selection, comisaria_list, month_list, quarters):

        filters = []


        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))
    

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlpj_fec_den', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))
        
        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlpj_fec_den', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-28 23:59:59'))


        if project_selection =='null' or project_selection ==None:
            print('no provincia')
        else:
           filters.append(('provincia', '=', project_selection))

        
        if juggados_selection == 'null' or juggados_selection ==None:
            print('no hay juzgado')
        else:
           filters.append(('pjf_juzgado.id', '=', juggados_selection))
        
        if comisaria_list == 'null' or comisaria_list ==None:
            print('no hay comisaria')
        else:
            filters.append(('comisarias.id', '=', comisaria_list))

        denuncias = self.env['sitrad.denuncias'].search(filters)
        denuncias_data = []
        for denuncia in denuncias:
            # Convertir las fechas al formato de zona horaria correcto
            ctrlv_fec_den = denuncia.ctrlv_fec_den.astimezone(pytz.timezone('America/Lima')) if denuncia.ctrlv_fec_den else None
            ctrlv_fec_rempj = denuncia.ctrlv_fec_rempj.astimezone(pytz.timezone('America/Lima')) if denuncia.ctrlv_fec_rempj else None
            ctrlpj_fec_den = denuncia.ctrlpj_fec_den.astimezone(pytz.timezone('America/Lima')) if denuncia.ctrlpj_fec_den else None
            ctrlpj_fec_rempj = denuncia.ctrlpj_fec_rempj.astimezone(pytz.timezone('America/Lima')) if denuncia.ctrlpj_fec_rempj else None
            ctrlmp_fec_den = denuncia.ctrlmp_fec_den.astimezone(pytz.timezone('America/Lima')) if denuncia.ctrlmp_fec_den else None

            denuncia_data = {
                'provincia': denuncia.provincia,
                'comisarias': denuncia.comisarias.sigla,
                'ctrlv_fec_den': ctrlv_fec_den,
                'ctrlv_fec_rempj': ctrlv_fec_rempj,
                'crtlv_contador': denuncia.crtlv_contador,
                'pjf_juzgado': denuncia.pjf_juzgado.sigla,
                'pjf_exp': denuncia.pjf_exp,
                'ctrlpj_fec_den': ctrlpj_fec_den,
                'ctrlpj_fec_rempj': ctrlpj_fec_rempj,
                'crtlpj_contador': denuncia.crtlpj_contador,
                'ctrlmp_fec_den': ctrlmp_fec_den,
                'crtlmp_contador': denuncia.crtlmp_contador,
                'pjf_med_prot_pdf': denuncia.pjf_med_prot_pdf,
                'pjf_med_prot': denuncia.pjf_med_prot,
                'cem_legal': denuncia.cem_legal,
                'cem_psicologica': denuncia.cem_psicologica,
                'cem_tsocial': denuncia.cem_tsocial,
                'sld_rqr': denuncia.sld_rqr,
                'url_medida': denuncia.url_medida,
                'pjf_btn_pnc': denuncia.pjf_btn_pnc,
                'pjf_acm': denuncia.pjf_acm,
                'crtlpjp_general': denuncia.crtlpjp_general,
                'url_medida': denuncia.url_medida,
            }
            denuncias_data.append(denuncia_data)

        return {
            'denuncias': denuncias_data
        }