import nts


def execute():
	nts.clear_cache(doctype="Leave Type")

	if nts.db.has_column("Leave Type", "based_on_date_of_joining"):
		LeaveType = nts.qb.DocType("Leave Type")
		nts.qb.update(LeaveType).set(LeaveType.allocate_on_day, "Last Day").where(
			(LeaveType.based_on_date_of_joining == 0) & (LeaveType.is_earned_leave == 1)
		).run()

		nts.qb.update(LeaveType).set(LeaveType.allocate_on_day, "Date of Joining").where(
			LeaveType.based_on_date_of_joining == 1
		).run()

		nts.db.sql_ddl("alter table `tabLeave Type` drop column `based_on_date_of_joining`")
		# clear cache for doctype as it stores table columns in cache
		nts.clear_cache(doctype="Leave Type")
