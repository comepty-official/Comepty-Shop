from django.shortcuts import render

def custom_page_not_found(request, exception):
    """ Friendly 404 Error Page """
    return render(request, 'errors/404.html', status=404)

def custom_server_error(request):
    """ Friendly 500 Error Page """
    return render(request, 'errors/500.html', status=500)