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
        domain = []
        crtlv_contador_values = 0
        crtlpj_contador_values = 0
        crtlpjp_general_values = 0
        total_projects = 0
        total_time = 0
        total_general = 0
        project_stage_list = 0

        if year =='null' or year ==None:
            print('no hay fecha')
        else:
            domain.append(('ctrlpj_fec_den', '>=', f"{year}-01-01 00:00:00"))
            domain.append(('ctrlpj_fec_den', '<=', f"{year}-12-31 23:59:59"))
            
            if month_list =='null' or month_list ==None:
                print('no hay fecha')
            else:
                # Obtenemos el último día del mes
                last_day_of_month = monthrange(int(year), int(month_list))[1]
                # Construimos la fecha con el último día del mes
                domain.append(('ctrlpj_fec_den', '>=', f"{year}-{month_list}-01 00:00:00"))
                domain.append(('ctrlpj_fec_den', '<=', f"{year}-{month_list}-{last_day_of_month} 23:59:59"))

        if project_selection =='null' or project_selection ==None:
            print('no hay dato2')
        else:
            domain.append(('provincia', '=', project_selection))

        if juggados_selection == 'null' or juggados_selection ==None:
            print('no hay dato3')
        else:
            domain.append(('pjf_juzgado.id', '=', juggados_selection))

        if comisaria_list == 'null' or comisaria_list ==None:
            print('no hay dato4')
        else:
            domain.append(('comisarias.id', '=', comisaria_list))

        all_projects = self.env['sitrad.denuncias'].search(domain)
        
        crtlv_contador_values = all_projects.mapped('crtlv_contador')
        crtlpj_contador_values = all_projects.mapped('crtlpj_contador')
        crtlpjp_general_values = all_projects.mapped('crtlpjp_general')
        crtlpjp_general_notifi = all_projects.mapped('crtlmp_contador')
        

        total_projects = round(sum(crtlv_contador_values) / len(crtlv_contador_values), 0) if crtlv_contador_values else 0
        total_time = round(sum(crtlpj_contador_values) / len(crtlpj_contador_values), 0) if crtlpj_contador_values else 0
        # total_general = round(sum(crtlpjp_general_values) / len(crtlpjp_general_values), 0) if crtlpjp_general_values else 0
        # project_stage_list = round(total_projects + total_time,0)
        project_stage_list = round(sum(crtlpjp_general_notifi) / len(crtlpjp_general_notifi), 0) if crtlpjp_general_notifi else 0
        
        total_general = (round(total_projects,0) + round(total_time,0) + round(project_stage_list,0))
        

        #Guardar la consulta SQL en un archivo de texto
        # archivo_sql = "C:\\consulta_sql_2.txt"
        # with open(archivo_sql, 'w') as archivo:
        #     archivo.write(str(domain)+"****"+str(all_projects))

        return {
            'total_projects': total_projects,
            'total_hours': total_time,
            'project_stage_list': project_stage_list,
            'total_general': total_general,
        }


    @api.model
    def get_top_timesheet_employees(self, year, project_selection, juggados_selection, comisaria_list, month_list, quarters):
        # Construir los filtros basados en los parámetros que no son nulos
        filters = []

        if year == 'null' or year is None:
            print('no hay fecha')
        else:
            filters.append(f"EXTRACT(YEAR FROM ctrlpj_fec_den) = {year}")

            if quarters and quarters != 'null':  # Verificar si quarters no es 'null'
                for quarter in quarters.split(','):
                    if quarter != 'null':  # Verificar si el trimestre no es 'null'
                        start_month, end_month = map(int, quarter.split('-'))
                        filters.append(f"EXTRACT(MONTH FROM ctrlpj_fec_den) >= {start_month}")
                        filters.append(f"EXTRACT(MONTH FROM ctrlpj_fec_den) <= {end_month}")
            
            if month_list == 'null' or month_list is None:
                print('no hay fecha')
            else:
                filters = []
                filters.append(f"EXTRACT(MONTH FROM ctrlpj_fec_den) = {month_list}")

        if project_selection == 'null' or project_selection is None:
            print('no hay provincia seleccionada')
        else:
            filters.append(f"provincia = '{project_selection}'")

        if juggados_selection == 'null' or juggados_selection is None:
            print('no hay juzgado seleccionado')
        else:
            filters.append(f"pjf_juzgado = '{juggados_selection}'")

        if comisaria_list == 'null' or comisaria_list is None:
            print('no hay comisaría seleccionada')
        else:
            filters.append(f"comisarias = '{comisaria_list}'")

        # Construir la cláusula WHERE solo si hay filtros definidos
        where_clause = ""
        if filters:
            # Si hay más de un filtro, agregamos "AND" entre ellos
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
                COUNT(*) as denuncias,
                COUNT(*) FILTER (WHERE ctrlpj_fec_rempj IS NOT NULL) as medidas_proteccion
            FROM 
                sitrad_denuncias
            {where_clause}
            GROUP BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den)
            ORDER BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den) ASC;
        '''
        # Ejecutar la consulta SQL
        self._cr.execute(query)
        top_product = self._cr.dictfetchall()

        #Guardar la consulta SQL en un archivo de texto
        #archivo_sql = "C:\\consulta_sql_2.txt"
        #with open(archivo_sql, 'w') as archivo:
            # archivo.write(str(query))

        # Procesar los resultados de la consulta
        unit = [record.get('mes') for record in top_product]
        employee = [record.get('denuncias') for record in top_product]
        medprot = [record.get('medidas_proteccion') for record in top_product]

        return [unit, employee, medprot]



    @api.model
    def get_denuncias_data(self, year, project_selection, juggados_selection, comisaria_list, month_list, quarters):

        filters = []


        if year =='null' or year ==None:
            print('no hay fecha')
        else:
            filters.append(('ctrlpj_fec_den', '>=', f"{year}-01-01 00:00:00"))
            filters.append(('ctrlpj_fec_den', '<=', f"{year}-12-31 23:59:59"))
            
            if month_list =='null' or month_list ==None:
                print('no hay fecha')
            else:
                # Obtenemos el último día del mes
                last_day_of_month = monthrange(int(year), int(month_list))[1]
                # Construimos la fecha con el último día del mes
                filters.append(('ctrlpj_fec_den', '>=', f"{year}-{month_list}-01 00:00:00"))
                filters.append(('ctrlpj_fec_den', '<=', f"{year}-{month_list}-{last_day_of_month} 23:59:59"))


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
                'pjf_btn_pnc': denuncia.pjf_btn_pnc,
                'pjf_acm': denuncia.pjf_acm,
                'crtlpjp_general': denuncia.crtlpjp_general,
                'url_medida': denuncia.url_medida,
            }
            denuncias_data.append(denuncia_data)

        return {
            'denuncias': denuncias_data
        }

    @api.model
    def get_top_provincia(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las denuncias por provincia
        denuncias_por_provincia = {}

        # Contar las denuncias por provincia
        for denuncia in denuncias:
            provincia = denuncia.provincia
            if provincia:
                if provincia in denuncias_por_provincia:
                    denuncias_por_provincia[provincia] += 1
                else:
                    denuncias_por_provincia[provincia] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_provincia = dict(sorted(denuncias_por_provincia.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_provincia.keys())
        values = list(denuncias_por_provincia.values())

        return {'labels': labels, 'values': values}


    @api.model
    def get_top_comisarias(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

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
    def get_top_medidas(self):
        # Buscar todas las denuncias que tengan la fecha de pronóstico del juzgado establecida
        denuncias = self.env['sitrad.denuncias'].search([('ctrlpj_fec_rempj', '!=', False)])

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
    def get_top_grado(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las denuncias por grado
        denuncias_por_grado = {}

        # Contar las denuncias por grado
        for denuncia in denuncias:
            grado = denuncia.grado
            if grado:
                if grado in denuncias_por_grado:
                    denuncias_por_grado[grado] += 1
                else:
                    denuncias_por_grado[grado] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_grado = dict(sorted(denuncias_por_grado.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de pastel
        labels = list(denuncias_por_grado.keys())
        values = list(denuncias_por_grado.values())

        return {'labels': labels, 'values': values}

    @api.model
    def get_top_forma(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Inicializar un diccionario para contar las denuncias por forma
        denuncias_por_forma = {}

        # Contar las denuncias por forma
        for denuncia in denuncias:
            formas = denuncia.forma
            if formas:
                # Tomar solo la primera forma si hay más de una
                primera_forma = formas[0]
                if primera_forma.name in denuncias_por_forma:
                    denuncias_por_forma[primera_forma.name] += 1
                else:
                    denuncias_por_forma[primera_forma.name] = 1

        # Ordenar el diccionario por el número de denuncias en orden descendente
        denuncias_por_forma = dict(sorted(denuncias_por_forma.items(), key=lambda item: item[1], reverse=True))

        # Preparar los datos para el gráfico de barras
        labels = list(denuncias_por_forma.keys())
        values = list(denuncias_por_forma.values())

        return {'labels': labels, 'values': values}



    @api.model
    def get_top_denunciaing(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

        # Contar el total de denuncias
        total_denuncias = len(denuncias)

        return {'totaldenuncias': total_denuncias}  # Devolver el valor en un diccionario


    @api.model
    def get_top_cems(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

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
    def get_top_cemprov(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

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
    def get_top_tipcem(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

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
    def get_top_cs(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

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
    def get_top_csprov(self):
        # Buscar todas las denuncias
        denuncias = self.env['sitrad.denuncias'].search([])

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
    def get_top_cstip(self):
        # Buscar todas las denuncias que tienen pjf_med_prot como verdadero
        denuncias_con_proteccion = self.env['sitrad.denuncias'].search([('pjf_med_prot', '=', True)])

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
        values = [ percent_otros, percent_facultativo, percent_obligatorio]

        return {'labels': labels, 'values': values}


    @api.model
    def get_top_intervenciones_cem(self):
        # Construir la consulta SQL
        query = '''
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
            GROUP BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den)
            ORDER BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den) ASC;
        '''
        
        # Ejecutar la consulta SQL
        self._cr.execute(query)
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
    def get_top_intervenciones_cs(self):
        # Construir la consulta SQL
        query = '''
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
                ) as Facultativo,
                COUNT(*) FILTER (
                    WHERE pjf_med_prot IS TRUE AND sld_rqr = 'Obligatorio'
                ) as Obligatorio
            FROM 
                sitrad_denuncias
            GROUP BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den)
            ORDER BY 
                EXTRACT(MONTH FROM ctrlpj_fec_den) ASC;
        '''
        
        # Ejecutar la consulta SQL
        self._cr.execute(query)
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
        