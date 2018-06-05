from django.contrib import admin
from .models import *
import xmlrpclib

# odoo database credentials
db_username = 'minasamy@gmail.com'
db_password = 123456
db_name = 'odoo'

# establishing connection with DB to get admin id
sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
db_user_id = sock_common.login(db_name, db_username, db_password)

# establishe connection with odoo server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')


class InlineTickets(admin.StackedInline):
    model = Tickets
    extra = 2


class CustomCustomer(admin.ModelAdmin):
    inlines = [InlineTickets]

    ################################### Customers Model ###################################
    #override original save_model for customers
    def save_model(self, request, obj, form, change):
        partner = {'name': obj.name, 'phone': obj.mobile}
        partner_id = sock.execute(db_name, db_user_id, db_password, 'res.partner', 'create', partner)
        print("**************************************")
        print('new partner created with id', partner_id)
        print("**************************************")
        super(CustomCustomer, self).save_model(request, obj, form, change)

    #override delete_model
    def delete_model(modeladmin, request, queryset):
        print("***********************")
        unwanted_customer_id = sock.execute(db_name, db_user_id, db_password, 'res.partner', 'search',[['name', '=', queryset.name], ['phone', '=', queryset.mobile]])
        respone = sock.execute(db_name, db_user_id, db_password, 'res.partner', 'unlink', unwanted_customer_id)
        queryset.delete()
        print("***********************")
        print("Partener of id ", unwanted_customer_id, " Removed Succesfully ")
        print("***********************")



            ################################### Tickets Model ###################################


class CustomTickets(admin.ModelAdmin):
    # override  save_model for tickets
    def save_model(self, request, obj, form, change):

    	if not change:
        	data = {'name': obj.name,'description':obj.name,'price': 10000}
        	ticket_id = sock.execute(db_name, db_user_id, db_password, 'machine.machines', 'create', data)
        	print("**************************************")
        	print('new ticket created with id', ticket_id)
        	print("**************************************")
        	super(CustomTickets,self).save_model(request, obj, form, change)

    # override delete_model for tickets
    def delete_model(modeladmin, request, queryset):
        print("***********************")
        unwanted_ticket_id = sock.execute(db_name, db_user_id, db_password, 'machine.machines', 'search', [['name','=', queryset.name],['description','=',queryset.name]])
        print(unwanted_ticket_id)
        respone = sock.execute(db_name, db_user_id, db_password, 'machine.machines', 'unlink', unwanted_ticket_id)

        if respone:
            queryset.delete()
            print("***********************")
            print("Ticket of id ", unwanted_ticket_id, " Removed Succesfully ")
            print("***********************")


admin.site.register(Customer, CustomCustomer)
admin.site.register(Tickets,CustomTickets)
