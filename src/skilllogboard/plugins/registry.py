"""Plugin registry placeholder."""

_REGISTRY = {}


def register(plugin):
    _REGISTRY[plugin.name] = plugin
    return plugin


def get_plugin(name):
    return _REGISTRY[name]
