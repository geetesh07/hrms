nts.pages["organizational-chart"].on_page_load = function (wrapper) {
	nts.ui.make_app_page({
		parent: wrapper,
		title: __("Organizational Chart"),
		single_column: true,
	});

	$(wrapper).bind("show", () => {
		nts.require("hierarchy-chart.bundle.js", () => {
			let organizational_chart;
			let method = "hrms.hr.page.organizational_chart.organizational_chart.get_children";

			if (nts.is_mobile()) {
				organizational_chart = new hrms.HierarchyChartMobile("Employee", wrapper, method);
			} else {
				organizational_chart = new hrms.HierarchyChart("Employee", wrapper, method);
			}

			nts.breadcrumbs.add("HR");
			organizational_chart.show();
		});
	});
};
