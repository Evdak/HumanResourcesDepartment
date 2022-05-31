from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
from department.doc import create_doc

# Register your models here.


@admin.register(Employee)
class FilterEmployee(ExportActionMixin, admin.ModelAdmin):

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
class FilterContract(ExportActionMixin, admin.ModelAdmin):
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
class FilterEmpBook(ExportActionMixin, admin.ModelAdmin):
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
class FilterEducation(ExportActionMixin, admin.ModelAdmin):
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
class FilterEmpFamily(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "marStatus",
        "maidenName",
    )
    list_filter = (
        "marStatus",
        "maidenName",
    )


@ admin.register(FamilyComposition)
class FilterFamilyComposition(ExportActionMixin, admin.ModelAdmin):
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
class FilterPassport(ExportActionMixin, admin.ModelAdmin):
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


@admin.action(description='Сформировать личное дело')
def create_personal_file(modeladmin, request, queryset):
    for el in queryset:
        create_doc(el.id, el.employee, el.ITN, el.insPolicy, el.snils,
                   el.phoneNum, el.bornDate, el.sex,
                   el.fact_living_place, el.family,
                   el.passport, el.education, el.contract, el.empBook)


@ admin.register(PersonalFile)
class FilterPersonalFile(ExportActionMixin, admin.ModelAdmin):
    actions = [create_personal_file]

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
