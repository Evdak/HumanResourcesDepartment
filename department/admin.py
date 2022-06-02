from ast import Or
from django.contrib import admin
from django.http import HttpResponse
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


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
        doc = create_doc(el.id, el.employee, el.ITN, el.insPolicy, el.snils,
                         el.phoneNum, el.bornDate, el.sex,
                         el.fact_living_place, el.family,
                         el.passport, el.education, el.contract, el.empBook)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=personal_file{el.id}.docx'
        doc.save(response)

        return response


@admin.action(description='Отметить "Принято"')
def mark_as_accepted(modeladmin, request, queryset):
    if request.user.groups.filter(name='Начальник').exists():
        for el in queryset:
            el.status = 'Принято'
            el.save()


@admin.action(description='Отметить "Не принято"')
def mark_as_not_accepted(modeladmin, request, queryset):
    if request.user.groups.filter(name='Начальник').exists():
        for el in queryset:
            el.status = 'Не Принято'
            el.save()


@ admin.register(PersonalFile)
class FilterPersonalFile(ExportActionMixin, admin.ModelAdmin):
    actions = [create_personal_file]

    list_display = (
        "id",
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
        "id",
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


@ admin.register(Order)
class FilterOrder(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "file",
        "status"
    )
    list_filter = (
        "id",
        "type",
        "file",
        "status"
    )

    actions = [
        mark_as_accepted,
        mark_as_not_accepted
    ]
