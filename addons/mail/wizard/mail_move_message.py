# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MailMoveMessage(models.TransientModel):
    _name = 'mail.move.message'
    _description = 'Move a message to another record'

    mail_message_id = fields.Many2one('mail.message', 'Message', readonly=True)
    model = fields.Char('Related Document Model', index=True)
    res_id = fields.Many2oneReference('Related Document ID', index=True, model_field='model')
    subject = fields.Char('Subject')

    def default_get(self, fields_list):
        rec = super(MailMoveMessage, self).default_get(fields_list)
        message = self.env['mail.message'].browse(self.env.context.get('mail_message_to_move', False))
        rec.update({
            'mail_message_id': message.id,
            'model': message.model,
            'res_id': message.res_id,
            'subject': message.subject
        })

        return rec

    def move(self):
        self.mail_message_id.write({
            'model': self.model,
            'res_id': self.res_id,
            'parent_id': False
        })
