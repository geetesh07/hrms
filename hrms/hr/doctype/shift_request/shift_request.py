# Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document
from nts.utils import get_link_to_form

from hrms.hr.doctype.shift_assignment.shift_assignment import has_overlapping_timings
from hrms.hr.utils import share_doc_with_approver, validate_active_employee
from hrms.mixins.pwa_notifications import PWANotificationsMixin


class OverlappingShiftRequestError(nts.ValidationError):
	pass


class ShiftRequest(Document, PWANotificationsMixin):
	def validate(self):
		validate_active_employee(self.employee)
		self.validate_from_to_dates("from_date", "to_date")
		self.validate_overlapping_shift_requests()
		self.validate_approver()
		self.validate_default_shift()

	def on_update(self):
		share_doc_with_approver(self, self.approver)
		self.notify_approval_status()

	def after_insert(self):
		self.notify_approver()

	def on_submit(self):
		if self.status not in ["Approved", "Rejected"]:
			nts.throw(_("Only Shift Request with status 'Approved' and 'Rejected' can be submitted"))
		if self.status == "Approved":
			assignment_doc = nts.new_doc("Shift Assignment")
			assignment_doc.company = self.company
			assignment_doc.shift_type = self.shift_type
			assignment_doc.employee = self.employee
			assignment_doc.start_date = self.from_date
			if self.to_date:
				assignment_doc.end_date = self.to_date
			assignment_doc.shift_request = self.name
			assignment_doc.flags.ignore_permissions = 1
			assignment_doc.insert()
			assignment_doc.submit()

			nts.msgprint(
				_("Shift Assignment: {0} created for Employee: {1}").format(
					nts.bold(assignment_doc.name), nts.bold(self.employee)
				)
			)

	def on_cancel(self):
		shift_assignment_list = nts.db.get_all(
			"Shift Assignment", {"employee": self.employee, "shift_request": self.name, "docstatus": 1}
		)
		if shift_assignment_list:
			for shift in shift_assignment_list:
				shift_assignment_doc = nts.get_doc("Shift Assignment", shift["name"])
				shift_assignment_doc.cancel()

	def validate_default_shift(self):
		default_shift = nts.get_value("Employee", self.employee, "default_shift")
		if self.shift_type == default_shift:
			nts.throw(
				_("You can not request for your Default Shift: {0}").format(nts.bold(self.shift_type))
			)

	def validate_approver(self):
		department = nts.get_value("Employee", self.employee, "department")
		shift_approver = nts.get_value("Employee", self.employee, "shift_request_approver")
		approvers = nts.db.sql(
			"""select approver from `tabDepartment Approver` where parent= %s and parentfield = 'shift_request_approver'""",
			(department),
		)
		approvers = [approver[0] for approver in approvers]
		approvers.append(shift_approver)
		if self.approver not in approvers:
			nts.throw(_("Only Approvers can Approve this Request."))

	def validate_overlapping_shift_requests(self):
		overlapping_dates = self.get_overlapping_dates()
		if len(overlapping_dates):
			# if dates are overlapping, check if timings are overlapping, else allow
			for d in overlapping_dates:
				if has_overlapping_timings(self.shift_type, d.shift_type):
					self.throw_overlap_error(d)

	def get_overlapping_dates(self):
		if not self.name:
			self.name = "New Shift Request"

		shift = nts.qb.DocType("Shift Request")
		query = (
			nts.qb.from_(shift)
			.select(shift.name, shift.shift_type)
			.where(
				(shift.employee == self.employee)
				& (shift.docstatus < 2)
				& (shift.name != self.name)
				& ((shift.to_date >= self.from_date) | (shift.to_date.isnull()))
			)
		)

		if self.to_date:
			query = query.where(shift.from_date <= self.to_date)

		return query.run(as_dict=True)

	def throw_overlap_error(self, shift_details):
		shift_details = nts._dict(shift_details)
		msg = _(
			"Employee {0} has already applied for Shift {1}: {2} that overlaps within this period"
		).format(
			nts.bold(self.employee),
			nts.bold(shift_details.shift_type),
			get_link_to_form("Shift Request", shift_details.name),
		)

		nts.throw(msg, title=_("Overlapping Shift Requests"), exc=OverlappingShiftRequestError)
