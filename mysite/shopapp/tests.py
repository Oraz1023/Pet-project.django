from random import choices
from string import ascii_letters

from mysite import settings
from .models import Product
from .utils import add_two_numbers
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ProductCreateViewTestCase(TestCase):
    """Определяет класс тестового примера с именем ProductCreateViewTestCase, который наследуется от Django TestCase."""

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
        """etUp Метод вызывается перед каждым методом тестирования. Он создает User экземпляр с именем пользователя 'testuser' и паролем 'testpassword', используя create_user метод Django. Затем он генерирует случайное название продукта длиной 10, используя choices функцию Python, и удаляет все существующие Product с таким же именем, чтобы обеспечить уникальность."""

    def test_product_create_view(self):
        """Этот метод определяет тест для проверки поведения ProductCreateView."""
        # Authenticate the user
        self.client.login(username='testuser', password='testpassword')
        print("Is user authenticated?", self.client.session.get('_auth_user_id'))
        """Проверяет подлинность тестируемого пользователя, созданного с помощью setUp метода, и выводит информацию о том, аутентифицирован ли пользователь путем проверки _auth_user_id ключа в сеансе."""

        # Make a post request to create a product
        response = self.client.post(
            reverse('shopapp:product-create'),
            {
                'name': self.product_name,
                'price': "123.66",
                'description': 'a good table',
                'discount': "10",
            },
        )
        """Отправляет запрос POST в ProductCreateView с помощью тестового клиента Django (self.client). Он включает данные для создания продукта, такие как название, цена, описание и скидка."""
        # Print response content for debugging
        print("Response content:", response.content)
        """Печатает содержимое ответа, полученного от запроса POST. Для целей отладки может быть полезно посмотреть, что возвращает представление."""

        # Check if the response redirects to the product list page
        self.assertRedirects(response, reverse("shopapp:product-list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists)
        """Проверяет, что ответ перенаправляется на страницу списка продуктов после создания продукта с помощью assertRedirects. Кроме того, он проверяет, существует ли продукт с сгенерированным названием в базе данных с помощью assertTrue."""


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")
        """Метод setUpClass - это метод класса, который вызывается один раз перед запуском любых методов тестирования в классе test case. В этом методе вы создаете объект product с именем "Лучший продукт" и присваиваете ему атрибут class cls.product"""

    @classmethod
    def tearDown(cls) -> None:
        cls.product.delete()
        """Mетод tearDown - это метод класса, который вызывается один раз после выполнения всех методов тестирования в классе test case. Он удаляет объект product, созданный в методе , гарантируя, что все изменения, внесенные во время тестирования, будут очищены.setUpClass"""

    def test_get_product(self):
        response = self.client.get('shopapp:product-detail', kwargs={"pk": self.product.pk})
        self.assertEqual(response.status_code, 200)
        """Этот метод определяет тестовый пример для проверки того, возвращает ли представление сведений о продукте код состояния 200 (OK) при обращении с использованием шаблона URL с именем 'shopapp:product-detail' и первичного ключа (pk) объекта product, созданного в setUpClass."""

    def test_get_product_and_check_content(self):
        response = self.client.get(reverse('shopapp:product-detail', kwargs={"pk": self.product.pk}))
        self.assertContains(response, self.product.name)
        """Этот метод определяет тестовый пример для проверки, содержит ли представление сведений о продукте название объекта product, созданного в setUpClass. Он использует  для получения шаблона URL с именем reverse и передает первичный ключ продукта в качестве ключевого аргумента. Затем он утверждает, что ответ содержит название продукта.'shopapp:product-detail'"""


class ProductListViewTestCase(TestCase):
    fixtures = ['products-fixture.json', ]
    """Указывает файл (ы) прибора для загрузки перед запуском тестов. Он загружает products-fixture.json прибор, который содержит исходные данные для тестирования."""

    def test_products(self):
        response = self.client.get(reverse("shopapp:product-list"))
        """Отправляет запрос GET в представление списка продуктов (shopapp:product-list) с помощью тестового клиента Django (self.client). Он извлекает ответ, возвращенный представлением."""
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(product.pk for product in response.context["products"]),
            transform=lambda product: product.pk,
        )


"""Сравнивает набор запросов активных продуктов Product.objects.filter(archived=False).all()) с первичными ключами (pk) продуктов в контексте ответа (response.context["products"]).
В аргументе value указываются ожидаемые значения (первичные ключи продукта) для сравнения с набором запросов.
transform Аргумент - это функция, которая преобразует каждый элемент в наборе запросов в формат, который можно сравнить с ожидаемыми значениями. Здесь он преобразует каждый продукт в его первичный ключ (product.pk)."""


# class OrdersListViewTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.credentials = dict(username="Ораз", password="qwerty")
#         cls.user = User.objects.create_user(**cls.credentials)
#         """setUpClass это метод класса, который вызывается один раз в начале тестового примера. Он создает тестируемого пользователя с именем пользователя "testuser" и паролем, указанным в <PASSWORD> заполнителе с использованием User.objects.create_user."""
#     @classmethod
#     def tearDownClass(cls):
#         cls.user.delete()
#         """tearDownClass это метод класса, который вызывается один раз в конце тестового примера. Он удаляет тестируемого пользователя, созданного в setUpClass для очистки после теста."""
#
#     def setUp(self)->None:
#         self.client.login(**self.credentials)
#         """Метод setUp вызывается перед каждым методом тестирования. Он входит в систему тестируемого пользователя, используя предоставленные учетные данные (self.credentials) с помощью self.client.login."""
#
#     def test_orders_view(self):
#         response = self.client.get(reverse('shopapp:order_list'))
#         """Отправляет запрос GET в представление заказов (shopapp:order_list) с помощью тестового клиента Django (self.client). Он извлекает ответ, возвращенный представлением."""
#         self.assertContains(response,"Orders")
#         """Используется assertContains для проверки наличия строки "Orders" в содержимом ответа. Это гарантирует, что представление orders содержит текст "Orders", указывающий на правильность отображения представления."""


class OrdersListViewTestCase(TestCase):
    """Определяет класс тестового примера с именем OrdersListViewTestCase, который наследуется от Django TestCase"""

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="Bob", password="qwerty")
        """setUpClass это метод класса, который вызывается один раз в начале тестового примера. Он создает тестируемого пользователя с именем пользователя "Bob" и паролем "qwerty", используя User.objects.create_user."""

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        """tearDownClass это метод класса, который вызывается один раз в конце тестового примера. Он удаляет тестируемого пользователя, созданного в setUpClass для очистки после теста."""

    def setUp(self) -> None:
        self.client.force_login(self.user)
        """Метод setUp вызывается перед каждым методом тестирования. Он регистрирует тестируемого пользователя с помощью self.client.force_login(self.user). Это гарантирует, что пользователь проходит аутентификацию перед каждым тестом."""

    def test_orders_view(self):
        """Этот метод определяет тест для проверки правильности отображения в представлении заказов (shopapp:order_list)."""
        response = self.client.get(reverse('shopapp:order_list'))
        """Отправляет запрос GET в представление заказов (shopapp:order_list) с помощью тестового клиента Django (self.client). Он извлекает ответ, возвращенный представлением."""
        self.assertContains(response, "Orders")
        """Используется assertContains для проверки наличия строки "Orders" в содержимом ответа. Это гарантирует, что представление orders содержит текст "Orders", указывающий на правильность отображения представления."""

    def test_orders_view_authenticated(self):
        """Этот метод определяет тест для проверки того, перенаправляется ли просмотр заказов на страницу входа при доступе пользователя, не прошедшего проверку подлинности."""
        self.client.logout()
        """Тестовый клиент выходит из системы, чтобы имитировать доступ пользователя, не прошедшего проверку подлинности, к просмотру заказов."""
        response = self.client.get(reverse("shopapp:order_list"))
        """Отправляет запрос GET в представление заказов (shopapp:order_list) от имени пользователя, не прошедшего проверку подлинности, с помощью тестового клиента Django. Он извлекает ответ, возвращенный представлением."""
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)
        """Утверждает, что код состояния ответа равен 302 (перенаправление) и что URL-адрес ответа содержит URL-адрес входа, указанный в настройках Django (settings.LOGIN_URL). Это гарантирует, что просмотр заказов перенаправляется на страницу входа для пользователей, не прошедших проверку подлинности."""


class ProductsExportViewTestCase(TestCase):
    fixtures = ['products-fixture.json']

    def test_get_products_export(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


"""
Assert-утверждения (assertions) в тестах Django используются для проверки ожидаемых результатов. Если утверждение не выполняется (т.е. результат не соответствует ожиданиям), то тест считается неудачным. Вот краткое объяснение каждого assert-утверждения в вашем тесте:

assertEqual: Проверяет, что два значения равны.
self.assertEqual(фактическое_значение, ожидаемое_значение)

assertNotEqual: Проверяет, что два значения не равны.
self.assertNotEqual(фактическое_значение, ожидаемое_значение)

assertTrue: Проверяет, что утверждение истинно.
self.assertTrue(условие)

assertFalse: Проверяет, что утверждение ложно.
self.assertFalse(условие)

assertIs: Проверяет, что два объекта являются одним и тем же объектом (имеют одинаковые идентификаторы)
self.assertIs(фактический_объект, ожидаемый_объект)

assertIsNot: Проверяет, что два объекта не являются одним и тем же объектом (имеют разные идентификаторы).
self.assertIsNot(фактический_объект, ожидаемый_объект)

assertRaises: Проверяет, что определенное исключение было 
возбуждено при выполнении кода
self.assertRaises(Исключение, функция_или_выражение)

assertRedirects: Проверяет, что ответ перенаправляется на указанный URL
self.assertRedirects(ответ, ожидаемый_URL)

assertIn: Проверяет, что элемент присутствует в контейнере (списке, кортеже, множестве или словаре)
self.assertIn(элемент, контейнер)

assertNotIn: Проверяет, что элемент отсутствует в контейнере (списке, кортеже, множестве или словаре).
self.assertNotIn(элемент, контейнер)

assertRaisesMessage: Проверяет, что определенное исключение с определенным сообщением было возбуждено при выполнении кода.
self.assertRaisesMessage(Исключение, ожидаемое_сообщение, функция_или_выражение)

Эти утверждения используются для проверки различных аспектов вашего кода в тестах Django, чтобы убедиться, что он работает должным образом и соответствует вашим ожиданиям."""
