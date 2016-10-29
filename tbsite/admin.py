from django.contrib import admin

# Register your models here.
from .models import *
from .xls2items import *

class RefAdmin ( admin.ModelAdmin ):
	list_display = ( 'id', 'rf_type', 'rf_descr')
	list_filter = [ 'rf_type' ]
	search_fields = [ 'rf_descr' ]
admin.site.register(Refs,RefAdmin)

class CPAdmin ( admin.ModelAdmin ):
	list_display = ( 'id', 'cp_type', 'cp_name')
	list_filter = [ 'cp_type' ]
	search_fields = [ 'cp_name' ]
admin.site.register(CPty,CPAdmin)

class ItemAdmin ( admin.ModelAdmin ):
	list_display = ( 'id', 'it_cat', 'it_grp', 'it_sname', 'it_code', 'it_orig_code', 'it_man')
	list_filter = [ 'it_cat', 'it_grp', 'it_man' ]
	actions = ['imp_items']	
	search_fields = [ 'it_sname', 'it_code', 'it_orig_code', 'it_descr' ]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "it_grp":
			kwargs["queryset"] = Refs.objects.filter(rf_type=RefType.GRP.value)
		if db_field.name == "it_cat":
			kwargs["queryset"] = Refs.objects.filter(rf_type=RefType.CAT.value)
		return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def imp_items(self, request, queryset):
		""" тест импорта товаров из файла (временный)
		"""
		res = getItems("/Users/mkv/tmp/items.xlsx", "Лист1")
		if len(res):
			self.message_user(request, res )

	imp_items.short_description = "Импорт товаров из файла /Users/mkv/tmp/items.xls.Лист1 (временный)"

admin.site.register(Items,ItemAdmin)

class AttrsAdmin ( admin.ModelAdmin ):
	list_display = ( 'id', 'at_sname', 'at_grp')
	list_filter = [ 'at_grp' ]
	search_fields = [ 'at_sname' ]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "at_grp":
			kwargs["queryset"] = Refs.objects.filter(rf_type=RefType.GRP.value)
		return super(AttrsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Attrs,AttrsAdmin)

class ATVAdmin ( admin.ModelAdmin ):
	list_display = ( 'id', 'av_item', 'av_attr', 'av_value')
	list_filter = [ 'av_attr' ]
	search_fields = [ 'av_value' ]
admin.site.register(AtVals,ATVAdmin)

class ATLAdmin ( admin.ModelAdmin ):
	list_display = ( 'il_orig', 'il_repl', 'il_rate')
	list_filter = [ 'il_rate' ]
	search_fields = [ 'il_descr' ]
admin.site.register(ItemLinks,ATLAdmin)

class ILHAdmin ( admin.ModelAdmin ):
	list_display = ( 'ls_name', 'ls_created', 'ls_buyer')
	list_filter = [ 'ls_buyer' ]
	search_fields = [ 'ls_name', 'ls_descr' ]
admin.site.register(ItemList,ILHAdmin)

class ILMAdmin ( admin.ModelAdmin ):
	list_display = ( 'lm_item', 'lm_quan', 'lm_price', 'lm_order', 'lm_rate')
	list_filter = [ 'lm_list' ]
	search_fields = [ 'lm_order', 'lm_descr' ]
admin.site.register(ILMatr,ILMAdmin)
