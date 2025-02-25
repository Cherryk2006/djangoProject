import datetime
from datetime import timedelta

CANCEL_STATUS = "Canceled"
ACCEPT_STATUS = "Accepted"
PROCESSING_STATUS = "Processing"

def booking_time_discovery(schedule_start, schedule_end, trainer_bookings, search_window):

    start_time = schedule_start
    end_time = schedule_end

    all_time_slots = []
    current_time = start_time
    while current_time + timedelta(minutes=search_window) <= end_time:
        all_time_slots.append(current_time)
        current_time += timedelta(minutes=30)

    for booking in trainer_bookings :
        booking_start = booking[0]
        booking_end = booking[1]
        all_time_slots = [slot for slot in all_time_slots if not (booking_start <= slot < booking_end)]

    return all_time_slots


if __name__ == '__main__':
    trainer_id = 1
    service_id = 1
    date = datetime.date(2024, 12, 25)

    available_slots = booking_time_discovery(trainer_id, service_id, date)
    print("Available slots for booking:")
    for slot in available_slots:
        print(slot.strf("%Y-%m-%d %H:%M"))
