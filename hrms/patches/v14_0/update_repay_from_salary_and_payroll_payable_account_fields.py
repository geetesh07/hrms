import nts


def execute():
	if nts.db.exists("Custom Field", {"name": "Loan Repayment-repay_from_salary"}):
		nts.db.set_value("Custom Field", {"name": "Loan Repayment-repay_from_salary"}, "fetch_if_empty", 1)

	if nts.db.exists("Custom Field", {"name": "Loan Repayment-payroll_payable_account"}):
		nts.db.set_value(
			"Custom Field",
			{"name": "Loan Repayment-payroll_payable_account"},
			"insert_after",
			"payment_account",
		)
