// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Timesheet", {
	refresh(frm) {
		if (frm.doc.docstatus === 1 && nts.model.can_create("Salary Slip")) {
			if (!frm.doc.salary_slip && frm.doc.employee) {
				frm.add_custom_button(__("Create Salary Slip"), function () {
					frm.trigger("make_salary_slip");
				});
			}
		}
	},

	make_salary_slip: function (frm) {
		nts.model.open_mapped_doc({
			method: "hrms.payroll.doctype.salary_slip.salary_slip.make_salary_slip_from_timesheet",
			frm: frm,
		});
	},
});
