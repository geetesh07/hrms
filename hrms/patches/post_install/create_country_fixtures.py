import nts

from hrms.overrides.company import make_salary_components, run_regional_setup


def execute():
	for country in nts.get_all("Company", pluck="country", distinct=True):
		run_regional_setup(country)
		make_salary_components(country)
