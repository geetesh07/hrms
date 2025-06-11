# Copyright (c) 2015, nts Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import nts
from nts import _
from nts.model.document import Document
from nts.model.naming import append_number_if_name_exists
from nts.utils import flt, validate_email_address

from hrms.hr.doctype.interview.interview import get_interviewers


class DuplicationError(nts.ValidationError):
	pass


class JobApplicant(Document):
	def onload(self):
		job_offer = nts.get_all("Job Offer", filters={"job_applicant": self.name})
		if job_offer:
			self.get("__onload").job_offer = job_offer[0].name

	def autoname(self):
		self.name = self.email_id

		# applicant can apply more than once for a different job title or reapply
		if nts.db.exists("Job Applicant", self.name):
			self.name = append_number_if_name_exists("Job Applicant", self.name)

	def validate(self):
		if self.email_id:
			validate_email_address(self.email_id, True)

		if self.employee_referral:
			self.set_status_for_employee_referral()

		if not self.applicant_name and self.email_id:
			guess = self.email_id.split("@")[0]
			self.applicant_name = " ".join([p.capitalize() for p in guess.split(".")])

	def before_insert(self):
		if self.job_title:
			job_opening_status = nts.db.get_value("Job Opening", self.job_title, "status")
			if job_opening_status == "Closed":
				nts.throw(
					_("Cannot create a Job Applicant against a closed Job Opening"), title=_("Not Allowed")
				)

	def set_status_for_employee_referral(self):
		emp_ref = nts.get_doc("Employee Referral", self.employee_referral)
		if self.status in ["Open", "Replied", "Hold"]:
			emp_ref.db_set("status", "In Process")
		elif self.status in ["Accepted", "Rejected"]:
			emp_ref.db_set("status", self.status)


@nts.whitelist()
def create_interview(doc, interview_round):
	import json

	if isinstance(doc, str):
		doc = json.loads(doc)
		doc = nts.get_doc(doc)

	round_designation = nts.db.get_value("Interview Round", interview_round, "designation")

	if round_designation and doc.designation and round_designation != doc.designation:
		nts.throw(
			_("Interview Round {0} is only applicable for the Designation {1}").format(
				interview_round, round_designation
			)
		)

	interview = nts.new_doc("Interview")
	interview.interview_round = interview_round
	interview.job_applicant = doc.name
	interview.designation = doc.designation
	interview.resume_link = doc.resume_link
	interview.job_opening = doc.job_title

	interviewers = get_interviewers(interview_round)
	for d in interviewers:
		interview.append("interview_details", {"interviewer": d.interviewer})

	return interview


@nts.whitelist()
def get_interview_details(job_applicant):
	interview_details = nts.db.get_all(
		"Interview",
		filters={"job_applicant": job_applicant, "docstatus": ["!=", 2]},
		fields=["name", "interview_round", "scheduled_on", "average_rating", "status"],
	)
	interview_detail_map = {}
	meta = nts.get_meta("Interview")
	number_of_stars = meta.get_options("average_rating") or 5

	for detail in interview_details:
		detail.average_rating = detail.average_rating * number_of_stars if detail.average_rating else 0

		interview_detail_map[detail.name] = detail

	return {"interviews": interview_detail_map, "stars": number_of_stars}


@nts.whitelist()
def get_applicant_to_hire_percentage():
	total_applicants = nts.db.count("Job Applicant")
	total_hired = nts.db.count("Job Applicant", filters={"status": "Accepted"})

	return {
		"value": flt(total_hired) / flt(total_applicants) * 100 if total_applicants else 0,
		"fieldtype": "Percent",
	}
