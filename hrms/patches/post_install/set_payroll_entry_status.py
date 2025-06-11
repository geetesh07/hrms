import nts


def execute():
	PayrollEntry = nts.qb.DocType("Payroll Entry")

	status = (
		nts.qb.terms.Case()
		.when(PayrollEntry.docstatus == 0, "Draft")
		.when(PayrollEntry.docstatus == 1, "Submitted")
		.else_("Cancelled")
	)

	(nts.qb.update(PayrollEntry).set("status", status).where(PayrollEntry.status.isnull())).run()
