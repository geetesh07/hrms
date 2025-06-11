// Copyright (c) 2019, nts Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

nts.ui.form.on("Employee Skill Map", {
	// refresh: function(frm) {

	// }
	designation: (frm) => {
		frm.set_value("employee_skills", null);
		if (frm.doc.designation) {
			nts.db.get_doc("Designation", frm.doc.designation).then((designation) => {
				designation.skills.forEach((designation_skill) => {
					let row = nts.model.add_child(frm.doc, "Employee Skill", "employee_skills");
					row.skill = designation_skill.skill;
					row.proficiency = 1;
				});
				refresh_field("employee_skills");
			});
		}
	},
});
