from django.shortcuts import render
from django.conf import settings

class FriendlyExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
        This catches code crashes (500 errors) before Django can 
        render the default server error page.
        """
        # Only show the cute error page if DEBUG is False (Production mode)
        if not settings.DEBUG:
            return render(request, 'errors/500.html', status=500)
        
        # If DEBUG is True, return None so you can still see the 
        # traceback locally to fix your bugs.
        return None