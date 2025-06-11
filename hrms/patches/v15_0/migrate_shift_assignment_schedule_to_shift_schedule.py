import nts

from hrms.hr.doctype.shift_schedule.shift_schedule import get_or_insert_shift_schedule


def execute():
	if not nts.db.has_table("Shift Assignment Schedule"):
		return

	fields = ["name", "shift_type", "frequency", "employee", "shift_status", "enabled", "create_shifts_after"]
	for doc in nts.get_all("Shift Assignment Schedule", fields=fields):
		repeat_on_days = nts.get_all(
			"Assignment Rule Day", {"parent": doc.name}, pluck="day", distinct=True
		)
		shift_schedule_name = get_or_insert_shift_schedule(doc.shift_type, doc.frequency, repeat_on_days)

		schedule_assignment = nts.get_doc(
			{
				"doctype": "Shift Schedule Assignment",
				"shift_schedule": shift_schedule_name,
				"employee": doc.employee,
				"shift_status": doc.shift_status,
				"enabled": doc.enabled,
				"create_shifts_after": doc.create_shifts_after,
			}
		).insert()

		for d in nts.get_all("Shift Assignment", filters={"schedule": doc.name}, pluck="name"):
			nts.db.set_value("Shift Assignment", d, "shift_schedule_assignment", schedule_assignment.name)
