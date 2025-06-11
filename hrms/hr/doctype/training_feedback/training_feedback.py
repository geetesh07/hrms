# Copyright (c) 2015, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document


class TrainingFeedback(Document):
	def validate(self):
		training_event = nts.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			nts.throw(_("{0} must be submitted").format(_("Training Event")))

		emp_event_details = nts.db.get_value(
			"Training Event Employee",
			{"parent": self.training_event, "employee": self.employee},
			["name", "attendance"],
			as_dict=True,
		)

		if not emp_event_details:
			nts.throw(
				_("Employee {0} not found in Training Event Participants.").format(
					nts.bold(self.employee_name)
				)
			)

		if emp_event_details.attendance == "Absent":
			nts.throw(_("Feedback cannot be recorded for an absent Employee."))

	def on_submit(self):
		employee = nts.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			nts.db.set_value("Training Event Employee", employee, "status", "Feedback Submitted")

	def on_cancel(self):
		employee = nts.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			nts.db.set_value("Training Event Employee", employee, "status", "Completed")
