import calendar
import random
import pytz
from datetime import datetime
from calendar import monthrange
from statistics import mean
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class SitradVic(models.Model):
    _inherit = 'sitrad.denuncias'
    
    @api.model
    def get_top_vicprov(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por provincia
        victimas_por_provincia = {}

        # Contar las víctimas por provincia
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                provincia = denuncia.provincia
                if provincia:
                    if provincia in victimas_por_provincia:
                        victimas_por_provincia[provincia] += 1
                    else:
                        victimas_por_provincia[provincia] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        victimas_por_provincia = dict(sorted(victimas_por_provincia.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(victimas_por_provincia.keys())
        values = list(victimas_por_provincia.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_vicsex(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por sexo
        victimas_por_sexo = {}

        # Contar las víctimas por sexo
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                sexo = den_vict.victima.sex.name if den_vict.victima and den_vict.victima.sex else None
                if sexo:
                    if sexo in victimas_por_sexo:
                        victimas_por_sexo[sexo] += 1
                    else:
                        victimas_por_sexo[sexo] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        victimas_por_sexo = dict(sorted(victimas_por_sexo.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(victimas_por_sexo.keys())
        values = list(victimas_por_sexo.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_vicgen(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por sexo
        victimas_por_sexo = {}

        # Contar las víctimas por sexo
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                sexo = den_vict.victima.gen.name if den_vict.victima and den_vict.victima.gen else None
                if sexo:
                    if sexo in victimas_por_sexo:
                        victimas_por_sexo[sexo] += 1
                    else:
                        victimas_por_sexo[sexo] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        victimas_por_sexo = dict(sorted(victimas_por_sexo.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(victimas_por_sexo.keys())
        values = list(victimas_por_sexo.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_vicestado(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por marital_status
        victimas_por_status= {}

        # Contar las víctimas por marital_status
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                marital_status = den_vict.victima.civil.name if den_vict.victima and den_vict.victima.civil else None
                if marital_status:
                    if marital_status in victimas_por_status:
                        victimas_por_status[marital_status] += 1
                    else:
                        victimas_por_status[marital_status] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        victimas_por_status = dict(sorted(victimas_por_status.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(victimas_por_status.keys())
        values = list(victimas_por_status.values())
        return {'labels': labels, 'values': values}


    @api.model
    def get_top_vicedad(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por marital_status
        victimas_por_status= {}

        # Contar las víctimas por marital_status
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                marital_status = den_vict.victima.condicion.name if den_vict.victima and den_vict.victima.condicion else None
                if marital_status:
                    if marital_status in victimas_por_status:
                        victimas_por_status[marital_status] += 1
                    else:
                        victimas_por_status[marital_status] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        victimas_por_status = dict(sorted(victimas_por_status.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(victimas_por_status.keys())
        values = list(victimas_por_status.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_vicedistrito(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por marital_status
        victimas_por_status= {}

        # Contar las víctimas por marital_status
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                marital_status = den_vict.victima.distrito if den_vict.victima and den_vict.victima.distrito else None
                if marital_status:
                    if marital_status in victimas_por_status:
                        victimas_por_status[marital_status] += 1
                    else:
                        victimas_por_status[marital_status] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        victimas_por_status = dict(sorted(victimas_por_status.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(victimas_por_status.keys())
        values = list(victimas_por_status.values())
        return {'labels': labels, 'values': values}


    @api.model
    def get_top_vichijos(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar el contador para el número total de hijos
        total_hijos = 0

        # Contar el número total de hijos
        for denuncia in denuncias:
            for den_vict in denuncia.victima:
                if den_vict.victima:
                    hijos = den_vict.victima.hijos
                    if hijos:
                        total_hijos += hijos

        # Preparar los datos para el gráfico de barras
        labels = ['Total Hijos']
        values = [total_hijos]
        
        return {'labels': labels, 'values': values}
