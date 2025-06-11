# Copyright (c) 2019, nts and Contributors
# License: GNU General Public License v3. See license.txt

import nts

from hrms.regional.india.setup import make_custom_fields


def execute():
	company = nts.get_all("Company", filters={"country": "India"})
	if not company:
		return

	make_custom_fields()

	nts.reload_doc("payroll", "doctype", "income_tax_slab")
