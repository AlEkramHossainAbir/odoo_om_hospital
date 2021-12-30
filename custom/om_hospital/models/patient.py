
#config utf-8


from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self,vals_list):
        res = super(ResPartner,self).create()
        print("yes working")
        return res


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name='patient_name'

    @api.model
    def test_cron_job(self):
        print("Abcd")  #

    def name_get(self):
        res=[]
        for field in self:
            res.append((field.id, '%s %s' % (field.patient_name,field.name_seq)))
            return res



    @api.constrains('patient_age')
    def check_age(self):
        for record in self:
            if record.patient_age<=5:
                raise ValidationError(_("Beshi Choto Baba ! Boro Hoye nau"))
            if record.patient_age>=100:
                raise ValidationError(_("Tomar Boyosh Beshi ! Website chalanor shomoy nai"))


    @api.depends('patient_age')
    def set_age_group(self):
        for record in self:
            if record.patient_age<10:
                record.age_group='minor'
            else:
                record.age_group='major'

    def get_appointment_count(self):
            count= self.env['hospital.appointment'].search_count([('patient_id','=',self.id)])
            self.appointment_count=count



    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender= rec.doctor_id.gender
    

    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)


    patient_name = fields.Char(string='Name', required=True, ondelete="cascade")
    patient_age = fields.Integer('Age',track_visibility='always')
    age_group = fields.Char('AgeGroup')
    gender= fields.Char('Gender')
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image')
    appointment_count= fields.Integer(string='APPOINTMENT',compute='get_appointment_count')
    active= fields.Boolean('Active',default=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    email_id = fields.Char(string="Email")
    user_id = fields.Many2one('res.users', string="PRO")
    doctor_gender= fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], string="Gender"
    )

    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        index=True, default=lambda self:_('New'))
    age_group=fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor')
    ],
    default='minor',
    string='Age Group',
    compute='set_age_group'
    )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], default='female', string="Gender"
    )

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')

        result = super(HospitalPatient, self).create(vals)
        return result
   
    def open_patient_appointments(self):
        # raise ValidationError(_("Beshi Choto Baba ! Boro Hoye nau"))
        return{
            'name':_('Appointment'),
            'domain':[('patient_id','=',self.id)],
            'view_type':'form',
            'res_model':'hospital.appointment',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window',


        }   

    def test_name(self):
        pass

    def action_send_card(self):
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        print("Template ID",template_id)
        template = self.env['mail.template'].browse(template_id)
        print("Template",template)
        template.send_mail(self.id, force_send=True)

    # def open_patient_date(self):
    #     pass