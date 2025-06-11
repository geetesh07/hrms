// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

nts.query_reports["Salary Payments via ECS"] = $.extend(
	{},
	hrms.salary_slip_deductions_report_filters,
);

nts.query_reports["Salary Payments via ECS"]["filters"].push({
	fieldname: "type",
	label: __("Type"),
	fieldtype: "Select",
	options: ["", "Bank", "Cash", "Cheque"],
});
