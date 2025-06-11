import nts

__version__ = "15.47.1"


def refetch_resource(cache_key: str | list, user=None):
	nts.publish_realtime(
		"hrms:refetch_resource",
		{"cache_key": cache_key},
		user=user or nts.session.user,
		after_commit=True,
	)
