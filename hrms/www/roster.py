import nts


def get_context(context):
	csrf_token = nts.sessions.get_csrf_token()
	nts.db.commit()  # nosempgrep
	context = nts._dict()
	context.csrf_token = csrf_token
	return context
