# Copyright (c) 2024, nts Technologies Pvt. Ltd. and Contributors
# See license.txt

# import nts
from nts.tests import IntegrationTestCase, UnitTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class TestShiftScheduleAssignment(IntegrationTestCase):
	"""
	Integration tests for ShiftScheduleAssignment.
	Use this class for testing interactions between multiple components.
	"""

	pass
