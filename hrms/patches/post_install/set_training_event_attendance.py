import nts


def execute():
	nts.reload_doc("hr", "doctype", "training_event")
	nts.reload_doc("hr", "doctype", "training_event_employee")

	# no need to run the update query as there is no old data
	if not nts.db.exists("Training Event Employee", {"attendance": ("in", ("Mandatory", "Optional"))}):
		return

	nts.db.sql(
		"""
		UPDATE `tabTraining Event Employee`
		SET is_mandatory = 1
		WHERE attendance = 'Mandatory'
		"""
	)
	nts.db.sql(
		"""
		UPDATE `tabTraining Event Employee`
		SET attendance = 'Present'
		WHERE attendance in ('Mandatory', 'Optional')
	"""
	)
