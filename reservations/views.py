from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from .forms import ReservationForm, RegisterationForm
from .models import Rooms, TheReservation

from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated









def home_page(request):
    rooms = Rooms.objects.all()
    reminder = None
    reservations = []

    if request.user.is_authenticated:
        now = timezone.now()
        reminder = TheReservation.objects.filter(
            user=request.user,
            start_time__gte=now,
            start_time__lt=now + timedelta(hours=24)
        ).order_by('start_time').first()

        reservations = TheReservation.objects.filter(
            user=request.user
        ).order_by('start_time')

    return render(request, 'home.html', {
        'rooms': rooms,
        'reminder': reminder,
        'reservations': reservations
    })


def registering(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            try:
                user.save()
                login(request, user)
                messages.success(request, 'Account created successfully! 🎉')
                return redirect('room_list')
            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = RegisterationForm()
    return render(request, 'reservations/register.html', {'form': form})


def room_lists(request):
    rooms = Rooms.objects.all()
    return render(request, 'reservations/room_list.html', {'rooms': rooms})


def room_detail(request, pk):
    room = get_object_or_404(Rooms, pk=pk)
    upcoming = TheReservation.objects.filter(
        room=room,
        end_time__gte=timezone.now()
    ).order_by('start_time')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.path)

        form = ReservationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.room = room
            try:
                res.clean()
                res.save()

                # ✅ Send confirmation email
                context = {'reservation': res}
                subject = 'Your Room Reservation is Confirmed'
                text_body = render_to_string('emails/confirmation_email.txt', context)
                html_body = render_to_string('emails/confirmation_email.html', context)

                send_mail(
                    subject,
                    text_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [res.user.email],
                    html_message=html_body,
                    fail_silently=False,
                )

                messages.success(request, 'Reservation confirmed (email sent).')
                return redirect('my_reservations')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = ReservationForm()

    return render(request, 'reservations/room_detail.html', {
        'room': room,
        'form': form,
        'upcoming': upcoming,
    })


@login_required
def my_reservations(request):
    reservations = TheReservation.objects.filter(user=request.user).order_by('start_time')
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})


@login_required
def reservation_editing(request, pk):
    res = get_object_or_404(TheReservation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=res)
        if form.is_valid():
            updated = form.save(commit=False)
            try:
                updated.clean()
                updated.save()
                messages.success(request, 'Reservation updated.')
                return redirect('my_reservations')
            except Exception as e:
                messages.error(request, str(e))
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = ReservationForm(instance=res)

    return render(request, 'reservations/reservations_edit.html', {
        'reservation': res,
        'form': form,
    })


@login_required
def reservations_cancelling(request, pk):
    res = get_object_or_404(TheReservation, pk=pk, user=request.user)
    if request.method == 'POST':
        res.delete()
        messages.success(request, 'Reservation cancelled.')
        return redirect('my_reservations')
    return render(request, 'reservations/reservations_cancel.html', {'reservation': res})


def room_status(request):
    slot_s = request.GET.get('slot_start')
    slot_e = request.GET.get('slot_end')
    try:
        start = datetime.fromisoformat(slot_s) if slot_s else timezone.now()
    except (TypeError, ValueError):
        start = timezone.now()
    end = datetime.fromisoformat(slot_e) if slot_e else start + timedelta(hours=1)

    status_list = []
    for room in Rooms.objects.all():
        occupied = TheReservation.objects.filter(
            room=room,
            start_time__lt=end,
            end_time__gt=start
        ).exists()
        next_res = TheReservation.objects.filter(
            room=room,
            start_time__gte=end
        ).order_by('start_time').first()
        status_list.append({
            'room': room,
            'occupied': occupied,
            'next_res': next_res,
        })

    return render(request, 'reservations/room_status.html', {
        'status_list': status_list,
        'slot_start': start,
        'slot_end': end,
    })


def test_email(request):
    send_mail(
        subject="Test Email",
        message="This is a test email from Django using SendGrid.",
        from_email="mannatsareen1998@gmail.com",  # must match verified sender
        recipient_list=["mannatsareen1998@gmail.com"],
        fail_silently=False,
    )
    return HttpResponse("Test email sent.")



class RoomViewSet(viewsets.ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TheReservation.objects.filter(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]