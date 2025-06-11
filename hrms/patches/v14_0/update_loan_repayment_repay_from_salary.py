import nts


def execute():
	if nts.db.exists("Custom Field", "Loan Repayment-repay_from_salary"):
		nts.db.set_value(
			"Custom Field",
			"Loan Repayment-repay_from_salary",
			{"fetch_from": None, "fetch_if_empty": 0},
		)
