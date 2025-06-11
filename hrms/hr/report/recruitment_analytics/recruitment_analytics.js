// Copyright (c) 2016, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

nts.query_reports["Recruitment Analytics"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: nts.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "on_date",
			label: __("On Date"),
			fieldtype: "Date",
			default: nts.datetime.now_date(),
			reqd: 1,
		},
	],
};
