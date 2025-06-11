# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts import _
from nts.model.document import Document
from nts.utils import get_link_to_form

from prodman.setup.doctype.employee.employee import get_employee_email


class ExitInterview(Document):
	def validate(self):
		self.validate_relieving_date()
		self.validate_duplicate_interview()
		self.set_employee_email()

	def validate_relieving_date(self):
		if not nts.db.get_value("Employee", self.employee, "relieving_date"):
			nts.throw(
				_("Please set the relieving date for employee {0}").format(
					get_link_to_form("Employee", self.employee)
				),
				title=_("Relieving Date Missing"),
			)

	def validate_duplicate_interview(self):
		doc = nts.db.exists(
			"Exit Interview", {"employee": self.employee, "name": ("!=", self.name), "docstatus": ("!=", 2)}
		)
		if doc:
			nts.throw(
				_("Exit Interview {0} already exists for Employee: {1}").format(
					get_link_to_form("Exit Interview", doc), nts.bold(self.employee)
				),
				nts.DuplicateEntryError,
			)

	def set_employee_email(self):
		employee = nts.get_doc("Employee", self.employee)
		self.email = get_employee_email(employee)

	def on_submit(self):
		if self.status != "Completed":
			nts.throw(_("Only Completed documents can be submitted"))

		self.update_interview_date_in_employee()

	def on_cancel(self):
		self.update_interview_date_in_employee()
		self.db_set("status", "Cancelled")

	def update_interview_date_in_employee(self):
		if self.docstatus == 1:
			nts.db.set_value("Employee", self.employee, "held_on", self.date)
		elif self.docstatus == 2:
			nts.db.set_value("Employee", self.employee, "held_on", None)


@nts.whitelist()
def send_exit_questionnaire(interviews):
	interviews = get_interviews(interviews)
	validate_questionnaire_settings()

	email_success = []
	email_failure = []

	for exit_interview in interviews:
		interview = nts.get_doc("Exit Interview", exit_interview.get("name"))
		if interview.get("questionnaire_email_sent"):
			continue

		employee = nts.get_doc("Employee", interview.employee)
		email = get_employee_email(employee)

		context = interview.as_dict()
		context.update(employee.as_dict())
		template_name = nts.db.get_single_value("HR Settings", "exit_questionnaire_notification_template")
		template = nts.get_doc("Email Template", template_name)

		if email:
			nts.sendmail(
				recipients=email,
				subject=template.subject,
				message=nts.render_template(template.response, context),
				reference_doctype=interview.doctype,
				reference_name=interview.name,
			)
			interview.db_set("questionnaire_email_sent", 1)
			interview.notify_update()
			email_success.append(email)
		else:
			email_failure.append(get_link_to_form("Employee", employee.name))

	show_email_summary(email_success, email_failure)


def get_interviews(interviews):
	import json

	if isinstance(interviews, str):
		interviews = json.loads(interviews)

	if not len(interviews):
		nts.throw(_("At least one interview has to be selected."))

	return interviews


def validate_questionnaire_settings():
	settings = nts.db.get_value(
		"HR Settings",
		"HR Settings",
		["exit_questionnaire_web_form", "exit_questionnaire_notification_template"],
		as_dict=True,
	)

	if not settings.exit_questionnaire_web_form or not settings.exit_questionnaire_notification_template:
		nts.throw(
			_("Please set {0} and {1} in {2}.").format(
				nts.bold(_("Exit Questionnaire Web Form")),
				nts.bold(_("Notification Template")),
				get_link_to_form("HR Settings", "HR Settings"),
			),
			title=_("Settings Missing"),
		)


def show_email_summary(email_success, email_failure):
	message = ""
	if email_success:
		message += _("Sent Successfully: {0}").format(", ".join(email_success))
	if message and email_failure:
		message += "<br><br>"
	if email_failure:
		message += _("Sending Failed due to missing email information for employee(s): {1}").format(
			", ".join(email_failure)
		)

	nts.msgprint(message, title=_("Exit Questionnaire"), indicator="blue", is_minimizable=True, wide=True)
