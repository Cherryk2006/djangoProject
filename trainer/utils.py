from datetime import datetime, timedelta
import booking


def booking_time_discovery(trainer, service, date, start_time, end_time, booking, service_duration):

    trainer_schedule = trainer.models.TrainerSchedule.filter(trainer=trainer, datetime_start_date=date)
    trainer_booking = booking.models.Booking.objects.filter(trainer=trainer, datetime_start_date=date)
    desired_service = trainer.models.Service.objects.get(pk=service)
    search_window = desired_service.duration

    start_time = datetime.combine(date, trainer_schedule.start_time)
    end_time = datetime.combine(date, trainer_schedule.end_time)

    all_slots = []
    current_time = start_time

    while current_time + timedelta(minutes=service_duration) <= end_time:
        all_slots.append(current_time)
        current_time += timedelta(minutes=15)

    free_slots = all_slots[:]
    for booking in trainer_booking:
        booked_start = booking.start_time
        booked_end = booked_start + timedelta(minutes=booking.duration)

        free_slots = [
            slot for slot in free_slots
            if not (booked_start <= slot < booked_end)
        ]
    return free_slots
