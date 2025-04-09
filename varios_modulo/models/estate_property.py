from odoo import models,fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer received'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ],default='new',copy=False,required=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))  
    expected_price = fields.Float(  required=True)
    selling_price = fields.Float(readonly=True, copy=False)  
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ],)

    partner_id = fields.Many2one('res.partner', string='Cliente')

    def action_create_invoice(self):
        self.ensure_one()
        if self.state != 'sold':
            raise UserError("La factura solo puede crearse cuando la propiedad está en estado 'sold'.")
    
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': f"Venta de propiedad: {self.name}",
                'quantity': 1,
                'price_unit': self.selling_price or self.expected_price,
            })]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factura',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
        }