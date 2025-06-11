import nts


def execute():
	nts.reload_doc("hr", "doctype", "employee_advance")

	advance = nts.qb.DocType("Employee Advance")
	(
		nts.qb.update(advance)
		.set(advance.status, "Returned")
		.where(
			(advance.docstatus == 1)
			& ((advance.return_amount) & (advance.paid_amount == advance.return_amount))
			& (advance.status == "Paid")
		)
	).run()

	(
		nts.qb.update(advance)
		.set(advance.status, "Partly Claimed and Returned")
		.where(
			(advance.docstatus == 1)
			& (
				(advance.claimed_amount & advance.return_amount)
				& (advance.paid_amount == (advance.return_amount + advance.claimed_amount))
			)
			& (advance.status == "Paid")
		)
	).run()
