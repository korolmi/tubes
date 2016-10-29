import datetime

from django.db import models
from enum import Enum

# Мелкие справочники

# Супер справочник
RefType = Enum ( 'RefType', 'CAT GRP TAG' )
C_ref_types = ((RefType.CAT.value,"Категория"),(RefType.GRP.value,"Группа"),(RefType.TAG.value,"Тэг"))

class Refs (models.Model):
	rf_type = models.IntegerField('тип',choices=C_ref_types,default=RefType.TAG.value)
	rf_descr = models.CharField('описание',max_length=1000)

	class Meta:
		verbose_name = "Справочник"
		verbose_name_plural = "1. Справочники"
		ordering = [ "rf_type" ]

	def __str__(self):              
		return self.rf_descr

# контрагенты
CPType = Enum ( 'CPType', 'CLI SUP MAN' )
C_cp_types = ((CPType.CLI.value,"Клиент"),(CPType.SUP.value,"Поставщик"),(CPType.MAN.value,"Производитель"))

class CPty (models.Model):
	cp_type = models.IntegerField('тип',choices=C_cp_types,default=CPType.MAN.value)
	cp_name = models.CharField('имя',max_length=1000)

	class Meta:
		verbose_name = "Контрагент"
		verbose_name_plural = "2. Контрагенты"
		ordering = [ "cp_name" ]

	def __str__(self):              
		return self.cp_name

# товары
class Items (models.Model):
	it_code = models.CharField('код',max_length=100)
	it_sname = models.CharField('кратко',max_length=1000)
	it_cat = models.ForeignKey(Refs,verbose_name='категория',related_name='cat')
	it_grp = models.ForeignKey(Refs,verbose_name='группа',related_name='grp')
	it_tags  = models.ManyToManyField ( Refs, blank=True, verbose_name='тэги' )
	it_descr = models.CharField('описание',max_length=10000,blank=True, null=True)
	# photos
	it_man = models.ForeignKey(CPty,verbose_name='производитель')
	it_orig_code = models.CharField('оригинальный код',max_length=100)
	it_base_price = models.DecimalField('базовая цена', null=True,blank=True, max_digits=8, decimal_places=2)
	it_www = models.CharField('сайт',max_length=1000,blank=True, null=True)

	class Meta:
		verbose_name = "Товар"
		verbose_name_plural = "3. Товары"
		ordering = [ "it_code" ]

	def __str__(self):              
		return self.it_sname

# атррибуты товаров
class Attrs (models.Model):
	at_sname = models.CharField('атрибут',max_length=100)
	at_grp = models.ForeignKey(Refs,verbose_name='группа товаров')
	at_descr = models.CharField('описание',max_length=10000,blank=True, null=True)

	class Meta:
		verbose_name = "Атрибут"
		verbose_name_plural = "5. Атрибуты"
		ordering = [ "at_sname" ]

	def __str__(self):              
		return self.at_sname

# значения атрибутов товара
class AtVals (models.Model):
	av_item = models.ForeignKey(Items,verbose_name='товар')
	av_attr = models.ForeignKey(Attrs,verbose_name='атрибут')
	av_value = models.CharField('значение',max_length=1000)

	class Meta:
		verbose_name = "Значение атрибута"
		verbose_name_plural = "6. Значения атрибутов"
		ordering = [ "av_item" ]

	def __str__(self):              
		return self.av_value

# аналоги и связи
class ItemLinks (models.Model):
	il_orig = models.ForeignKey(Items,verbose_name='оригинал',related_name='orig')
	il_repl = models.ForeignKey(Items,verbose_name='аналог',related_name='repl')
	il_rate	= models.IntegerField('степень аналогичности',default = 1)
	il_descr = models.CharField('описание',max_length=10000,blank=True, null=True)

	class Meta:
		verbose_name = "Связь товаров"
		verbose_name_plural = "4. Связи товаров"
		ordering = [ "il_orig" ]

#	def __str__(self):              
#		return self.il_orig

# список товаров - заголовок
class ItemList (models.Model):
	ls_name = models.CharField('название списка',max_length=1000)
	ls_descr = models.CharField('описание',max_length=10000,blank=True, null=True)
	ls_created = models.DateField('создан')# ,auto_now_add=True)
	ls_buyer = models.CharField('закупщик',max_length=100)

	class Meta:
		verbose_name = "Список товаров"
		verbose_name_plural = "7. Списки товаров"
		ordering = [ "ls_name" ]

	def __str__(self):              
		return self.ls_name

	def save(self,**kwargs):	
		self.ls_created = datetime.datetime.today()
		super(ItemList, self).save()		

# список товаров - табличная часть
class ILMatr (models.Model):
	lm_list = models.ForeignKey(ItemList,verbose_name='список')
	lm_item = models.ForeignKey(Items,verbose_name='товар')
	lm_order = models.IntegerField('порядковый номер в списке')
	lm_quan = models.IntegerField('количество')
	lm_price = models.DecimalField('цена', max_digits=8, decimal_places=2)
	lm_rate = models.IntegerField('близость к оригиналу')
	lm_descr = models.CharField('описание',max_length=10000,blank=True, null=True)

	class Meta:
		verbose_name = "Товар списка"
		verbose_name_plural = "8. Товары списка"
		ordering = [ "lm_item" ]

#	def __str__(self):              
#		return self.lm_item
