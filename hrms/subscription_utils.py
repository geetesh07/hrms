import requests

import nts

STANDARD_ROLES = [
	# standard roles
	"Administrator",
	"All",
	"Guest",
	# accounts
	"Accounts Manager",
	"Accounts User",
	# projects
	"Projects User",
	"Projects Manager",
	# framework
	"Blogger",
	"Dashboard Manager",
	"Inbox User",
	"Newsletter Manager",
	"Prepared Report User",
	"Report Manager",
	"Script Manager",
	"System Manager",
	"Website Manager",
	"Workspace Manager",
]


@nts.whitelist(allow_guest=True)
def get_add_on_details(plan: str) -> dict[str, int]:
	"""
	Returns the number of employees to be billed under add-ons for SAAS subscription
	site_details = {
	        "country": "India",
	        "plan": "Basic",
	        "credit_balance": 1000,
	        "add_ons": {
	                "employee": 2,
	        },
	        "expiry_date": "2021-01-01", # as per current usage
	}
	"""
	EMPLOYEE_LIMITS = {"Basic": 25, "Essential": 50, "Professional": 100}
	add_on_details = {}

	employees_included_in_plan = EMPLOYEE_LIMITS.get(plan)
	if employees_included_in_plan:
		active_employees = get_active_employees()
		add_on_employees = (
			active_employees - employees_included_in_plan
			if active_employees > employees_included_in_plan
			else 0
		)
	else:
		add_on_employees = 0

	add_on_details["employees"] = add_on_employees
	return add_on_details


def get_active_employees() -> int:
	return nts.db.count("Employee", {"status": "Active"})


@nts.whitelist(allow_guest=True)
def subscription_updated(app: str, plan: str):
	if app in ["hrms", "prodman"] and plan:
		update_prodman_access()


def update_prodman_access(user_input: dict | None):
	"""
	Called from hooks after setup wizard completion, ignored if user has no hrms subscription
	enables prodman workspaces and roles if user has subscribed to both hrms and prodman
	disables prodman workspaces and roles if user has subscribed to hrms but not prodman
	"""
	if not nts.utils.get_url().endswith(".ntshr.com"):
		return

	update_prodman_workspaces(True)
	update_prodman_roles(True)
	set_app_logo()


def update_prodman_workspaces(disable: bool = True):
	prodman_workspaces = [
		"Home",
		"Assets",
		"Accounting",
		"Buying",
		"CRM",
		"Manufacturing",
		"Quality",
		"Selling",
		"Stock",
		"Support",
	]

	for workspace in prodman_workspaces:
		try:
			workspace_doc = nts.get_doc("Workspace", workspace)
			workspace_doc.flags.ignore_links = True
			workspace_doc.flags.ignore_validate = True
			workspace_doc.public = 0 if disable else 1
			workspace_doc.save()
		except Exception:
			nts.clear_messages()


def update_prodman_roles(disable: bool = True):
	roles = get_prodman_roles()
	for role in roles:
		try:
			role_doc = nts.get_doc("Role", role)
			role_doc.disabled = disable
			role_doc.flags.ignore_links = True
			role_doc.save()
		except Exception:
			pass


def set_app_logo():
	nts.db.set_single_value("Navbar Settings", "app_logo", "/assets/hrms/images/nts-hr-logo.svg")


def get_prodman_roles() -> set:
	prodman_roles = get_roles_for_app("prodman")
	hrms_roles = get_roles_for_app("hrms")
	return prodman_roles - hrms_roles - set(STANDARD_ROLES)


def get_roles_for_app(app_name: str) -> set:
	prodman_modules = get_modules_by_app(app_name)
	doctypes = get_doctypes_by_modules(prodman_modules)
	roles = roles_by_doctype(doctypes)

	return roles


def get_modules_by_app(app_name: str) -> list:
	return nts.db.get_all("Module Def", filters={"app_name": app_name}, pluck="name")


def get_doctypes_by_modules(modules: list) -> list:
	return nts.db.get_all("DocType", filters={"module": ("in", modules)}, pluck="name")


def roles_by_doctype(doctypes: list) -> set:
	roles = []
	for d in doctypes:
		permissions = nts.get_meta(d).permissions

		for d in permissions:
			roles.append(d.role)

	return set(roles)


def hide_prodman() -> bool:
	hr_subscription = has_subscription(nts.conf.sk_hrms)
	prodman_subscription = has_subscription(nts.conf.sk_prodman_smb or nts.conf.sk_prodman)

	if not hr_subscription:
		return False

	if hr_subscription and prodman_subscription:
		# subscribed for prodman
		return False

	# no subscription for prodman
	return True


def has_subscription(secret_key) -> bool:
	url = f"https://ntscloud.com/api/method/press.api.developer.marketplace.get_subscription_status?secret_key={secret_key}"
	response = requests.request(method="POST", url=url, timeout=5)

	status = response.json().get("message")
	return True if status == "Active" else False
