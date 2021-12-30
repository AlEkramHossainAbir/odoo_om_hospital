from odoo import models,fields,api,_
import pytz



class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = "id desc,appointment_date desc"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')

        result = super(HospitalAppointment, self).create(vals)
        return result


    def write(self, vals):
        # overriding the write method of appointment model
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        # do as per the need
        return res

    def _get_default_note(self):
        return "Do WHatever you want"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        index=True, default=lambda self:_('New'))


    patient_id = fields.Many2one('hospital.patient',string='Patient', required=True,ondelete='cascade')
    patient_age = fields.Integer('Age',related='patient_id.patient_age')
    appointment_lines= fields.One2many('hospital.appointment.lines','appointment_id',string="appointment lines")
    notes = fields.Text(string='Reg Notes',default=_get_default_note)
    appointment_date = fields.Date(string='Date',required=True)
    appointment_datetime = fields.Datetime(string='Date Time')
    partner_id= fields.Many2one('res.partner',string="Customer")
    order_id= fields.Many2one('sale.order',string="Sale Order")
    amount=fields.Float(default=0.0)
    state=fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done'),
        ('cancel','Cancelled')
    ],string='Status',readonly=True,default='draft')


    def action_confirm(self):
        for rec in self:
            rec.state='confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed',
                    'type': 'rainbow_man',

                }
            }

    def action_done(self):
        for rec in self:
            rec.state='done'

    def delete_lines(self):
        for rec in self:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            time_in_timezone = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            print("user time zone ",user_tz);
            print("Time in UTC -->", rec.appointment_datetime)
            print("Time in Users Timezone -->", time_in_timezone)
            rec.appointment_lines = [(5, 0, 0)]

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id= fields.Many2one('product.product',string= 'product')
    product_qty= fields.Integer(string="Quantity")
    appointment_id= fields.Many2one('hospital.appointment',string='Appointment ID')