import nts


def execute():
	nts.delete_doc("DocType", "Employee Transfer Property", ignore_missing=True)
