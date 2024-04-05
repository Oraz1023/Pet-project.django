import csv


from django.http import *
from django.db.models import QuerySet
from django.db.models.options import Options
class ExportAsCSVFileMixins:
    def export_csv(self, requset: HttpRequest, queryset: QuerySet):
        meta: Options =self.model._meta
        fields_name =[field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}-export.csv'
        csv_writer=csv.writer(response)
        csv_writer.writerow(fields_name)

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in fields_name])
            return response

    export_csv.short_description = 'Export CSV'
"""

Давайте разберем код по строкам:

1.class ExportAsCSVFileMixins:: Определение класса ExportAsCSVFileMixins.

2.def export_csv(self, requset: HttpRequest, queryset: QuerySet):: Определение метода export_csv, который принимает self (экземпляр класса), request (запрос HTTP) и queryset (набор запросов). Этот метод отвечает за экспорт данных из queryset в CSV формат.

3.meta: Options = self.model._meta: Получение метаданных модели, к которой принадлежит экземпляр класса. self.model предположительно является моделью, к которой применяется этот миксин.

4.fields_name = [field.name for field in meta.fields]: Создание списка имен полей модели, которые будут использоваться в CSV файле.

5.response = HttpResponse(content_type='text/csv'): Создание объекта HttpResponse с типом содержимого text/csv, который будет использоваться для отправки CSV данных.

6.response['Content-Disposition'] = f'attachment; filename={meta}-export.csv': Установка заголовка Content-Disposition для указания браузеру, что файл должен быть загружен как вложение с указанным именем файла.

7.csv_writer = csv.writer(response): Создание объекта csv.writer, который будет использоваться для записи CSV данных в response.

8.csv_writer.writerow(fields_name): Запись заголовков (имен полей) в CSV файл.

9.for obj in queryset:: Начало цикла по объектам в queryset.

10.csv_writer.writerow([getattr(obj, field) for field in fields_name]): Получение значений полей объекта obj и запись их в CSV файл.

11.return response: Возврат CSV данных в виде HTTP ответа.

12.export_csv.short_description = 'Export CSV': Добавление атрибута short_description к методу export_csv. Этот атрибут может использоваться, например, в административном интерфейсе Django для отображения текста, описывающего функциональность этого метода.
"""