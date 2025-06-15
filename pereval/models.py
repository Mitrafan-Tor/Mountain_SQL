from django.db import models
from django.core.validators import EmailValidator


class User(models.Model):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    fam = models.CharField(max_length=150, verbose_name='Фамилия')
    name = models.CharField(max_length=150, verbose_name='Имя')
    otc = models.CharField(max_length=150, verbose_name='Отчество', blank=True, default='')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.fam} {self.name} {self.otc} ({self.email})"


class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return f"Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}"


class Level(models.Model):
    winter = models.CharField(max_length=10, blank=True, null=True, verbose_name='Зима')
    summer = models.CharField(max_length=10, blank=True, null=True, verbose_name='Лето')
    autumn = models.CharField(max_length=10, blank=True, null=True, verbose_name='Осень')
    spring = models.CharField(max_length=10, blank=True, null=True, verbose_name='Весна')

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'

    def __str__(self):
        return f"Зима: {self.winter}, Лето: {self.summer}, Осень: {self.autumn}, Весна: {self.spring}"


class Image(models.Model):
    data = models.ImageField(upload_to='pereval_images/', verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Название')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.title


class PerevalAdded(models.Model):
    STATUS_CHOICES = [
        ('new', 'новый'),
        ('pending', 'в работе'),
        ('accepted', 'принят'),
        ('rejected', 'отклонен'),
    ]

    beauty_title = models.CharField(max_length=255, verbose_name='Красивое название')
    title = models.CharField(max_length=255, verbose_name='Название')
    other_titles = models.CharField(max_length=255, blank=True, null=True, verbose_name='Другие названия')
    connect = models.TextField(blank=True, null=True, verbose_name='Что соединяет')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pereval', verbose_name='Пользователь')
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE, verbose_name='Координаты')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='Уровень сложности')
    images = models.ManyToManyField(Image, through='PerevalImage', verbose_name='Изображения')

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    def __str__(self):
        return self.title


class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изображение перевала'
        verbose_name_plural = 'Изображения перевалов'