# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VehicleDriver(Document):
	def validate(self):
		users = frappe.get_list("User",
            		fields=["full_name"],
            	filters = {
                	"email": self.user,
            	})
		#print("Yo yoyo yo %s" % (users))
		if(users):
			self.full_name=users[0]['full_name']

