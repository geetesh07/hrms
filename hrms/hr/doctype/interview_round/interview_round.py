# Copyright (c) 2021, nts Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import json

import nts
from nts.model.document import Document


class InterviewRound(Document):
	pass


@nts.whitelist()
def create_interview(doc):
	if isinstance(doc, str):
		doc = json.loads(doc)
		doc = nts.get_doc(doc)

	interview = nts.new_doc("Interview")
	interview.interview_round = doc.name
	interview.designation = doc.designation

	if doc.interviewers:
		interview.interview_details = []
		for d in doc.interviewers:
			interview.append("interview_details", {"interviewer": d.user})

	return interview
