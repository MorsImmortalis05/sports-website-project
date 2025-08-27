class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        print(f"Request: {request.method} {request.path}")
        if request.user.is_authenticated:
            print(f"User: {request.user.username}")
        response = self.get_response(request)
        print(f"Response: {response.status_code}")
        return response
