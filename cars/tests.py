import tempfile
from django.test import TestCase
from django.urls import reverse
from .models import Car


class CarModelTestCase(TestCase):
    def test_create(self):
        Car.objects.create(
            make="Honda",
            model="Accord",
            year=2017,
            )


class CarListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        car_1 = Car.objects.create(
            make="Honda",
            model="Accord",
            year=2017,
            )
        car_2 = Car.objects.create(
            make="Honda",
            model="Civic",
            year=2018,
            )
        car_3 = Car.objects.create(
            make="BMW",
            model="535",
            year=2015,
            )

    def test_url(self):
        url = reverse("car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        url = reverse("car-list")
        response = self.client.get(url)
        self.assertTemplateUsed("car_list.html")
        self.assertTemplateUsed("base.html")

    def test_template_displayed(self):
        url = reverse("car-list")
        response = self.client.get(url)
        cars = Car.objects.all()
        for car in cars:
            self.assertContains(response, car.make)

    def test_image_displayed(self):
        Car.objects.create(
            make="BMW",
            model="535",
            year=2015,
            img=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        url = reverse("car-list")
        response = self.client.get(url)
        cars = Car.objects.all()
        for car in cars:
            if car.img:
                self.assertContains(response, car.img.url)

    def test_details_url(self):
        url = reverse("car-list")
        response = self.client.get(url)
        cars = Car.objects.all()
        for car in cars:
            self.assertContains(response, reverse("car-detail", kwargs={"car_id":car.id}))

    def test_navbar(self):
        url = reverse("car-list")
        response = self.client.get(url)
        self.assertContains(response, reverse("car-create"))


class CarDetailsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.car_id = 2
        car_1 = Car.objects.create(
            make="Honda2",
            model="Accord",
            year=2017,
            )
        car_2 = Car.objects.create(
            make="Honda",
            model="Civic",
            year=2018,
            )
        car_3 = Car.objects.create(
            make="BMW",
            model="535",
            year=2015,
            )

    def test_url(self):
        url = reverse("car-detail", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        url = reverse("car-detail", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertTemplateUsed("car_detail.html")
        self.assertTemplateUsed("base.html")

    def test_template_displayed(self):
        url = reverse("car-detail", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        cars = Car.objects.all()
        for car in cars:
            if car.id == self.car_id:
                self.assertContains(response, car.make)
                self.assertContains(response, car.model)
                self.assertContains(response, car.year)
            else:
                self.assertNotContains(response, car.make)
                self.assertNotContains(response, car.model)
                self.assertNotContains(response, car.year)

    def test_image_displayed(self):
        car = Car.objects.create(
            make="BMW",
            model="535",
            year=2015,
            img=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        url = reverse("car-detail", kwargs={"car_id":car.id})
        response = self.client.get(url)
        self.assertContains(response, car.img.url)

    def test_update_delete_url(self):
        url = reverse("car-detail", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        car = Car.objects.get(id=self.car_id)
        self.assertContains(response, reverse("car-update", kwargs={"car_id":car.id}))
        self.assertContains(response, reverse("car-delete", kwargs={"car_id":car.id}))

    def test_navbar(self):
        url = reverse("car-detail", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertContains(response, reverse("car-create"))


class CarCreateTestCase(TestCase):
    def test_url(self):
        url = reverse("car-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        url = reverse("car-create")
        response = self.client.get(url)
        self.assertTemplateUsed("base.html")

    def test_create_valid(self):
        data = {
            "make": "Jeep",
            "model": "Wrangler",
            "year": 2018,
        }
        url = reverse("car-create")
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        cars = Car.objects.all()
        self.assertEqual(cars.count(), 1)
        self.assertEqual(cars[0].make, data["make"])
        self.assertEqual(cars[0].model, data["model"])
        self.assertEqual(cars[0].year, data["year"])

    def test_create_not_valid(self):
        data = {
            "make": "Jeep",
            "model": "Wrangler",
        }
        url = reverse("car-create")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(cars.count(), 0)
        self.assertContains(response, data["make"])
        self.assertContains(response, data["model"])

    def test_navbar(self):
        url = reverse("car-create")
        response = self.client.get(url)
        self.assertContains(response, reverse("car-create"))


class CarUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_id = 2
        car_1 = Car.objects.create(
            make="Honda2",
            model="Accord",
            year=2017,
            )
        car_2 = Car.objects.create(
            make="Honda",
            model="Civic",
            year=2018,
            )
        car_3 = Car.objects.create(
            make="BMW",
            model="535",
            year=2015,
            )

    def test_url(self):
        url = reverse("car-update", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        url = reverse("car-update", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertTemplateUsed("base.html")

    def test_template_displayed(self):
        url = reverse("car-update", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        cars = Car.objects.all()
        for car in cars:
            if car.id == self.car_id:
                self.assertContains(response, car.make)
                self.assertContains(response, car.model)
                self.assertContains(response, car.year)
            else:
                self.assertNotContains(response, car.make)
                self.assertNotContains(response, car.model)
                self.assertNotContains(response, car.year)

    def test_update_valid(self):
        car = Car.objects.get(id=self.car_id)
        data = {"model": car.model, "make": car.make, "year":2000}
        url = reverse("car-update", kwargs={"car_id":self.car_id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        new_car = Car.objects.get(id=self.car_id)
        self.assertEqual(new_car.model, car.model)
        self.assertEqual(new_car.year, data["year"])
        self.assertEqual(new_car.make, car.make)

    def test_update_invalid(self):
        car = Car.objects.get(id=self.car_id)
        data = {"model": car.model, "make": car.make}
        url = reverse("car-update", kwargs={"car_id":self.car_id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_navbar(self):
        url = reverse("car-update", kwargs={"car_id":self.car_id})
        response = self.client.post(url)
        self.assertContains(response, reverse("car-create"))


class CarDeleteTestCase(TestCase):
    def setUp(self):
        self.car_id = 2
        self.car_1 = Car.objects.create(
            make="Honda",
            model="Accord",
            year=2017,
            )
        self.car_2 = Car.objects.create(
            make="Honda",
            model="Civic",
            year=2018,
            )
        self.car_3 = Car.objects.create(
            make="BMW",
            model="535",
            year=2015,
            )

    def test_url(self):
        url = reverse("car-delete", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_works(self):
        url = reverse("car-delete", kwargs={"car_id":self.car_id})
        response = self.client.get(url)
        self.assertFalse(Car.objects.filter(id=self.car_id).exists())

