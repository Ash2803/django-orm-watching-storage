from django.shortcuts import render

from datacenter.models import Visit, format_duration
from datacenter.models import get_duration, get_visitor_name


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.all().filter(leaved_at__isnull=True)
    for visit in visits:
        visit_stats = {
            'who_entered': get_visitor_name(visit),
            'entered_at': visit.entered_at,
            'duration': format_duration(get_duration(visit)),
        }
        non_closed_visits.append(visit_stats)
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
