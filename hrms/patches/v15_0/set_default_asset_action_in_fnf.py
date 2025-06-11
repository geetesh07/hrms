import nts


def execute():
	FnF = nts.qb.DocType("Full and Final Asset")
	nts.qb.update(FnF).set(FnF.action, "Return").where((FnF.action.isnull()) | (FnF.action == "")).run()
