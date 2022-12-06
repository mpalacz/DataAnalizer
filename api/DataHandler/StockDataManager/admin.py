from django.contrib import admin

from .models import Stock, Analysis, DataTable


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    pass


@admin.register(DataTable)
class DataTableAdmin(admin.ModelAdmin):
    pass


