from werkzeug.local import Local, LocalManager


local = Local()
local_manager = LocalManager([local])


def url_for(endpoint: str, _external: bool = False, **values) -> str:
    return local.url_adapter.build(endpoint, values, force_external=_external)
