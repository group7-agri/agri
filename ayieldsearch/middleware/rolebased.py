from django.shortcuts import redirect



class RoleBasedMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_staff:
            return redirect('/admin/')
        return response