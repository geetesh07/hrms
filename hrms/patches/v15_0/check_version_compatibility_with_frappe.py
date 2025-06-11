import click

import nts


def execute():
	nts_v = nts.get_attr("nts" + ".__version__")
	hrms_v = nts.get_attr("hrms" + ".__version__")

	WIKI_URL = "https://github.com/nts/hrms/wiki/Changes-to-branching-and-versioning"

	if nts_v.startswith("14") and hrms_v.startswith("15"):
		message = f"""
			The `develop` branch of nts HR is no longer compatible with nts & prodman's `version-14`.
			Since you are using prodman/nts `version-14` please switch nts HR's branch to `version-14` and then proceed with the update.\n\t
			You can switch the branch by following the steps mentioned here: {WIKI_URL}
		"""
		click.secho(message, fg="red")

		nts.throw(message)  # nosemgrep
