# Copyright (c) 2018, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase
from nts.utils import getdate

test_dependencies = ["Employee Onboarding"]


class TestEmployeeSeparation(ntsTestCase):
	def test_employee_separation(self):
		separation = create_employee_separation()

		self.assertEqual(separation.docstatus, 1)
		self.assertEqual(separation.boarding_status, "Pending")

		project = nts.get_doc("Project", separation.project)
		project.percent_complete_method = "Manual"
		project.status = "Completed"
		project.save()

		separation.reload()
		self.assertEqual(separation.boarding_status, "Completed")

		separation.cancel()
		self.assertEqual(separation.project, "")

	def tearDown(self):
		for entry in nts.get_all("Employee Separation"):
			doc = nts.get_doc("Employee Separation", entry.name)
			if doc.docstatus == 1:
				doc.cancel()
			doc.delete()


def create_employee_separation():
	employee = nts.db.get_value("Employee", {"status": "Active", "company": "_Test Company"})
	separation = nts.new_doc("Employee Separation")
	separation.employee = employee
	separation.boarding_begins_on = getdate()
	separation.company = "_Test Company"
	separation.append("activities", {"activity_name": "Deactivate Employee", "role": "HR User"})
	separation.boarding_status = "Pending"
	separation.insert()
	separation.submit()
	return separation
