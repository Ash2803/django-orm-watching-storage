from django.shortcuts import get_object_or_404
from django.shortcuts import render

from datacenter.models import Passcard, get_duration, is_visit_long, format_duration
from datacenter.models import Visit


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard.objects, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        passcard_visits = {
            'entered_at': visit.entered_at,
            'duration': format_duration(get_duration(visit)),
            'is_strange': is_visit_long(visit)
        }
        this_passcard_visits.append(passcard_visits)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
