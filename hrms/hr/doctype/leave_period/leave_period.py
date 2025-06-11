# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document
from nts.utils import getdate

from hrms.hr.utils import validate_overlap


class LeavePeriod(Document):
	def validate(self):
		self.validate_dates()
		validate_overlap(self, self.from_date, self.to_date, self.company)

	def validate_dates(self):
		if getdate(self.from_date) >= getdate(self.to_date):
			nts.throw(_("To date can not be equal or less than from date"))
