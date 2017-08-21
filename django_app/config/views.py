from django.shortcuts import redirect


def index(request):
    return redirect('group:group_list')
