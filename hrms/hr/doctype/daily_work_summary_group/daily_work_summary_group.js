// Copyright (c) 2018, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Daily Work Summary Group", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Daily Work Summary"), function () {
				nts.set_route("List", "Daily Work Summary");
			});
		}
	},
});
