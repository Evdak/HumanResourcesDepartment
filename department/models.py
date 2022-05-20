import datetime
from statistics import mode
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
import re


User = get_user_model()


def validate_sninls(value):
    value = str(value)
    if not re.fullmatch(r"^\d{3}-\d{3}-\d{3} \d{2}$", value):
        raise ValidationError(
            _('%(value)s неверно указан'),
            params={'value': value},
        )


def validate_phone(value):
    value = str(value)
    if not re.fullmatch(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", value):
        raise ValidationError(
            _('%(value)s неверно указан'),
            params={'value': value},
        )


def validate_code(value):
    if not re.fullmatch(r"^\d{3}-\d{3}$", value):
        raise ValidationError(
            _('%(value)s неверно указан'),
            params={'value': value},
        )


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Логин работника"
    )
    firstName = models.CharField("Имя", max_length=50)
    middleName = models.CharField("Фамилия", max_length=50)
    lastName = models.CharField("Отчество", max_length=50)

    def __str__(self) -> str:
        return f"{self.user} {self.firstName} {self.middleName} {self.lastName}"

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"


class FamilyComposition(models.Model):
    firstName = models.CharField("Имя", max_length=50)
    middleName = models.CharField("Фамилия", max_length=50)
    lastName = models.CharField("Отчество", max_length=50)
    degreeOfKinship = models.CharField(
        "Степень родства",
        max_length=50,
        choices=(
            ('Жена', 'Жена'),
            ('Муж', 'Муж'),
            ('Сын', 'Сын'),
            ('Дочь', 'Дочь'),
        )
    )

    def __str__(self) -> str:
        return f"{self.firstName} {self.middleName} {self.lastName} {self.degreeOfKinship}"

    class Meta:
        verbose_name = 'Член семьи'
        verbose_name_plural = 'Члены семьи'


class EmpFamily(models.Model):
    marStatus = models.CharField(
        "Семейное положение",
        max_length=50,
        choices=(
            ('не замужем / не женат', 'не замужем / не женат'),
            ('замужем / женат', 'замужем / женат'),
            ('разведен / разведена', 'разведен / разведена'),
            ('вдовец / вдова', 'вдовец / вдова'),
        )
    )
    maidenName = models.CharField(
        "Девичья фамилия",
        max_length=50,
        null=True,
        blank=True
    )
    familyComposition = models.ManyToManyField(
        FamilyComposition,
        verbose_name='Состав семьи'
    )

    def __str__(self) -> str:
        return f"{self.familyComposition}"

    class Meta:
        verbose_name = 'Семья'
        verbose_name_plural = 'Семьи'


class Passport(models.Model):
    series = models.PositiveIntegerField(
        'Серия',
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(9999)
        ]
    )
    number = models.PositiveIntegerField(
        'Номер',
        validators=[
            MinValueValidator(100000),
            MaxValueValidator(999999)
        ]
    )

    code = models.CharField(
        'Код подразделения',
        max_length=7,
        validators=[
            MinLengthValidator(7),
            MaxLengthValidator(7),
            validate_code
        ]
    )

    place = models.CharField(
        'Кем выдан',
        max_length=250,
    )

    # добавить проверку, что не будущее время
    date = models.DateField('Дата выдачи')

    bornPlace = models.CharField(
        'Место рождения',
        max_length=250,
    )

    living_place = models.CharField(
        'Место прописки',
        max_length=250
    )

    def __str__(self) -> str:
        return f"{self.series} {self.number}"

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'


class Contract(models.Model):
    payment = models.FloatField(
        'Зарплата',
        validators=[
            MinValueValidator(0)
        ]
    )
    type = models.CharField(
        max_length=20,
        choices=(
            ('Срочный', 'Срочный'),
            ('Бессрочный', 'Бессрочный')
        )
    )
    start_date = models.DateField(
        'Дата начала действия договора'
    )
    end_date = models.DateField(
        'Дата начала действия договора',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.type == 'Бессрочный':
            self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"ID: {self.id}"

    class Meta:
        verbose_name = 'Трудовой договор'
        verbose_name_plural = 'Трудовые договора'


class EmpBook(models.Model):
    give_date = models.DateField(
        'Дата выдачи'
    )

    position = models.CharField(
        'Должность',
        max_length=150
    )

    work_start_date: datetime.date = models.DateField(
        'Дата принятия на работу'
    )

    work_end_date: datetime.date = models.DateField(
        'Дата увольнения или выхода на пенсию',
        null=True,
        blank=True
    )

    work_experience = models.PositiveIntegerField(
        'Стаж работы', editable=False, default=0
    )

    def save(self, *args, **kwargs):

        if self.work_end_date:
            if self.work_end_date < self.work_start_date:
                raise ValidationError(
                    "Дата увольнения меньше, чем дата принятия на работу")
            self.work_experience = (
                self.work_end_date - self.work_start_date).days // 365
        else:
            self.work_experience = (datetime.datetime.now(
            ).date() - self.work_start_date).days // 365
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"ID: {self.id}"

    class Meta:
        verbose_name = 'Трудовая книжка'
        verbose_name_plural = 'Трудовые книжки'


class Education(models.Model):
    nameIns = models.CharField(
        'Наименование образовательного учреждения',
        max_length=100
    )
    nameDoc = models.CharField(
        'Наименование документа об образовании',
        max_length=100
    )
    series = models.PositiveBigIntegerField(
        'Серия'
    )
    number = models.PositiveBigIntegerField(
        'Номер'
    )
    speciality = models.CharField(
        'Направление или специальность',
        max_length=100
    )
    qalification = models.CharField(
        'Квалификация',
        max_length=100,
        choices=(
            ('Нет', 'Нет'),
            ('Дошкольное образование', 'Дошкольное образование'),
            ('Начальное общее образование', 'Начальное общее образование'),
            ('Основное общее образование', 'Основное общее образование'),
            ('Среднее общее образование', 'Среднее общее образование'),
            ('Среднее профессиональное образование',
             'Среднее профессиональное образование'),
            ('Высшее образование — бакалавриат',
             'Высшее образование — бакалавриат'),
            ('Высшее образование — специалитет, магистратура',
             'Высшее образование — специалитет, магистратура'),
            ('Высшее образование — подготовка кадров высшей квалификации',
             'Высшее образование — подготовка кадров высшей квалификации'),
            ('Дополнительное образование детей и взрослых',
             'Дополнительное образование детей и взрослых'),
            ('Дополнительное профессиональное образование',
             'Дополнительное профессиональное образование'),
            ('Профессиональное обучение', 'Профессиональное обучение'),
            ('Другое', 'Другое'),
        )
    )
    graduationYear = models.PositiveIntegerField(
        'Год окончания',
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(datetime.datetime.now().year)
        ]
    )

    def __str__(self) -> str:
        return f"{self.series} {self.number}"

    class Meta:
        verbose_name = "Документ об образовании"
        verbose_name_plural = "Документы об образовании"


class PersonalFile(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="Логин работника"
    )
    ITN = models.PositiveBigIntegerField(
        "ИНН",
        validators=[
            MinValueValidator(10000000000),
            MaxValueValidator(999999999999)
        ]
    )
    insPolicy = models.PositiveBigIntegerField(
        "Номер мед. полиса",
        validators=[
            MinValueValidator(10000000000000000),
            MaxValueValidator(999999999999999999)
        ]
    )
    snils = models.CharField(
        "СНИЛС",
        max_length=14,
        validators=[
            MinLengthValidator(14),
            MaxLengthValidator(14),
            validate_sninls
        ]
    )
    phoneNum = models.CharField(
        "Номер телефона",
        max_length=12,
        validators=[
            validate_phone,
            MinLengthValidator(11),
            MaxLengthValidator(12)
        ]
    )

    # добавить проверку, что не будущее время
    bornDate = models.DateField('Дата рождения')

    sex = models.CharField(
        'Пол',
        max_length=1,
        choices=(
            ('М', 'М'),
            ('Ж', 'Ж')
        )
    )

    fact_living_place = models.CharField(
        'Фактическое место проживания',
        max_length=250
    )

    family = models.OneToOneField(
        EmpFamily,
        on_delete=models.CASCADE,
        verbose_name='Семья',
        null=True,
        blank=True
    )

    passport = models.OneToOneField(
        Passport,
        on_delete=models.CASCADE,
        verbose_name='Паспорт'
    )

    education = models.ManyToManyField(
        Education,
        verbose_name='Образование'
    )

    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        verbose_name='Трудовой договор'
    )

    empBook = models.OneToOneField(
        EmpBook,
        on_delete=models.CASCADE,
        verbose_name='Трудовая книжка'
    )

    class Meta:
        verbose_name = "Личное дело"
        verbose_name_plural = "Личные дела"
