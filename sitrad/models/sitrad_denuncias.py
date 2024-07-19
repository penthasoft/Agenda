import logging
import time
import datetime
import pytz
import os
from odoo.http import request
from pytz import timezone
from odoo import models, fields, api, http, _
from odoo import tools
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools import float_round
from werkzeug.urls import url_encode
import calendar
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

class SitradIRC(models.Model):
    _name = "sitrad.irc"
    _description = "IRC - Instancias Regionales Provinciales y Distritales"

    TIPO_INST = [
      ('Regional', 'Regional'),
      ('Provincial', 'Provincial'),
      ('Distrital', 'Distrital'),
    ]

    RESOLUCION = [
      ('Si', 'Si'),
      ('No', 'No'),
    ]
    
    name = fields.Char(string='Nombre Instancia')
    sigla = fields.Char(string='Sigla')
    tipo_inst = fields.Selection(TIPO_INST, string='Tipo')
    distrito = fields.Char(string='Distrito')
    provincia = fields.Char(string='Provincia')
    region = fields.Char(string='Región')
    presidente = fields.Char(string='Presidente')
    sec_tecnica = fields.Char(string='Seretaria Tecnica')
    # Instalacion
    resolucion = fields.Selection(RESOLUCION, string='Res. Instalacion')
    doc_resolucion = fields.Binary(string="Subir PDF - Instalacion")
    # Funcionamiento
    resolucionf = fields.Selection(RESOLUCION, string='Res. Funcionamiento')
    doc_resolucionf = fields.Binary(string="Subir PDF - Funcionamiento")

    

class SitradIRCact(models.Model):
    _name = "sitrad.ircplan"
    _description = "IRC - Plan de trabajo"

    name = fields.Many2one('sitrad.irc', string="Instancia")
    irc = fields.Many2one('sitrad.irc', string="Instancia")
    year_trab = fields.Char(string='Año - Plan de trabajo')
    plan_trab = fields.Binary(string="Subir Plan de Trabjao PDF")


class SitradIRCact(models.Model):
    _name = "sitrad.ircact"
    _description = "IRC - Actividades"

    ircplan = fields.Many2one('sitrad.ircplan', string="Plan de Trabajo")
    name = fields.Char(string='Nombre de Actividad')
    fecha = fields.Datetime(string='Fecha de Actividad', default=lambda self: fields.datetime.now())
    acta = fields.Binary(string="Subir Acta")
    ref = fields.Char(string='Observacion/Resumen')


class SitradInstancias(models.Model):
    _name = "sitrad.instancias"
    _description = "Instancias"

    TIPO_INST = [
      ('Regional', 'Regional'),
      ('Provincial', 'Provincial'),
      ('Distrital', 'Distrital'),
    ]

    RESOLUCION = [
      ('Si', 'Si'),
      ('No', 'No'),
    ]
    
    name = fields.Char(string='Institucion')
    sigla = fields.Char(string='Sigla')
    tipo_inst = fields.Selection(TIPO_INST, string='Instancia')
    provincia = fields.Char(string='Provincia')
    region = fields.Char(string='Región')
    resolucion = fields.Selection(RESOLUCION, string='Resolucion')
    doc_resolucion = fields.Binary(string="Subir Resolucion PDF")
    presidente = fields.Char(string='Presidente')
    sec_tecnica = fields.Char(string='Seretaria Tecnica')
    year_trab = fields.Char(string='Año - Plan de trabajo')
    plan_trab = fields.Binary(string="Subir Plan de Trabjao PDF")

class SitradCem(models.Model):
    _name = 'sitrad.cem'
    _description = 'Operadores de Justicia'

    name = fields.Char(string='Centro', required=True)
    provincia = fields.Char(string='Provincia')
    sigla = fields.Char(string='Sigla')
    latitude = fields.Char(string='Latitud')
    longitude = fields.Char(string='Longitud')
    is_cem = fields.Boolean(string="¿Es CEM?")
    direccion = fields.Char(string='Direccion')
    tel = fields.Char(string='Telefono')
    direc = fields.Char(string='Referencia')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'El Operador de Justicia debe ser único !')
    ]

    @api.model
    def get_cem_data(self):
        return self.search([
            ('is_cem', '=', False),
            ('latitude', '!=', False),
            ('longitude', '!=', False)
        ]).read(['name', 'provincia', 'sigla', 'latitude', 'longitude', 'direccion','tel','direc' ])

    @api.model
    def get_cem_data_true(self):
        return self.search([
            ('is_cem', '=', True),
            ('latitude', '!=', False),
            ('longitude', '!=', False)
        ]).read(['name', 'provincia', 'sigla', 'latitude', 'longitude', 'direccion','tel','direc' ])

class SitradCemJusti(models.Model):
    _name = 'sitrad.cem.justi'
    _description = 'Justificación'

    name = fields.Char(size=256, string='Justificación', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'La Justificacion debe ser única !')]

class SitradSalud(models.Model):
    _name = 'sitrad.salud'
    _description = 'Centros de Salud'

    name = fields.Char(string='Centro', required=True)
    provincia = fields.Char(string='Provincia')
    sigla = fields.Char(string='Sigla')
    latitude = fields.Char(string='Latitud')
    longitude = fields.Char(string='Longitud')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'El Centro debe ser único !')]

class SitradDenuncias(models.Model):
    _name = "sitrad.denuncias"
    _description = "Denuncias"

    GRADO_DEN = [
      ('Leve', 'Leve'),
      ('Moderado', 'Moderado'),
      ('Severo', 'Severo'),
      ('Muy Severo', 'Muy Severo'),
      ('Ninguno', 'Ninguno'),
    ]

    ZONA_DEN = [
      ('Urbana', 'Urbana'),
      ('Rural', 'Rural'),
    ]

    ESTADO_MP = [
      ('Tramite', 'Tramite'),
      ('Archivo', 'Archivo'),
      ('Denuncia', 'Denuncia'),
    ]

    ESTADO_PJP = [
      ('Tramite', 'Tramite'),
      ('Sentencia', 'Sentencia'),
    ]

    CEM_TIPO = [
      ('Legal', 'Legal'),
      ('Psicologica', 'Psicologica'),
      ('TSocial', 'TSocial'),
    ]

    OPERADOR_DFP = [
      ('Comisaria', 'Comisaria'),
      ('Juzgado', 'Juzgado'),
      ('CEM', 'CEM'),
      ('Centro de Salud', 'Centro de Salud'),
    ]
    
    MOTIVO_DFP = [
      ('Retardo', 'Retardo'),
      ('Maltrado', 'Maltrado'),
      ('Discriminacion', 'Discriminacion'),
    ]

    CARACTER = [
      ('Ninguno', 'Ninguno'),
      ('Facultativo', 'Facultativo'),
      ('Obligatorio', 'Obligatorio'),
    ]

    PROVINCIAS = [
      ('Tacna', 'Tacna'),
      ('JBasadre', 'JBasadre'),
      ('Tarata', 'Tarata'),
      ('Candarave', 'Candarave'),
    ]

    def _get_empleado(self):
        empleado_obj = self.env['res.partner']
        domain = [('user_id', '=', self.env.uid)]
        user_ids = empleado_obj.search(domain, limit=1)
        if user_ids:
            return user_ids.id or False
        else:
            return False

    name = fields.Char(string='Identificador.', readonly=True, required=True, default=lambda *a: '/')
    date = fields.Datetime(string='Fecha Registro', readonly=True, default=lambda self: fields.datetime.now())
    registra = fields.Many2one('res.partner', string='Registrad@r', default=_get_empleado, readonly=True)
    victima = fields.One2many('sitrad.den_victima','denuncia_id', string="Victimas")
    agresor = fields.One2many('sitrad.den_agresor','denuncia_id', string="Agresores")
    forma = fields.Many2many('sitrad.formas', string="Tipo Violencia")
    forma_names = fields.Char(string="Violencias Grupo", compute='_compute_forma_names', store=True)
    def _compute_forma_names(self):
        for record in self:
            record.forma_names = ', '.join(record.forma.mapped('name'))

    sub_frm = fields.Char(string='Modalidad', default=lambda *a: 'Ninguna')
    grado = fields.Selection(GRADO_DEN, string='Grado')
    zona = fields.Selection(ZONA_DEN, string='ZONA')
    comisarias = fields.Many2one('sitrad.cem', string="Op. Just. Denuncia")
    
    #### PJ FAMILIA ###
    pjf_juzgado = fields.Many2one('sitrad.instancias', string="Juzgado")
    provincias = fields.Selection(PROVINCIAS, string='Provincias')
    provincia = fields.Char(string='Provincia')
    region = fields.Char(string='Región', related='pjf_juzgado.region')
    pjf_exp = fields.Char(string='Expediente Nro.')
    nro_den = fields.Char(string='Denuncia Nro.')
    pjf_med_prot = fields.Boolean(string="¿Medida de Protección?")
    pjf_med_prot_tipo = fields.Many2many('sitrad.medprotec', string="Tipo MedProt")
    pjf_med_prot_pdf = fields.Binary(string="Subir Medida de Proteccion")
    pjf_med_prot_apela = fields.Boolean(string="Apelacion MedProt")
    pjf_btn_pnc = fields.Boolean(string="Boton de Pánico")
    pjf_acm = fields.Boolean(string="Acumulado")
    pjf_acm_exp = fields.Char(string="Exp. Acumulado")

    #### MINISTERIO PUBLICO-FISCALIA ###
    mp_carpeta = fields.Char(string='Carpeta Nro.')
    mp_cem = fields.Boolean(string="Participacion CEM-MinPub")
    mp_estado = fields.Selection(ESTADO_MP, string='MinPub Estado')

    #### Poder Judicial Penal ###
    pjp_juzgados = fields.Many2one('sitrad.instancias', string="PJP Juzgado")
    pjp_exp = fields.Char(string='PJP Expediente Nro.')
    pjp_cem = fields.Boolean(string="Participacion CEM - PJP")
    pjp_estado = fields.Selection(ESTADO_PJP, string='PJP - Estado ')

    #### CEM/AURORA ###
    cem_name =  fields.Many2one('sitrad.cem', string="Nombre del CEM")
    cem_legal = fields.Boolean(string="Legal - CEM")
    cem_psicologica = fields.Boolean(string="Psicologica - CEM")
    cem_tsocial = fields.Boolean(string="Trabajador Social - CEM")
    cem_justif = fields.Many2many('sitrad.cem.justi', string="Adenda")

    #### CENTRO DE SALUD ###
    sld_centro =  fields.Many2one('sitrad.salud', string="Centros de Salud")
    sld_rqr = fields.Selection(CARACTER,string="Caracter", default=lambda *a: 'Ninguno')
    sld_agrecs = fields.Boolean(string="Agresor ¿Es Oblig.?")
    sld_fec_recmp = fields.Datetime(string='Fecha Recepcion MedProt')
    sld_fec_recinf = fields.Datetime(string='Fecha Remision informe PJ')
    sld_contador = fields.Float(string='Control de Tiempos', digits='Product Price')

    #### DEFENSORIA DEL PUEBLO ###
    defp_rqr =  fields.Char(string='Requerimiento Nro.')
    defp_fec = fields.Datetime(string='Fecha')
    defp_opej = fields.Selection(OPERADOR_DFP, string='Operador de Justicia')
    defp_mtv = fields.Selection(MOTIVO_DFP, string='Motivo')
    defp_acta = fields.Boolean(string="Acta de Visita")
    
    ctrlv_fec_den_hec = fields.Datetime(string='Fec. Hechos VCM ')
    ctrlv_fec_den = fields.Datetime(string='Fec. Denuncia VCM')
    ctrlv_fec_rempj = fields.Datetime(string='Fec. Remision al PJ')
    crtlv_contador = fields.Float(string='Tiempo Tramite VCT - PJ', digits='Product Price', compute='_compute_tiempo_tramite', readonly=False, store=True, index=True)

    ctrlpj_fec_den = fields.Datetime(string='PJ Fec. Recep. Denuncia')
    ctrlpj_fec_rempj = fields.Datetime(string='PJ Fec. Pron. Med. Pro.')
    crtlpj_contador = fields.Float(string='PJ Tiempo Tramite Med.Prot.', digits='Product Price', compute='_compute_tiempo_tramite_pj', store=True, index=True)

    ctrlmp_fec_den = fields.Datetime(string='MP Fec. Noti. Med.Pro.')
    ctrlmp_fec_rempj = fields.Datetime(string='MP Fecha Archivo-Denuncia')
    crtlmp_contador = fields.Float(string='MP Tiempo Tramite', digits='Product Price', compute='_compute_tiempo_tramite_mp', store=True, index=True)

    ctrlpjp_fec_den = fields.Datetime(string='PJP Fec. Recep. Med.Pro.')
    ctrlpjp_fec_rempj = fields.Datetime(string='PJP Fecha Tramite-Sentencia')
    crtlpjp_contador = fields.Float(string='PJP Tiempo Tramite', digits='Product Price', compute='_compute_tiempo_tramite_pjp', store=True, index=True)
    
    crtlpjp_general = fields.Float(string='PJP Tiempo General', digits='Product Price', compute='_compute_tiempo_general', store=True, index=True)

    url_medida =  fields.Char(string='URL Medida')

    crtlv_categoria = fields.Selection([
        ('menos_24h', 'Antes de las 24 horas'),
        ('entre_24h_3d', 'Entre 24 horas y 3 días'),
        ('entre_3d_1s', 'Entre 3 días y 1 semana'),
        ('entre_1s_1m', 'Entre 1 semana y 1 mes'),
        ('mas_1m', '1 mes en adelante'),
    ], string='Categoría Tiempo', compute='_compute_categoria_tiempo', store=True)


    @api.depends('crtlv_contador')
    def _compute_categoria_tiempo(self):
        for record in self:
            if record.crtlv_contador <= 1:
                record.crtlv_categoria = 'menos_24h'
            elif record.crtlv_contador > 1 and record.crtlv_contador <= 3:
                record.crtlv_categoria = 'entre_24h_3d'
            elif record.crtlv_contador > 3 and record.crtlv_contador <= 7:
                record.crtlv_categoria = 'entre_3d_1s'
            elif record.crtlv_contador > 7 and record.crtlv_contador <= 30:
                record.crtlv_categoria = 'entre_1s_1m'
            elif record.crtlv_contador > 30:
                record.crtlv_categoria = 'mas_1m'
            else:
                record.crtlv_categoria = False

    @api.onchange('provincias')
    def _onchange_provincias(self):
        if self.provincias:
            self.provincia = self.provincias
        else:
            self.provincia = ''

    @api.depends('ctrlv_fec_den', 'ctrlv_fec_rempj')
    def _compute_tiempo_tramite(self):
        for record in self:
            if record.ctrlv_fec_den and record.ctrlv_fec_rempj:
                fecha_denuncia = fields.Datetime.from_string(record.ctrlv_fec_den)
                fecha_remision = fields.Datetime.from_string(record.ctrlv_fec_rempj)
                diferencia = fecha_remision - fecha_denuncia
                record.crtlv_contador = diferencia.days  # Obtener solo el número de días
            else:
                record.crtlv_contador = 0

    @api.depends('ctrlpj_fec_den', 'ctrlpj_fec_rempj')
    def _compute_tiempo_tramite_pj(self):
        for record in self:
            if record.ctrlpj_fec_den and record.ctrlpj_fec_rempj:
                fecha_denuncia = fields.Datetime.from_string(record.ctrlpj_fec_den)
                fecha_remision = fields.Datetime.from_string(record.ctrlpj_fec_rempj)
                diferencia = fecha_remision - fecha_denuncia
                record.crtlpj_contador = diferencia.days  # Obtener solo el número de días
            else:
                record.crtlpj_contador = 0

    @api.depends('ctrlpj_fec_rempj','ctrlmp_fec_den')
    def _compute_tiempo_tramite_mp(self):
        for record in self:
            if record.ctrlmp_fec_den and record.ctrlpj_fec_rempj:
                fecha_denuncia = fields.Datetime.from_string(record.ctrlpj_fec_rempj)
                fecha_remision = fields.Datetime.from_string(record.ctrlmp_fec_den)
                diferencia = fecha_remision - fecha_denuncia
                record.crtlmp_contador = diferencia.days  # Obtener solo el número de días
            else:
                record.crtlmp_contador = 0

    @api.depends('ctrlpjp_fec_den', 'ctrlpjp_fec_rempj')
    def _compute_tiempo_tramite_pjp(self):
        for record in self:
            if record.ctrlpjp_fec_den and record.ctrlpjp_fec_rempj:
                fecha_denuncia = fields.Datetime.from_string(record.ctrlpjp_fec_den)
                fecha_remision = fields.Datetime.from_string(record.ctrlpjp_fec_rempj)
                diferencia = fecha_remision - fecha_denuncia
                record.crtlpjp_contador = diferencia.days  # Obtener solo el número de días
            else:
                record.crtlpjp_contador = 0

    @api.depends('crtlv_contador', 'ctrlv_fec_rempj','crtlmp_contador' )
    def _compute_tiempo_general(self):
        for ina in self:
            fecha1 = ina.crtlv_contador
            fecha2 = ina.crtlpj_contador
            # fecha3 = ina.crtlmp_contador
            fecha3 = 0

            ina.crtlpjp_general =  fecha1 + fecha2 +  fecha3

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('sitrad.denuncias')
        vals['name'] = sequence or '/'
        inno_denuncias = super(SitradDenuncias, self).create(vals)
        return inno_denuncias

    def download_file(self):
        if self.url_medida:
            return {
                'type': 'ir.actions.act_url',
                'url': '/sitrad/download_file?url_medida=%s' % (self.url_medida),
                'target': 'new',
            }
        else:
            return False

class CustomController(http.Controller):
    @http.route('/sitrad/download_file', type='http', auth='user')
    def download_file(self, **kwargs):
        if request.env.user.has_group('base.group_user'):
            url_medida = kwargs.get('url_medida')
            if not url_medida:
                return request.not_found()

            # Construir la ruta del archivo
            file_path = os.path.join('/opt/medidas/', url_medida)

            # Verificar si el archivo existe
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_data = file.read()

                # Encabezados de respuesta
                headers = [
                    ('Content-Type', 'application/octet-stream'),
                    ('Content-Disposition', f'attachment; filename={url_medida}'),
                    ('Content-Length', str(len(file_data)))
                ]

                # Retornar la respuesta con el archivo adjunto
                return request.make_response(file_data, headers)

        # Si el archivo no existe o el usuario no tiene permisos, mostrar un error
        return request.not_found()