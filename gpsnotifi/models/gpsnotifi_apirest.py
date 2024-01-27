from odoo import api, fields, models, exceptions

class gpsnotifiApirest(models.Model):
    _name = "gpsnotifi.apirest"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "GPS Notificador"

    name = fields.Char(string="Identificador")
    date = fields.Date(string='Fecha Registro')
    barcode = fields.Char(string="Codigo de Barra")
    cedula = fields.Char(string="Nro. Cédula")
    expediente = fields.Char(string="Exp. Nro.")
    juzgado= fields.Char(string="Juzgado")
    image_ced = fields.Image(string="Cedula")
    image_casa = fields.Image(string="Casa")
    latitude = fields.Char(string="Latitud")
    longitude = fields.Char(string="Longitud")
    image_const = fields.Image(string="Constancia")
    notificador = fields.Many2one('res.partner', string='notificador', readonly=False)
    registra = fields.Many2one('res.partner', string='Registrad@r', readonly=False)