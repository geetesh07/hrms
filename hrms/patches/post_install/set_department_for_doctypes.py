import nts

# Set department value based on employee value


def execute():
	doctypes_to_update = {
		"hr": [
			"Appraisal",
			"Leave Allocation",
			"Expense Claim",
			"Salary Slip",
			"Attendance",
			"Training Feedback",
			"Training Result Employee",
			"Leave Application",
			"Employee Advance",
			"Training Event Employee",
			"Payroll Employee Detail",
		],
		"education": ["Instructor"],
		"projects": ["Activity Cost", "Timesheet"],
		"setup": ["Sales Person"],
	}

	for module, doctypes in doctypes_to_update.items():
		for doctype in doctypes:
			if nts.db.table_exists(doctype):
				nts.reload_doc(module, "doctype", nts.scrub(doctype))
				nts.db.sql(
					f"""
					update `tab{doctype}` dt
					set department=(select department from `tabEmployee` where name=dt.employee)
					where coalesce(`tab{doctype}`.`department`, '') = ''
					"""
				)
