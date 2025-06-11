import nts
from nts import _
from nts.desk.doctype.notification_log.notification_log import make_notification_logs
from nts.utils.user import get_system_managers


def execute():
	if "lending" in nts.get_installed_apps():
		return

	if nts.db.a_row_exists("Salary Slip Loan"):
		notify_existing_users()


def notify_existing_users():
	subject = _("WARNING: Loan Management module has been separated from prodman.") + "<br>"
	subject += _(
		"If you are using loans in salary slips, please install the {0} app from nts Cloud Marketplace or GitHub to continue using loan integration with payroll."
	).format(nts.bold("Lending"))

	notification = {
		"subject": subject,
		"type": "Alert",
	}
	make_notification_logs(notification, get_system_managers(only_name=True))
