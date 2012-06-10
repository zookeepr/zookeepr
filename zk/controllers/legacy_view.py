from zkpylons.config.middleware import make_app

class LegacyView(object):
    def __init__(self, global_config, **settings):
        self.app = make_app(global_config, True, True, **settings)
    def __call__(self, request):
        return request.get_response(self.app)

