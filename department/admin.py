from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Employee)
class FilterEmployee(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "firstName",
        "middleName",
        "lastName"
    )
    list_filter = (
        "id",
        "user",
        "firstName",
        "middleName",
        "lastName"
    )


@admin.register(Contract)
class FilterContract(admin.ModelAdmin):
    list_display = (
        "payment",
        "type",
        "start_date",
        "end_date"
    )
    list_filter = (
        "payment",
        "type",
        "start_date",
        "end_date"
    )


@ admin.register(EmpBook)
class FilterEmpBook(admin.ModelAdmin):
    list_display = (
        "give_date",
        "position",
        "work_start_date",
        "work_end_date",
        "work_experience"
    )
    list_filter = (
        "give_date",
        "position",
        "work_start_date",
        "work_end_date",
        "work_experience"
    )


@ admin.register(Education)
class FilterEducation(admin.ModelAdmin):
    list_display = (
        "nameIns",
        "nameDoc",
        "series",
        "number",
        "speciality",
        "qalification",
        "graduationYear"
    )
    list_filter = (
        "nameIns",
        "nameDoc",
        "series",
        "number",
        "speciality",
        "qalification",
        "graduationYear"
    )


@ admin.register(EmpFamily)
class FilterEmpFamily(admin.ModelAdmin):
    list_display = (
        "marStatus",
        "maidenName",
    )
    list_filter = (
        "marStatus",
        "maidenName",
    )


@ admin.register(FamilyComposition)
class FilterFamilyComposition(admin.ModelAdmin):
    list_display = (
        "id",
        "firstName",
        "middleName",
        "lastName",
        "degreeOfKinship"
    )
    list_filter = (
        "id",
        "firstName",
        "middleName",
        "lastName",
        "degreeOfKinship"
    )


@ admin.register(Passport)
class FilterPassport(admin.ModelAdmin):
    list_display = (
        "series",
        "number",
        "code",
        "place",
        "date",
        "bornPlace",
        "living_place"
    )
    list_filter = (
        "series",
        "number",
        "code",
        "place",
        "date",
        "bornPlace",
        "living_place"
    )


@ admin.register(PersonalFile)
class FilterPersonalFile(admin.ModelAdmin):
    list_display = (
        "employee",
        "ITN",
        "insPolicy",
        "snils",
        "phoneNum",
        "bornDate",
        "sex",
        "fact_living_place",
        "family",
        "passport",
        "contract",
        "empBook"
    )
    list_filter = (
        "employee",
        "ITN",
        "insPolicy",
        "snils",
        "phoneNum",
        "bornDate",
        "sex",
        "fact_living_place",
        "family",
        "passport",
        "contract",
        "empBook"
    )
