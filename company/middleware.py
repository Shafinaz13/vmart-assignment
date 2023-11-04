from django.shortcuts import redirect


class CSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403 and 'CSRF verification failed' in response.content.decode('utf-8'):
            # Redirect to home.html when CSRF verification fails
            return redirect('home')
        return response
