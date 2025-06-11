# Copyright (c) 2024, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts.model.document import Document

from hrms.hr.utils import set_geolocation_from_coordinates


class ShiftLocation(Document):
	def validate(self):
		self.set_geolocation()

	@nts.whitelist()
	def set_geolocation(self):
		set_geolocation_from_coordinates(self)
