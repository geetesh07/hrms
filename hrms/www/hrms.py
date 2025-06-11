import nts
from nts.boot import load_translations

no_cache = 1


def get_context(context):
	csrf_token = nts.sessions.get_csrf_token()
	nts.db.commit()  # nosempgrep
	context = nts._dict()
	context.csrf_token = csrf_token
	context.boot = get_boot()
	return context


@nts.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
	if not nts.conf.developer_mode:
		nts.throw(nts._("This method is only meant for developer mode"))
	return get_boot()


def get_boot():
	bootinfo = nts._dict(
		{
			"site_name": nts.local.site,
			"push_relay_server_url": nts.conf.get("push_relay_server_url") or "",
			"default_route": get_default_route(),
		}
	)

	bootinfo.lang = nts.local.lang
	load_translations(bootinfo)

	return bootinfo


def get_default_route():
	return "/hrms"
