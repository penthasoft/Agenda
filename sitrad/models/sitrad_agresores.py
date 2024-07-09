import logging
import time
import datetime
import pytz
import requests
import json
from pytz import timezone
from odoo import api, fields, models, _
from odoo import tools
from odoo.exceptions import Warning, UserError, AccessError, ValidationError
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools import float_round
from werkzeug.urls import url_encode
from zipfile import ZipFile
from bs4 import BeautifulSoup
from io import BytesIO

_logger = logging.getLogger(__name__)

class SitradFormas(models.Model):
    _name = 'sitrad.formas'
    _description = 'formas'

    name = fields.Char(size=256, string='Formas de Violencia', required=True)
    sequence = fields.Integer(
        'Sequence', default=1, required=True,
        help="Orden")

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'Las formas deben ser únicas !')]

class SitradSexo(models.Model):
    _name = 'sitrad.sexo'
    _description = 'Sexo'

    name = fields.Char(size=256, string='Sexo', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'El sexo debe ser único !')]

class SitradGenero(models.Model):
    _name = 'sitrad.genero'
    _description = 'Género'

    name = fields.Char(size=256, string='Género', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'El Género debe ser único !')]

class SitradMaritalStatus(models.Model):
    _name = 'sitrad.marital_status'
    _description = 'Estado Civil'

    name = fields.Char(size=256, string='Estado Civil', required=True)

class SitradCondicion(models.Model):
    _name = "sitrad.condicion"
    _description = "Condicion"

    name = fields.Char(string='Condicion')
    rang_min = fields.Float(string='Rango Min', digits='Product Price')
    rang_max = fields.Float(string='Rango Max', digits='Product Price')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'La condicion debe ser única !')]

class SitradParentesco(models.Model):
    _name = 'sitrad.parentesco'
    _description = 'Parentesco'

    name = fields.Char(size=256, string='Parentesco', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'El parentesco debe ser único !')]


class SitradMedProt(models.Model):
    _name = 'sitrad.medprotec'
    _description = 'Medidas de Proteccion'

    name = fields.Char(size=256, string='Medida', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'La medida debe ser única !')]

class SitradJuzgado(models.Model):
    _name = 'sitrad.juzgados'
    _description = 'Juzgados'

    name = fields.Char(size=256, string='Medida', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'El Juzgado debe ser único !')]

class SitradTipDoc(models.Model):
    _name = 'sitrad.tipo_doc'
    _description = 'Tipo de Documento'

    name = fields.Char(size=256, string='Medida', required=True)

    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'El Tipo de Documento debe ser único !')]

class SitradAgresores(models.Model):
    _name = "sitrad.agresores"
    # _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Agresores"

    def _agresor_age(self):
        def compute_age_from_dates (patient_dob,patient_deceased,patient_dod):
            now=datetime.datetime.now()
            if (patient_dob):
                dob=datetime.datetime.strptime(patient_dob.strftime('%Y-%m-%d'), '%Y-%m-%d')
                if patient_deceased:
                    dod=datetime.datetime.strptime(patient_dod.strftime('%Y-%m-%d'), '%Y-%m-%d')
                    delta= dod - dob
                    deceased=" (deceased)"
                    years_months_days = str(delta.days // 365)+" Años "+ str(delta.days%365)+" días" + deceased
                else:
                    delta= now - dob
                    years_months_days = str(delta.days // 365)+" Años "+ str(delta.days%365)+" días"
            else:
                years_months_days = "Sin fecha de Nacimiento !"

            return years_months_days
        for patient_data in self:
            patient_data.age = compute_age_from_dates(patient_data.dob,patient_data.deceased,patient_data.dod)
        return True

    def _agresor_age_year(self):
        def compute_age_year_from_dates (patient_dob):
            now=datetime.datetime.now()
            yearss = ''
            if (patient_dob):
                dob=datetime.datetime.strptime(patient_dob.strftime('%Y-%m-%d'), '%Y-%m-%d')
                delta= now - dob
                yearss = str(delta.days // 365)+" Años"
            return yearss
        for patient_year in self:
            patient_year.age_year = compute_age_year_from_dates(patient_year.dob)
        return True

    def _agresor_age_month(self):
        def compute_age_month_from_dates (patient_dob):
            now=datetime.datetime.now()
            meses = ''
            if (patient_dob):
                dob=datetime.datetime.strptime(patient_dob.strftime('%Y-%m-%d'), '%Y-%m-%d')
                delta= now - dob
                meses = str((delta.days%365) // 30)+" Meses"
            return meses
        for patient_months in self:
            patient_months.age_month = compute_age_month_from_dates(patient_months.dob)
        return True

    def _compute_condicion(self):
        for record in self:
            if record.dob:
                age = (datetime.datetime.now().date() - record.dob).days // 365
                condicion = self.env['sitrad.condicion'].search([
                    ('rang_min', '<=', age),
                    ('rang_max', '>=', age)
                ], limit=1)
                record.condicion = condicion
                
    def _get_empleado(self):
        empleado_obj = self.env['res.partner']
        domain = [('user_id', '=', self.env.uid)]
        user_ids = empleado_obj.search(domain, limit=1)
        if user_ids:
            return user_ids.id or False
        else:
            return False

    name = fields.Char(string="Apellidos y Nombres")
    identificador = fields.Char(string='Identificador', readonly=True, required=True, default=lambda *a: '/')
    date = fields.Datetime(string='Fecha Registro', readonly=True, default=lambda self: fields.datetime.now())
    registra = fields.Many2one('res.partner', string='Registrad@r', default=_get_empleado, readonly=True)
    tipo_doc = fields.Many2one('sitrad.tipo_doc', string="Tipo de Identificacion", default=lambda self: self._get_default_tipo_doc())
    nro_doc = fields.Char(string="Nro. Doc")
    dob = fields.Date(string='Fecha de Nacimiento')
    deceased = fields.Boolean(string='¿Paciente fallecid@?')
    dod = fields.Date(string='Fecha de muerte')
    age = fields.Char(compute=_agresor_age, size=32, string='Edad', readonly=False, store=True, index=True)
    age_year = fields.Char(compute=_agresor_age_year, size=32, string='Edad Años', readonly=False, store=True, index=True)
    age_month = fields.Char(compute=_agresor_age_month, size=32, string='Edad Meses', readonly=False, store=True, index=True)
    sex = fields.Many2one('sitrad.sexo', string='Sexo', index=True)
    gen = fields.Many2one('sitrad.genero', string='Genero', index=True)
    civil = fields.Many2one('sitrad.marital_status', string='Estado Civil', index=True)
    condicion = fields.Many2one('sitrad.condicion', string='Condicion', store=True)
    hijos = fields.Float(string='Hijos')
    telefono = fields.Char(string="Telefono")
    distrito = fields.Char(string="Distrito")
    procedencia = fields.Char(string="Procedencia")

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('sitrad.agresores')
        vals['identificador'] = sequence or '/'
        inno_agresores = super(SitradAgresores, self).create(vals)
        return inno_agresores

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('nro_doc', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # def name_get(self):
    #     return [(box.nro_doc, '[%s] %s' % (box.nro_doc, box.name)) for box in self]

    def _get_default_tipo_doc(self):
        default_tipo_doc_id = 3
        return default_tipo_doc_id

    
    @api.onchange('nro_doc')
    def _onchange_nro_doc(self):

        validar_obj = self.env['sitrad.agresores']
        domain = [('nro_doc', '=', self.nro_doc)]
        validar_ids = validar_obj.search(domain, limit=1)
                
        if validar_ids:
            if self.nro_doc==False:
                return
            else:
                raise UserError(_('Ya existe el DNI/RUC registrado con : %s %s') % (validar_ids.nro_doc,validar_ids.name))
        else:
            self.get_data_dni()

    def get_data_dni(self):
        result = self.l10n_pe_dni_connection(self.nro_doc)
        if result:
            self.name = str(result['nombre'] or '').strip()

    def l10n_pe_dni_connection(self, dni):
        data = {}
        data = self.nejer_api_connection(dni)
        return data

    @api.model     
    def nejer_api_connection(self, dni):
        url = 'https://girame.net.pe/api/1.0/consultadni/{dni}'.format(dni=dni)
        data = {}
        try:
            r = requests.get(url,timeout=(15))
            result = r.json()
            name = result.get('data').get('nomape')
            data['nombre'] = name
        except Exception :
            data = False
        return data


class SitradDenAgre(models.Model):
    _name = 'sitrad.den_agresor'
    _description = 'Lista de agresores en Denuncia'

    name = fields.Char(string='Identificador', readonly=True, required=True, default=lambda *a: '/')
    agresor = fields.Many2one('sitrad.agresores', string="Agresor Den.")
    parentesco = fields.Many2one('sitrad.parentesco', string="Parentesco")
    denuncia_id = fields.Many2one('sitrad.denuncias', string="Nro. Denuncia")

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('sitrad.den_agresor')
        vals['name'] = sequence or '/'
        inno_agresores = super(SitradDenAgre, self).create(vals)
        return inno_agresores