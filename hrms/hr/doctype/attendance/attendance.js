// Copyright (c) 2022, nts Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

nts.ui.form.on("Attendance", {
	refresh(frm) {
		if (frm.doc.__islocal && !frm.doc.attendance_date) {
			frm.set_value("attendance_date", nts.datetime.get_today());
		}

		frm.set_query("employee", () => {
			return {
				query: "prodman.controllers.queries.employee_query",
			};
		});
	},
});
