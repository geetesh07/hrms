import nts


def execute():
	salary_structure = nts.qb.DocType("Salary Structure")
	nts.qb.update(salary_structure).set(salary_structure.payroll_frequency, "").where(
		salary_structure.salary_slip_based_on_timesheet == 1
	).run()
