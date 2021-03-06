from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render

from dashboard.plots import dummy_function, sun_burst, symptom_dist, infected_cummulative, profile_dist
from tracker_backend.firebase import get_data


def first_dashboard(request):
    # get data from firebase
    data = get_data()

    # Plot functions that should be displayed in this dashboard
    plot_functions = [("Häufigkeit der Symptome", symptom_dist),("Struktur der Profile", profile_dist), ("Symptomzusammenhang", sun_burst), ("Kumulative Anzahl Bestätigter Fälle", infected_cummulative)]

    plot_list = []
    for name, function in plot_functions:
        try:
            plot_list.append({"title": name, "html": function(data)})
        except Exception as e:
            plot_list.append(f"<p>error in plotting: {e}<\p>")

    context = {'plot_list':plot_list}

    return render(request, 'dashboard/first_dashboard.html', context)

