from django.shortcuts import render
from django.views import generic
from .models import Court, Booking, ScheduleException
from django.utils import timezone
from django.utils.timezone import timedelta
from datetime import datetime, date
from django.utils import timezone

from .utils import next_week, previous_week, schedule_str_format, session_current_week


class CourtsListView(generic.ListView):
    template_name = 'quadras/court_list.html'
    model = Court
    context_object_name = 'courts'


class CourtScheduleDetailView(generic.DetailView):
    template_name = 'quadras/court_detail.html'
    model = Court
    context_object_name = 'courts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        action = self.request.GET.get('action')
        session = self.request.session

        court = self.get_object()
        this_court_start_time = court.schedule.opening_time.hour
        this_court_end_time = court.schedule.closing_time.hour

        this_monday = timezone.now().date() - timedelta(days=timezone.now().weekday()) #DATE FORMAT VALUE

        if not session.get('current_monday_session'):
            session['current_monday_session'] = this_monday.isoformat() # JSON em forma de STR (django nao reconhece datetime.date())
            current_week = date.fromisoformat(session['current_monday_session'])
        else:
            current_week = date.fromisoformat(session['current_monday_session'])

        if action == 'next':
            session['current_monday_session'] = next_week(current_week).isoformat()
        elif action == 'previous':
            session['current_monday_session'] = previous_week(current_week).isoformat()

        schedules = schedule_str_format(time_start=this_court_start_time, time_end=this_court_end_time)
        court_week_days = session_current_week(current_week)
        
        slots = []

        for day in court_week_days:
            for hour in schedules:
                _date = timezone.make_aware(datetime.combine((day), hour))
                if Booking.objects.filter(court=court, start_time__lte=_date, end_time__gt=_date).exists():
                    status = "reservado"
                elif ScheduleException.objects.filter(courts=court, start_time__lte=_date, end_time__gt=_date).exists():
                    status = "manutencao"
                else:
                    status = "disponivel"
                
                slots.append(
                    {"datetime": _date, "status": status, "weekday": _date.weekday()}
                )

        context['horarios'] = schedules
        context['today'] = court_week_days
        context['slots'] = slots
        return context



        