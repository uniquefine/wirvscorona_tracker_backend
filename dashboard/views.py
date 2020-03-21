from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render


def first_dashboard(request):
    # get data from firebase
    data = {}

    # Plot functions that should be displayed in this dashboard
    plot_functions = []

    plot_list = []
    for function in plot_functions:
        try:
            plot_list.append(plot_functions(data))
        except Exception as e:
            plot_list.append(f"<p>error in plotting: {e}<\p>")

    context = {'plot_list':plot_list}

    return render(request, 'dashboard/first_dashboard.html', context)

