# Copyright (c) 2018, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts

import prodman

from hrms.tests.utils import HRMSTestSuite

test_dependencies = ["Leave Policy"]


class TestLeavePeriod(HRMSTestSuite):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.make_employees()


def create_leave_period(from_date, to_date, company=None):
	leave_period = nts.db.get_value(
		"Leave Period",
		dict(
			company=company or prodman.get_default_company(),
			from_date=from_date,
			to_date=to_date,
			is_active=1,
		),
		"name",
	)
	if leave_period:
		return nts.get_doc("Leave Period", leave_period)

	leave_period = nts.get_doc(
		{
			"doctype": "Leave Period",
			"company": company or prodman.get_default_company(),
			"from_date": from_date,
			"to_date": to_date,
			"is_active": 1,
		}
	).insert()
	return leave_period
