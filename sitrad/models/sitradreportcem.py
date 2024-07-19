import calendar
import random
import pytz
from datetime import datetime
from calendar import monthrange
from statistics import mean
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class SitradCemsCs(models.Model):
    _inherit = 'sitrad.denuncias'
    
    @api.model
    def get_top_cems(self, year, quarters, month_list):
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
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por cems
        denuncias_por_cems = {}

        # Contar las denuncias por cems
        for denuncia in denuncias:
            cems = denuncia.cem_name
            if cems:
                cems_name = cems.sigla
                if cems_name in denuncias_por_cems:
                    denuncias_por_cems[cems_name] += 1
                else:
                    denuncias_por_cems[cems_name] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_cems = dict(sorted(denuncias_por_cems.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_cems.keys())
        values = list(denuncias_por_cems.values())

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_cemprov(self, year, quarters, month_list):
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
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por cemprov
        denuncias_por_cemprov = {}

        # Contar las denuncias por cemprov
        for denuncia in denuncias:
            if denuncia.cem_legal or denuncia.cem_psicologica or denuncia.cem_tsocial:
                cemprov = denuncia.provincia
                if cemprov:
                        if cemprov in denuncias_por_cemprov:
                            denuncias_por_cemprov[cemprov] += 1
                        else:
                            denuncias_por_cemprov[cemprov] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_cemprov = dict(sorted(denuncias_por_cemprov.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_cemprov.keys())
        values = list(denuncias_por_cemprov.values())

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_tipcem(self, year, quarters, month_list):
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
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        total_denuncias = len(denuncias)
        total_intervenciones = 0

        # Contar las denuncias con al menos una intervención
        for denuncia in denuncias:
            if denuncia.cem_legal or denuncia.cem_psicologica or denuncia.cem_tsocial:
                total_intervenciones += 1

        # Calcular los porcentajes
        porcentaje_intervenciones = (total_intervenciones / total_denuncias) * 100 if total_denuncias > 0 else 0
        porcentaje_no_intervenciones = 100 - porcentaje_intervenciones

        # Redondear los porcentajes a un decimal
        porcentaje_intervenciones = round(porcentaje_intervenciones, 1)
        porcentaje_no_intervenciones = round(porcentaje_no_intervenciones, 1)

        # Preparar los datos para el gráfico
        labels = ['Intervención CEM', 'Denuncias']
        values = [porcentaje_intervenciones, porcentaje_no_intervenciones]

        return {
            'labels': labels,
            'values': values,
            'total_denuncias': total_denuncias,
            'total_intervenciones': total_intervenciones
        }

    @api.model
    def get_top_cs(self, year, quarters, month_list):
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
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por cs
        denuncias_por_cs = {}

        # Contar las denuncias por cs
        for denuncia in denuncias:
            cs = denuncia.sld_centro
            if cs:
                cs_name = cs.sigla
                if cs_name in denuncias_por_cs:
                    denuncias_por_cs[cs_name] += 1
                else:
                    denuncias_por_cs[cs_name] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_cs = dict(sorted(denuncias_por_cs.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_cs.keys())
        values = list(denuncias_por_cs.values())

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_csprov(self, year, quarters, month_list):
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
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por csprov
        denuncias_por_csprov = {}

        # Contar las denuncias por csprov
        for denuncia in denuncias:
            if denuncia.sld_centro:
                csprov = denuncia.provincia
                if csprov:
                        if csprov in denuncias_por_csprov:
                            denuncias_por_csprov[csprov] += 1
                        else:
                            denuncias_por_csprov[csprov] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_csprov = dict(sorted(denuncias_por_csprov.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_csprov.keys())
        values = list(denuncias_por_csprov.values())

        return {'labels': labels, 'values': values}

    
    @api.model
    def get_top_cstip(self, year, quarters, month_list):
        filters = [('pjf_med_prot', '=', True)]

        date_filters = []

        # Verificar y agregar filtro de año
        if year and year != 'null':
            date_filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
            date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))
    
        # Verificar y agregar filtros de trimestre
        if quarters and quarters != 'null':
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    date_filters.append(('ctrlpj_fec_den', '>=', f'{year}-01-01 00:00:00'))
                    date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    date_filters.append(('ctrlpj_fec_den', '>=', f'{year}-04-01 00:00:00'))
                    date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    date_filters.append(('ctrlpj_fec_den', '>=', f'{year}-07-01 00:00:00'))
                    date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    date_filters.append(('ctrlpj_fec_den', '>=', f'{year}-10-01 00:00:00'))
                    date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de mes
        if month_list and month_list != 'null':
            for month in month_list.split(','):
                month = month.zfill(2)
                date_filters.append(('ctrlpj_fec_den', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        date_filters.append(('ctrlpj_fec_den', '<=', f'{year}-{month}-28 23:59:59'))

        # Añadir los filtros de fecha a la lista de filtros
        if date_filters:
            filters += ['&'] * (len(date_filters) // 2) + date_filters

        # Realizar la búsqueda con los filtros establecidos
        denuncias_con_proteccion = self.env['sitrad.denuncias'].search(filters)

        # Contar la cantidad de medidas de protección (pjf_med_prot = True)
        total_medidas_proteccion = len(denuncias_con_proteccion)

        # Inicializar contadores para Facultativo y Obligatorio
        facultativo_count = 0
        obligatorio_count = 0

        # Contar las denuncias Facultativas y Obligatorias
        for denuncia in denuncias_con_proteccion:
            if denuncia.sld_rqr == 'Facultativo':
                facultativo_count += 1
            elif denuncia.sld_rqr == 'Obligatorio':
                obligatorio_count += 1

        # Calcular el porcentaje de Facultativo y Obligatorio respecto al total de medidas de protección
        percent_facultativo = (facultativo_count / total_medidas_proteccion) * 100 if total_medidas_proteccion > 0 else 0
        percent_obligatorio = (obligatorio_count / total_medidas_proteccion) * 100 if total_medidas_proteccion > 0 else 0

        # Calcular el porcentaje de "Otros" (restante)
        percent_otros = 100 - percent_facultativo - percent_obligatorio

        # Preparar los datos para el gráfico de barras
        labels = ['No Requerido', 'Facultativo', 'Obligatorio']
        values = [percent_otros, percent_facultativo, percent_obligatorio]

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_intervenciones_cem(self, year, quarters, month_list):
        filters = []

        # Filtrar por año
        if year and year != 'null':
            filters.append(("EXTRACT(YEAR FROM ctrlpj_fec_den) = %s", year))

        # Filtrar por trimestre
        if quarters and quarters != 'null':
            quarter_conditions = []
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 1 AND 3)")
                elif quarter == '04-06':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 4 AND 6)")
                elif quarter == '07-09':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 7 AND 9)")
                elif quarter == '10-12':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 10 AND 12)")
            if quarter_conditions:
                filters.append(("(" + " OR ".join(quarter_conditions) + ")",))

        # Filtrar por mes
        if month_list and month_list != 'null':
            month_conditions = []
            for month in month_list.split(','):
                month_conditions.append(f"EXTRACT(MONTH FROM ctrlpj_fec_den) = {int(month)}")
            if month_conditions:
                filters.append(("(" + " OR ".join(month_conditions) + ")",))

        # Construir la cláusula WHERE solo si hay filtros definidos
        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filter[0] for filter in filters)

        # Construir la consulta SQL
        query = f'''
            SET timezone = 'America/Lima';
            SELECT 
                CASE 
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 1 THEN 'Ene'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 2 THEN 'Feb'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 3 THEN 'Mar'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 4 THEN 'Abr'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 5 THEN 'May'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 6 THEN 'Jun'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 7 THEN 'Jul'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 8 THEN 'Ago'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 9 THEN 'Sep'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 10 THEN 'Oct'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 11 THEN 'Nov'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 12 THEN 'Dic'
                    ELSE 'S/F'
                END as mes,
                COUNT(*) as denuncias,
                COUNT(*) FILTER (
                    WHERE cem_legal IS TRUE 
                       OR cem_psicologica IS TRUE 
                       OR cem_tsocial IS TRUE
                ) as intervenciones
            FROM 
                sitrad_denuncias
                {where_clause}
            GROUP BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den)
            ORDER BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den) ASC;
        '''

        # Obtener los parámetros de los filtros
        params = [value for filter in filters for value in filter[1:]]

        # Ejecutar la consulta SQL
        self._cr.execute(query, params)
        top_product = self._cr.dictfetchall()

        # Procesar los resultados de la consulta
        months = [record.get('mes') for record in top_product]
        total_denuncias = [int(record.get('denuncias')) for record in top_product]
        total_intervenciones = [int(record.get('intervenciones')) for record in top_product]

        return {
            'months': months,
            'total_denuncias': total_denuncias,
            'total_intervenciones': total_intervenciones
        }


    @api.model
    def get_top_intervenciones_cs(self, year, quarters, month_list):
        filters = []

        # Filtrar por año
        if year and year != 'null':
            filters.append("EXTRACT(YEAR FROM ctrlpj_fec_den) = %s")

        # Filtrar por trimestre
        if quarters and quarters != 'null':
            quarter_conditions = []
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 1 AND 3)")
                elif quarter == '04-06':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 4 AND 6)")
                elif quarter == '07-09':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 7 AND 9)")
                elif quarter == '10-12':
                    quarter_conditions.append("(EXTRACT(MONTH FROM ctrlpj_fec_den) BETWEEN 10 AND 12)")
            if quarter_conditions:
                filters.append("(" + " OR ".join(quarter_conditions) + ")")

        # Filtrar por mes
        if month_list and month_list != 'null':
            month_conditions = []
            for month in month_list.split(','):
                month_conditions.append(f"EXTRACT(MONTH FROM ctrlpj_fec_den) = {int(month)}")
            if month_conditions:
                filters.append("(" + " OR ".join(month_conditions) + ")")

        # Construir la cláusula WHERE solo si hay filtros definidos
        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        # Construir la consulta SQL
        query = f'''
            SET timezone = 'America/Lima';
            SELECT 
                CASE 
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 1 THEN 'Ene'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 2 THEN 'Feb'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 3 THEN 'Mar'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 4 THEN 'Abr'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 5 THEN 'May'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 6 THEN 'Jun'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 7 THEN 'Jul'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 8 THEN 'Ago'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 9 THEN 'Sep'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 10 THEN 'Oct'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 11 THEN 'Nov'
                    WHEN EXTRACT(MONTH FROM ctrlpj_fec_den) = 12 THEN 'Dic'
                    ELSE 'S/F'
                END as mes,
                COUNT(*) FILTER (WHERE pjf_med_prot IS TRUE) as medidas_proteccion,
                COUNT(*) FILTER (
                    WHERE pjf_med_prot IS TRUE AND sld_rqr = 'Facultativo'
                ) as facultativo,
                COUNT(*) FILTER (
                    WHERE pjf_med_prot IS TRUE AND sld_rqr = 'Obligatorio'
                ) as obligatorio
            FROM 
                sitrad_denuncias
                {where_clause}
            GROUP BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den)
            ORDER BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den) ASC;
        '''
        # Obtener los parámetros de los filtros
        params = []
        if year and year != 'null':
            params.append(year)

        # Ejecutar la consulta SQL
        self._cr.execute(query, params)
        top_product = self._cr.dictfetchall()

        # Procesar los resultados de la consulta
        months = [record.get('mes') for record in top_product]
        total_medidas_proteccion = [int(record.get('medidas_proteccion')) for record in top_product]
        total_facultativo = [int(record.get('facultativo')) for record in top_product]
        total_obligatorio = [int(record.get('obligatorio')) for record in top_product]

        return {
            'months': months,
            'total_medidas_proteccion': total_medidas_proteccion,
            'total_facultativo': total_facultativo,
            'total_obligatorio': total_obligatorio
        }
