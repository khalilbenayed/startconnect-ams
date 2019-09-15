from flask_restful import fields

company_fields = {
    'id': fields.Integer,
    'company_name': fields.String,
    'email': fields.String,
    'address_1': fields.String,
    'address_2': fields.String,
    'city': fields.String,
    'province': fields.String,
    'zipcode': fields.String,
    'country': fields.String,
    'phone': fields.String,
    'state': fields.String,
}

companies_fields = {
    'companies': fields.List(fields.Nested(company_fields))
}
