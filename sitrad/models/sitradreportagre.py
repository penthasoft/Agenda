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
    def get_top_agreprov(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por provincia
        agresor_por_provincia = {}

        # Contar las víctimas por provincia
        for denuncia in denuncias:
            for den_agret in denuncia.agresor:
                provincia = denuncia.provincia
                if provincia:
                    if provincia in agresor_por_provincia:
                        agresor_por_provincia[provincia] += 1
                    else:
                        agresor_por_provincia[provincia] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        agresor_por_provincia = dict(sorted(agresor_por_provincia.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(agresor_por_provincia.keys())
        values = list(agresor_por_provincia.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_agresex(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por sexo
        agresor_por_sexo = {}

        # Contar las víctimas por sexo
        for denuncia in denuncias:
            for den_agret in denuncia.agresor:
                sexo = den_agret.agresor.sex.name if den_agret.agresor and den_agret.agresor.sex else None
                if sexo:
                    if sexo in agresor_por_sexo:
                        agresor_por_sexo[sexo] += 1
                    else:
                        agresor_por_sexo[sexo] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        agresor_por_sexo = dict(sorted(agresor_por_sexo.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(agresor_por_sexo.keys())
        values = list(agresor_por_sexo.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_agreestado(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por marital_status
        agresor_por_status= {}

        # Contar las víctimas por marital_status
        for denuncia in denuncias:
            for den_agret in denuncia.agresor:
                marital_status = den_agret.agresor.civil.name if den_agret.agresor and den_agret.agresor.civil else None
                if marital_status:
                    if marital_status in agresor_por_status:
                        agresor_por_status[marital_status] += 1
                    else:
                        agresor_por_status[marital_status] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        agresor_por_status = dict(sorted(agresor_por_status.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(agresor_por_status.keys())
        values = list(agresor_por_status.values())
        return {'labels': labels, 'values': values}


    @api.model
    def get_top_agreedad(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por marital_status
        agresor_por_status= {}

        # Contar las víctimas por marital_status
        for denuncia in denuncias:
            for den_agret in denuncia.agresor:
                marital_status = den_agret.agresor.condicion.name if den_agret.agresor and den_agret.agresor.condicion else None
                if marital_status:
                    if marital_status in agresor_por_status:
                        agresor_por_status[marital_status] += 1
                    else:
                        agresor_por_status[marital_status] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        agresor_por_status = dict(sorted(agresor_por_status.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(agresor_por_status.keys())
        values = list(agresor_por_status.values())
        return {'labels': labels, 'values': values}

    @api.model
    def get_top_agreedistrito(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las víctimas por marital_status
        agresor_por_status= {}

        # Contar las víctimas por marital_status
        for denuncia in denuncias:
            for den_agret in denuncia.agresor:
                marital_status = den_agret.agresor.distrito if den_agret.agresor and den_agret.agresor.distrito else None
                if marital_status:
                    if marital_status in agresor_por_status:
                        agresor_por_status[marital_status] += 1
                    else:
                        agresor_por_status[marital_status] = 1

        # Ordenar el diccionario por el número de víctimas en orden descendente
        agresor_por_status = dict(sorted(agresor_por_status.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(agresor_por_status.keys())
        values = list(agresor_por_status.values())
        return {'labels': labels, 'values': values}
        