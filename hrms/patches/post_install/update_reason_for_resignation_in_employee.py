# Copyright (c) 2020, nts Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import nts


def execute():
	nts.reload_doc("setup", "doctype", "employee")

	if nts.db.has_column("Employee", "reason_for_resignation"):
		nts.db.sql(
			""" UPDATE `tabEmployee`
            SET reason_for_leaving = reason_for_resignation
            WHERE status = 'Left' and reason_for_leaving is null and reason_for_resignation is not null
        """
		)
