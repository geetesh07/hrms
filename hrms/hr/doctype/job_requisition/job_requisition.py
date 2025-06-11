# Copyright (c) 2022, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import nts
from nts import _
from nts.model.document import Document
from nts.model.mapper import get_mapped_doc
from nts.utils import format_duration, get_link_to_form, time_diff_in_seconds


class JobRequisition(Document):
	def validate(self):
		self.validate_duplicates()
		self.set_time_to_fill()

	def validate_duplicates(self):
		duplicate = nts.db.exists(
			"Job Requisition",
			{
				"designation": self.designation,
				"department": self.department,
				"requested_by": self.requested_by,
				"status": ("not in", ["Cancelled", "Filled"]),
				"name": ("!=", self.name),
			},
		)

		if duplicate:
			nts.throw(
				_("A Job Requisition for {0} requested by {1} already exists: {2}").format(
					nts.bold(self.designation),
					nts.bold(self.requested_by),
					get_link_to_form("Job Requisition", duplicate),
				),
				title=_("Duplicate Job Requisition"),
			)

	def set_time_to_fill(self):
		if self.status == "Filled" and self.completed_on:
			self.time_to_fill = time_diff_in_seconds(self.completed_on, self.posting_date)

	@nts.whitelist()
	def associate_job_opening(self, job_opening):
		nts.db.set_value(
			"Job Opening", job_opening, {"job_requisition": self.name, "vacancies": self.no_of_positions}
		)
		nts.msgprint(
			_("Job Requisition {0} has been associated with Job Opening {1}").format(
				nts.bold(self.name), get_link_to_form("Job Opening", job_opening)
			),
			title=_("Job Opening Associated"),
		)


@nts.whitelist()
def make_job_opening(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.job_title = source.designation
		target.status = "Open"
		target.currency = nts.db.get_value("Company", source.company, "default_currency")
		target.lower_range = source.expected_compensation
		target.description = source.description

	return get_mapped_doc(
		"Job Requisition",
		source_name,
		{
			"Job Requisition": {
				"doctype": "Job Opening",
			},
			"field_map": {
				"designation": "designation",
				"name": "job_requisition",
				"department": "department",
				"no_of_positions": "vacancies",
			},
		},
		target_doc,
		set_missing_values,
	)


@nts.whitelist()
def get_avg_time_to_fill(company=None, department=None, designation=None):
	filters = {"status": "Filled"}
	if company:
		filters["company"] = company
	if department:
		filters["department"] = department
	if designation:
		filters["designation"] = designation

	avg_time_to_fill = nts.db.get_all(
		"Job Requisition",
		filters=filters,
		fields=["avg(time_to_fill) as average_time"],
	)[0].average_time

	return format_duration(avg_time_to_fill) if avg_time_to_fill else 0
