# Copyright (c) 2020, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from nts.model.document import Document

# import nts
import prodman


class IncomeTaxSlab(Document):
	def validate(self):
		if self.company:
			self.currency = prodman.get_company_currency(self.company)
