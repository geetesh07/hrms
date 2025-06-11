import nts


def execute():
	nts.reload_doc("HR", "doctype", "Leave Allocation")
	nts.reload_doc("HR", "doctype", "Leave Ledger Entry")
	nts.db.sql(
		"""
		UPDATE `tabLeave Ledger Entry` as lle
		SET company = (select company from `tabEmployee` where employee = lle.employee)
		WHERE company IS NULL
		"""
	)
	nts.db.sql(
		"""
		UPDATE `tabLeave Allocation` as la
		SET company = (select company from `tabEmployee` where employee = la.employee)
		WHERE company IS NULL
		"""
	)
