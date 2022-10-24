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
    if not visit.leaved_at:
        current_time = django.utils.timezone.localtime().replace(microsecond=0, second=0)
        entered_time = visit.entered_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        time_in_storage = str(current_time - entered_time)
        return time_in_storage[:-3]
    else:
        entered_time = visit.entered_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        leave_time = visit.leaved_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        total_time = str(leave_time - entered_time)
        return total_time[:-3]


def get_visitor_name(visitor):
    return visitor.passcard


def is_visit_long(visit, minutes=60):
    if visit.leaved_at:
        entered_time = visit.entered_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        leave_time = visit.leaved_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        suspicious_time = (leave_time - entered_time).total_seconds() // 60
        return suspicious_time > minutes
