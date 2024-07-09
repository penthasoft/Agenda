import calendar
import random
import pytz
from datetime import datetime
from calendar import monthrange
from statistics import mean
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
import os

class SitradReport(models.Model):
    _inherit = 'sitrad.denuncias'

    @api.model
    def get_top_provincia(self, year, quarters, month_list):
        filters = []

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))
    

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))
        
        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlv_fec_rempj', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-28 23:59:59'))
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)
        
        denuncias_por_provincia = {}
        for denuncia in denuncias:
            provincia = denuncia.provincia
            if provincia:
                if provincia in denuncias_por_provincia:
                    denuncias_por_provincia[provincia] += 1
                else:
                    denuncias_por_provincia[provincia] = 1
        
        denuncias_por_provincia = dict(sorted(denuncias_por_provincia.items(), key=lambda item: item[1], reverse=True))
        
        labels = list(denuncias_por_provincia.keys())
        values = list(denuncias_por_provincia.values())
        
        return {'labels': labels, 'values': values}


    @api.model
    def get_top_comisarias(self, year, quarters, month_list):
        filters = []

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))
    

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))
        
        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlv_fec_rempj', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-28 23:59:59'))
        
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por comisarias
        denuncias_por_comisarias = {}

        # Contar las denuncias por comisarias
        for denuncia in denuncias:
            comisarias = denuncia.comisarias
            if comisarias:
                comisarias_name = comisarias.sigla
                if comisarias_name in denuncias_por_comisarias:
                    denuncias_por_comisarias[comisarias_name] += 1
                else:
                    denuncias_por_comisarias[comisarias_name] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_comisarias = dict(sorted(denuncias_por_comisarias.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_comisarias.keys())
        values = list(denuncias_por_comisarias.values())

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_medidas(self, year, quarters, month_list):

        filters = []

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))
    

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))
        
        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlv_fec_rempj', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-28 23:59:59'))

        filters.append(('ctrlpj_fec_rempj', '!=', False))
        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar listas para almacenar las etiquetas (labels) y los valores (values) para el gráfico
        labels = []
        values = []

        # Contar las denuncias por juzgado
        for denuncia in denuncias:
            juzgado = denuncia.pjf_juzgado
            if juzgado:
                juzgado_name = juzgado.sigla
                if juzgado_name not in labels:
                    labels.append(juzgado_name)
                    values.append(1)
                else:
                    index = labels.index(juzgado_name)
                    values[index] += 1

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_grado(self, year, quarters, month_list):
        filters = []

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlv_fec_rempj', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-28 23:59:59'))

        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por grado
        denuncias_por_grado = {}

        # Contar las denuncias por grado
        for denuncia in denuncias:
            grado = denuncia.grado
            if grado:
                grado_name = 'No Deter.' if grado == 'Ninguno' else grado
                if grado_name in denuncias_por_grado:
                    denuncias_por_grado[grado_name] += 1
                else:
                    denuncias_por_grado[grado_name] = 1

        # Lista ordenada de los grados de denuncia
        ordered_grades = ['Leve', 'Moderado', 'Severo', 'Muy Severo', 'No Deter.']

        # Ordenar el diccionario por el orden de los grados de denuncia
        denuncias_por_grado = {grade: denuncias_por_grado.get(grade, 0) for grade in ordered_grades}

        # Preparar los datos para el gráfico de pastel
        labels = list(denuncias_por_grado.keys())
        values = list(denuncias_por_grado.values())

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_forma(self, year, quarters, month_list):
        filters = []

        # Verificar y agregar filtro de año
        if year != 'null' and year is not None:
            filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
            filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de trimestre
        if quarters != 'null' and quarters is not None:
            for quarter in quarters.split(','):
                if quarter == '01-03':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-01-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-03-31 23:59:59'))
                elif quarter == '04-06':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-04-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-06-30 23:59:59'))
                elif quarter == '07-09':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-07-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-09-30 23:59:59'))
                elif quarter == '10-12':
                    filters.append(('ctrlv_fec_rempj', '>=', f'{year}-10-01 00:00:00'))
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-12-31 23:59:59'))

        # Verificar y agregar filtros de mes
        if month_list != 'null' and month_list is not None:
            for month in month_list.split(','):
                filters.append(('ctrlv_fec_rempj', '>=', f'{year}-{month}-01 00:00:00'))
                if month in ['01', '03', '05', '07', '08', '10', '12']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-31 23:59:59'))
                elif month in ['04', '06', '09', '11']:
                    filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-30 23:59:59'))
                elif month == '02':
                    if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-29 23:59:59'))
                    else:
                        filters.append(('ctrlv_fec_rempj', '<=', f'{year}-{month}-28 23:59:59'))

        # Realizar la búsqueda con los filtros establecidos
        denuncias = self.env['sitrad.denuncias'].search(filters)

        # Inicializar un diccionario para contar las denuncias por forma
        denuncias_por_forma = {}

        # Contar las denuncias por forma
        for denuncia in denuncias:
            formas = denuncia.forma
            if formas:
                # Tomar solo la primera forma si hay más de una
                primera_forma = formas[0]
                if primera_forma.name in denuncias_por_forma:
                    denuncias_por_forma[primera_forma.name]['count'] += 1
                else:
                    denuncias_por_forma[primera_forma.name] = {
                        'count': 1,
                        'sequence': primera_forma.sequence
                    }

        # Ordenar el diccionario por el campo sequence
        denuncias_por_forma = dict(sorted(denuncias_por_forma.items(), key=lambda item: item[1]['sequence']))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_forma.keys())
        values = [item['count'] for item in denuncias_por_forma.values()]

        return {'labels': labels, 'values': values}
