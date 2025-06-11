import nts


def execute():
	onboarding_template = nts.qb.DocType("Employee Onboarding Template")
	(
		nts.qb.update(onboarding_template)
		.set(onboarding_template.title, onboarding_template.designation)
		.where(onboarding_template.title.isnull())
	).run()

	separation_template = nts.qb.DocType("Employee Separation Template")
	(
		nts.qb.update(separation_template)
		.set(separation_template.title, separation_template.designation)
		.where(separation_template.title.isnull())
	).run()
