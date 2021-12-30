from odoo import models,fields,api,_


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _order='id desc'
    _description = 'Doctor Record'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'doctor_name'



    doctor_name = fields.Char(string='Name', required=True)
    doctor_age = fields.Integer('Age',track_visibility='always')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], default='female', string="Gender"
    )
    notes = fields.Text(string='Notes')

    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        index=True, default=lambda self:_('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or _('New')

        result = super(HospitalDoctor, self).create(vals)
        return result
