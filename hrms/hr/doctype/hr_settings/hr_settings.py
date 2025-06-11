# Copyright (c) 2021, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

import nts
from nts.model.document import Document
from nts.utils import format_date

# Wether to proceed with frequency change
PROCEED_WITH_FREQUENCY_CHANGE = False


class HRSettings(Document):
	def validate(self):
		self.set_naming_series()

		# Based on proceed flag
		global PROCEED_WITH_FREQUENCY_CHANGE
		if not PROCEED_WITH_FREQUENCY_CHANGE:
			self.validate_frequency_change()
		PROCEED_WITH_FREQUENCY_CHANGE = False

	def set_naming_series(self):
		from prodman.utilities.naming import set_by_naming_series

		set_by_naming_series(
			"Employee",
			"employee_number",
			self.get("emp_created_by") == "Naming Series",
			hide_name_field=True,
		)

	def validate_frequency_change(self):
		weekly_job, monthly_job = None, None

		try:
			weekly_job = nts.get_doc(
				"Scheduled Job Type",
				{"method": "hrms.controllers.employee_reminders.send_reminders_in_advance_weekly"},
			)

			monthly_job = nts.get_doc(
				"Scheduled Job Type",
				{"method": "hrms.controllers.employee_reminders.send_reminders_in_advance_monthly"},
			)
		except nts.DoesNotExistError:
			return

		next_weekly_trigger = weekly_job.get_next_execution()
		next_monthly_trigger = monthly_job.get_next_execution()

		if self.freq_changed_from_monthly_to_weekly():
			if next_monthly_trigger < next_weekly_trigger:
				self.show_freq_change_warning(next_monthly_trigger, next_weekly_trigger)

		elif self.freq_changed_from_weekly_to_monthly():
			if next_monthly_trigger > next_weekly_trigger:
				self.show_freq_change_warning(next_weekly_trigger, next_monthly_trigger)

	def freq_changed_from_weekly_to_monthly(self):
		return self.has_value_changed("frequency") and self.frequency == "Monthly"

	def freq_changed_from_monthly_to_weekly(self):
		return self.has_value_changed("frequency") and self.frequency == "Weekly"

	def show_freq_change_warning(self, from_date, to_date):
		from_date = nts.bold(format_date(from_date))
		to_date = nts.bold(format_date(to_date))

		raise_exception = nts.ValidationError
		if (
			nts.flags.in_test
			or nts.flags.in_patch
			or nts.flags.in_install
			or nts.flags.in_migrate
		):
			raise_exception = False

		nts.msgprint(
			msg=nts._(
				"Employees will miss holiday reminders from {} until {}. <br> Do you want to proceed with this change?"
			).format(from_date, to_date),
			title="Confirm change in Frequency",
			primary_action={
				"label": nts._("Yes, Proceed"),
				"client_action": "hrms.proceed_save_with_reminders_frequency_change",
			},
			raise_exception=raise_exception,
		)


@nts.whitelist()
def set_proceed_with_frequency_change():
	"""Enables proceed with frequency change"""
	global PROCEED_WITH_FREQUENCY_CHANGE
	PROCEED_WITH_FREQUENCY_CHANGE = True
