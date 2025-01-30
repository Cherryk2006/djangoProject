from datetime import datetime
import booking


def booking_time_discovery(trainer, service, date):

    trainer_schedule = trainer.models.TrainerSchedule.filter(trainer=trainer, datetime_start_date=date)
    trainer_booking = booking.models.Booking.objects.filter(trainer=trainer, datetime_start_date=date)
    desired_service = trainer.models.Service.objects.get(pk=service)
    search_window = desired_service.duration
