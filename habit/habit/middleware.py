"""
Setting up urls for dev version
example.com/dev/... --> example.com/....
"""

class RemoveScriptPrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        script_name = ''
        if request.path.startswith('/dev/'):
            script_name = '/dev'
        elif request.path.startswith('/test/'):
            script_name = '/test'

        if script_name:
            request.path_info = request.path_info[len(script_name):]
            request.path = request.path[len(script_name):]

        response = self.get_response(request)
        return response
