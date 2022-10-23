from datacenter.models import Passcard, get_duration, get_visitor_name
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.all().filter(leaved_at=None)
    for visit in visits:
        visit_stats = {
            'who_entered': get_visitor_name(visit),
            'entered_at': visit.entered_at,
            'duration': get_duration(visit),
        }
        non_closed_visits.append(visit_stats)
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
