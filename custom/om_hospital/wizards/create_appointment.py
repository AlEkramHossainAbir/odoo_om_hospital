from odoo import models,fields,_

class CreateAppointment(models.TransientModel):
    _name= "create.appointment"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date= fields.Date(string="Appointment Date")

    def print_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        # if data['form']['patient_id']:
        #     selected_patient = data['form']['patient_id'][0]
        #     appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])
        # else:
        #     appointments = self.env['hospital.appointment'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date
        #     }
        #     appointment_list.append(vals)
        # data['appointments'] = appointment_list
        return self.env.ref('om_hospital.report_appointment_id').report_action(self, data=data)

    def create_Appointment(self):
         vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code'
        }
         self.patient_id.message_post(body="Appointment Created Successfully ", subject="Appointment Creation")
         self.env['hospital.appointment'].create(vals)



    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        print("Appointments ", appointments)
        for rec in appointments:
            print("Appointment Name", rec.name)
        # return {
        #     "type":"ir.actions.do_nothing",
        # }

    def remove_data(self):
        for rec in self:
            rec.patient_id.unlink()
