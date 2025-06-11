# Copyright (c) 2018, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

import nts
from nts.tests.utils import ntsTestCase

import prodman

test_dependencies = ["Employee", "Leave Type", "Leave Policy"]


class TestLeavePeriod(ntsTestCase):
	pass


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
