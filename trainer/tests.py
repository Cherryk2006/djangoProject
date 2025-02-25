import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

from booking.models import Booking
from trainer.models import Category, Service, Trainer_schedule
from trainer.utils import booking_time_discovery


# Create your tests here.
class TrainerTests(TestCase):
    def setUp(self):
        client_group = Group.objects.create(name='Client')
        trainer_group = Group.objects.create(name='Trainer')

        user = User.objects.create_user(
            "test_user", "test@gmail.com", "test_password",
            first_name="test_first_name", last_name="test_last_name"
        )
        user.groups.add(client_group)
        user.save()

        trainer = User.objects.create_user(
            "test_trainer", "trainer@gmail.com", "test_password",
            first_name="trainer_first_name", last_name="trainer_last_name"
        )
        trainer.groups.add(trainer_group)
        trainer.save()

        Category.objects.create(name="Category")

    def test_add_service(self):
        client = Client()

        category_name = Category.objects.first().name
        data = {
            "category": category_name,
            "price": "10",
            "level": "1",
            "duration": "30"
        }

        response = client.post("/trainer/services/", data)

        self.assertEqual(response.status_code, 403)

        client.login(username='test_user', password='test_password')
        response = client.post("/trainer/services/", data)

        self.assertEqual(response.status_code, 403)

        client.login(username='test_trainer', password='test_password')
        response = client.post("/trainer/services/", data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Service.objects.all().count(), 1)

    def test_add_schedule(self):
        client = Client()

        day = "2025-05-22"
        start_at = "08:00"
        end_at = "17:00"

        data = {
            "day": day,
            "start_at": start_at,
            "end_at": end_at,
        }

        response = client.post("/trainer/schedule/", data)

        self.assertEqual(response.status_code, 403)

        client.login(username='test_user', password='test_password')
        response = client.post("/trainer/schedule/", data)

        self.assertEqual(response.status_code, 403)

        client.login(username='test_trainer', password='test_password')
        response = client.post("/trainer/schedule/", data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Trainer_schedule.objects.all().count(), 1)

        response = client.post("/trainer/schedule/", {
            "day": day,
            "start_at": end_at,
            "end_at": start_at,
        })

        self.assertEqual(response.status_code, 400)

        response = client.post("/trainer/schedule/", {
            "day": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "start_at": start_at,
            "end_at": end_at,
        })

        self.assertEqual(response.status_code, 400)

    def test_booking_service(self):
        client = Client()
        client.login(username="test_trainer", password="test_password")

        category_name = Category.objects.first().name
        client.post("/trainer/services/", {
            "category": category_name,
            "price": "10",
            "level": "1",
            "duration": "30"
        })
        client.post("/trainer/schedule/", {
            "day": "2025-05-22",
            "start_at": "08:00",
            "end_at": "17:00",
        })

        client.logout()

        trainer = User.objects.get(username='test_trainer')
        schedule = Trainer_schedule.objects.filter(trainer_id=trainer.id).first()
        service = Service.objects.filter(trainer_id=trainer.id).first()
        bookings = Booking.objects.filter(trainer_id=trainer.id).all()

        day = "2025-05-22"
        time = booking_time_discovery(
            schedule.datetime_start, schedule.datetime_end,
            [[_.datetime_start, _.datetime_end] for _ in bookings],
            service.duration
        )[0].strftime("%H:%M")

        data = {
            "date": day,
            "time": time,
        }

        response = client.post(f"/trainer/{trainer.id}/{service.id}/booking", data)
        self.assertEqual(response.status_code, 403)

        client.login(username='test_trainer', password='test_password')

        response = client.post(f"/trainer/{trainer.id}/{service.id}/booking", data)
        self.assertEqual(response.status_code, 403)

        client.login(username='test_user', password='test_password')

        response = client.post(f"/trainer/{trainer.id}/{service.id}/booking", data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.all().count(), 1)