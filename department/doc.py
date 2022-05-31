from docx import Document
from docx.shared import Inches


def create_doc(id, employee, ITN, insPolicy, snils,
               phoneNum, bornDate, sex,
               fact_living_place, family,
               passport, education, contract, empBook):

    document = Document()
    document.add_heading(f'ЛИЧНОЕ ДЕЛО № {id if id else "-"}', 0)
    document.add_paragraph(
        f'1. Имя: {employee.firstName if employee.firstName else "-"}')
    document.add_paragraph(
        f'2. Фамилия: {employee.middleName if employee.middleName else "-"}')
    document.add_paragraph(
        f'3. Отчество: {employee.lastName if employee.lastName else "-"}')
    document.add_paragraph(f'4. Пол: {sex if sex else "-"}')
    document.add_paragraph(
        f'5. Номер телефона: {phoneNum if phoneNum else "-"}')
    document.add_paragraph(
        f'6. Место проживания: {fact_living_place if fact_living_place else "-"}')
    document.add_paragraph(
        f'7. Дата рождения: {bornDate.strftime("%d-%m-%Y") if bornDate else "-"}')
    document.add_paragraph(
        f'8. Место проживания: {fact_living_place if fact_living_place else "-"}')
    document.add_paragraph(f'9. ИНН: {ITN if ITN else "-"}')
    document.add_paragraph(f'10. СНИЛС {snils if snils else "-"}')
    document.add_paragraph(
        f'11. Номер мед. полиса: {insPolicy if insPolicy else "-"}')
    document.add_paragraph(f'12. Семья: {"" if family else "-"}')

    if family:
        records = (
            (family.marStatus, family.maidenName),
        )
        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Семейное положение'
        hdr_cells[1].text = 'Девичья фамилия'
        for r1, r2 in records:
            row_cells = table.add_row().cells
            row_cells[0].text = r1
            row_cells[1].text = r2

    document.add_paragraph(f'13. Семья: {"" if family else "-"}')

    if family:
        records = (
            (family.marStatus, family.maidenName),
        )
        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Семейное положение'
        hdr_cells[1].text = 'Девичья фамилия'
        for r1, r2 in records:
            row_cells = table.add_row().cells
            row_cells[0].text = r1
            row_cells[1].text = r2

    # document.
    # print(f"{id=}", f"{employee=} {employee.firstName=}", f"{ITN=}", f"{insPolicy=}", f"{snils=}",
    #       phoneNum, f"{bornDate=}", f"{sex=}",
    #       fact_living_place, f"{family=}",
    #       passport, f"{education=}", f"{contract=}", f"{empBook=}")
    # id=1 employee=<Employee: user Наталья Васильева Юрьевна>
    # ITN=498390608771 insPolicy=10000000000000123 snils='123-123-123 01' phoneNum='+79321762312'
    # bornDate=datetime.date(1966, 1, 26) sex='Ж' fact_living_place='Россия, г. Нижневартовск, Зеленая ул., д. 5 кв.23'
    # family=None 4445 219261
    # education=<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x109ba75e0>
    # contract=<Contract: ID: 1> empBook=<EmpBook: ID: 2>

    # p = document.add_paragraph('1. A plain paragraph having some ')
    # p.add_run('bold').bold = True
    # p.add_run(' and some ')
    # p.add_run('italic.').italic = True

    # document.add_heading('Heading, level 1', level=1)
    # document.add_paragraph('Intense quote', style='Intense Quote')

    # document.add_paragraph(
    #     'first item in unordered list', style='List Bullet'
    # )
    # document.add_paragraph(
    #     'first item in ordered list', style='List Number'
    # )

    # records = (
    #     (3, '101', 'Spam'),
    #     (7, '422', 'Eggs'),
    #     (4, '631', 'Spam, spam, eggs, and spam')
    # )

    # table = document.add_table(rows=1, cols=3)
    # hdr_cells = table.rows[0].cells
    # hdr_cells[0].text = 'Qty'
    # hdr_cells[1].text = 'Id'
    # hdr_cells[2].text = 'Desc'
    # for qty, id, desc in records:
    #     row_cells = table.add_row().cells
    #     row_cells[0].text = str(qty)
    #     row_cells[1].text = id
    #     row_cells[2].text = desc

    # document.add_page_break()

    document.save('demo.docx')
