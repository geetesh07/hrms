import nts
from nts.model.utils.rename_field import rename_field


def execute():
	nts.reload_doc("hr", "doctype", "hr_settings")

	try:
		# Rename the field
		rename_field("HR Settings", "stop_birthday_reminders", "send_birthday_reminders")

		# Reverse the value
		old_value = nts.db.get_single_value("HR Settings", "send_birthday_reminders")

		nts.db.set_single_value("HR Settings", "send_birthday_reminders", 1 if old_value == 0 else 0)

	except Exception as e:
		if e.args[0] != 1054:
			raise
