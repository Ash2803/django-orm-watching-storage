from datetime import datetime

import django
from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    current_time = django.utils.timezone.localtime(visit.leaved_at).replace(microsecond=0)
    entered_time = django.utils.timezone.localtime(visit.entered_at).replace(microsecond=0)
    time_in_storage = current_time - entered_time
    return time_in_storage


def get_visitor_name(visitor):
    return visitor.passcard


def is_visit_long(visit, minutes=60):
    suspicious_time = get_duration(visit).total_seconds() // 60
    return suspicious_time > minutes


def format_duration(duration):
    duration_to_str = str(duration)
    duration_to_datetime = datetime.strptime(duration_to_str, '%H:%M:%S')
    duration_back_to_str = datetime.strftime(duration_to_datetime, '%H:%M')
    return duration_back_to_str
