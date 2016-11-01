from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from .logger import *

""" Такая идея

- передать на страницу дополнительные атрибуты (кроме текста)
	- признак принадлежности к найденным (еще не существующим в списке) позициям
	- id товара
- на странице использовать признак для подкраски цветом
- по id красить (добавлением класса) пары ячеек
- по окончанию считывать покрашенные (их id)
"""

# для главной страницы
def mainPageView(request):
	""" главная страница """

	context = {  }
	return render ( request, 'tbsite/main_page.html', context )

# показ списка
def listMgrView(request, listid):
	""" работа со списком """

	if request.method == 'POST':	# команды от клиента, исполняем (если будут здесь)
		if request.is_ajax():		
			return JsonResponse(data)
	else:	# отрисовываем список
		# формируем список позиций
		mSet = []
		manDict = {}
		mItems = ILMatr.objects.filter(lm_list_id=listid,lm_rate=0).order_by('lm_order')
		for mi in mItems:	# идем по оригинальным позициям списка, пока предполагаем, что они есть всегда
			# читаем аналоги
			aItems = ILMatr.objects.filter(lm_list_id=listid,lm_order=mi.lm_order).exclude(lm_rate=0)
			aSet = {}
			for ai in aItems:
				ii = Items.objects.get(id=ai.lm_item_id)
				if ii.it_man_id not in manDict:	# формируем список производителей
					mm = CPty.objects.get(id=ii.it_man_id)
					manDict[ ii.it_man_id ] = mm.cp_name
				aSet[ii.it_man_id] = [ ii.it_code, ai.lm_price ]
			mii = Items.objects.get(id=mi.lm_item_id)
			mSet.append([ mi.lm_order, mii.it_code, mi.lm_quan, mi.lm_price, mi.lm_price*mi.lm_quan,aSet ])

		# преобразуем аналоги в линейные списки
		rSet = []
		manSet = []
		for m in mSet:
			ln = [ ["",m[0]], ["",m[1]], ["",m[2]], ["",m[3]], ["",m[4]] ]		# оригинальные позиции
			for manId in manDict:
				if manId in m[5]:
					ln.append( ["",m[5][manId][0]] )
					ln.append( ["",m[5][manId][1]] )
				else:
					ln.append( ["","-"] )
					ln.append( ["","-"] )
			rSet.append ( ln )
		for manId in manDict:
			manSet.append(manDict[manId])

		bst = [ "my_btn", "my_disabled", "my_disabled", "my_disabled"]
		context = { "ms": rSet, "mans": manSet, "bs": bst }
		return render ( request, 'tbsite/list_mgr_view.html', context )

def doCopyList ( aid, nname ):
	""" копирует список в новый (с новым именем) """

	ol = ItemList.objects.get(id=aid)

	# сам список
	nl = ItemList.objects.create(
		ls_name = nname,
		ls_descr = "(copy) " + ol.ls_descr,
		ls_buyer = "tester"
	)
	# копируем элементы
	for i in ILMatr.objects.filter(lm_list_id=ol.id):
		ni = ILMatr.objects.create(
			lm_list_id = nl.id,
			lm_item_id = i.lm_item_id,
			lm_order = i.lm_order,
			lm_quan = i.lm_quan,
			lm_price = i.lm_price,
			lm_rate = i.lm_rate,
			lm_descr = "(copy)" + i.lm_descr
		)

	return nl.id

def doDeleteList ( ol ):
	""" удаляет список со всеми элементам """

	# удаляем элементы
	for i in ILMatr.objects.filter(lm_list_id=ol.id):
		i.delete()
	# удяляем список 
	ol.delete()

def doSaveList ( req, lid ):
	""" Сохраняет список из черновика - фактически переименовывает и заменяет is_found 
		в параметрах передается оригинальный список - не черновик
	"""

	ol = ItemList.objects.get(id=lid)	

	# находим черновик
	ll = ItemList.objects.filter(ls_name="(DRAFT)"+ol.ls_name)
	if len(ll)==0 or len(ll)>1:
		data = {'id': lid, 'resMsg': "Что-то не так с черновиком..." }
		return data
	il = ll[0]	

	il.ls_name = ol.ls_name
	il.save()

	# проходим по товарам и меняем признак lm_is_found
	lItems = ILMatr.objects.filter(lm_list_id=il.id,lm_is_found=True)
	for i in lItems:
		i.lm_is_found = False
		i.save()

	# удаляем старый список
	doDeleteList(ol)

	data = {'id': il.id, 'resMsg': "" }
	return data

def doDelEls(request,listid):
	""" удаляет выделенные элементы из списка """

	idList = request.POST.get('idls').strip().split()

	for i in idList:
		aEl = ILMatr.objects.get(id=int(i))
		aEl.delete()

	data = { 'id': listid, 'resMsg': "" }

	return data

# всякие там добавки в список
def listAddView(request, listid):
	""" добавление аналогов в список """

	if request.method == 'POST':	# команды от клиента, исполняем (если будут здесь)
		if request.is_ajax():		
			data = {}
			if int(request.POST.get('cmd'))==1:
				data = doSaveList(request,listid)
			if int(request.POST.get('cmd'))==2:
				data = doDelEls(request,listid)
			return JsonResponse(data)
	else:	# отрисовываем список
		# создаем черновик списка, если он не существует
		il = ItemList.objects.get(id=listid)	# КОСТЫЛЬ: нужно потом будет еще фильтровать по пользователю
		lName = il.ls_name
		dlName = "(DRAFT)"+lName 
		lss = ItemList.objects.filter(ls_name=dlName)
		if not len(lss):	# черновика еще нет - создаем
			nlId = doCopyList ( listid, dlName )
			DoLog ( "copied:{0}".format(nlId))
		else:
			nlId = lss[0].id
			DoLog ( "found:{0}".format(nlId))


		# формируем список позиций собственно списка
		mSet = []	# предварительный список (нерегулярный)
		idSet = []	# список ID всех элементов результирующего список
		manDict = {}	# словарь наименований производителей
		mItems = ILMatr.objects.filter(lm_list_id=nlId,lm_rate=0).order_by('lm_order')
		for mi in mItems:	# идем по оригинальным позициям списка, пока предполагаем, что они есть всегда
			# читаем аналоги
			aItems = ILMatr.objects.filter(lm_list_id=nlId,lm_order=mi.lm_order).exclude(lm_rate=0)
			aSet = {}
			for ai in aItems:
				ii = Items.objects.get(id=ai.lm_item_id)
				if ii.it_man_id not in manDict:	# формируем список производителей
					mm = CPty.objects.get(id=ii.it_man_id)
					manDict[ ii.it_man_id ] = mm.cp_name
				aSet[ii.it_man_id] = [ ii.it_code, ai.lm_price, ai.id, ai.lm_is_found ]
				idSet.append(ii.id)
			mii = Items.objects.get(id=mi.lm_item_id)
			idSet.append(mii.id)
			# подбираем аналоги, которых еще нет в списке
			nSet = {}
			nItems = ItemLinks.objects.filter(il_orig_id=mii.id)
			for n in nItems:
				if n.il_repl_id not in idSet:	# такого в списке не было - добавляем
					ii = Items.objects.get(id=n.il_repl_id)
					if ii.it_man_id not in manDict:	# формируем список производителей
						mm = CPty.objects.get(id=ii.it_man_id)
						manDict[ ii.it_man_id ] = mm.cp_name
					idSet.append(ii.id)
					ni = ILMatr.objects.create(
						lm_list_id = nlId,
						lm_item_id = ii.id,
						lm_order = mi.lm_order,
						lm_quan = mi.lm_quan,
						lm_price = ii.it_base_price,
						lm_rate = n.il_rate,
						lm_is_found = True,
						lm_descr = "Created from orig->repl"
					)
					nSet[ii.it_man_id] = [ ii.it_code, ii.it_base_price, ni.id ]
			nItems = ItemLinks.objects.filter(il_repl_id=mii.id)
			for n in nItems:
				if n.il_orig_id not in idSet:	# такого в списке не было - добавляем
					ii = Items.objects.get(id=n.il_orig_id)
					if ii.it_man_id not in manDict:	# формируем список производителей
						mm = CPty.objects.get(id=ii.it_man_id)
						manDict[ ii.it_man_id ] = mm.cp_name
					idSet.append(ii.id)
					ni = ILMatr.objects.create(
						lm_list_id = nlId,
						lm_item_id = ii.id,
						lm_order = mi.lm_order,
						lm_quan = mi.lm_quan,
						lm_price = ii.it_base_price,
						lm_rate = n.il_rate,
						lm_is_found = True,
						lm_descr = "Created from repl->orig"
					)
					nSet[ii.it_man_id] = [ ii.it_code, ii.it_base_price, ni.id ]					
			mSet.append([ mi.lm_order, [mii.it_code,mi.id], mi.lm_quan, mi.lm_price, mi.lm_price*mi.lm_quan,aSet,nSet ])

		# преобразуем аналоги в линейные списки
		rSet = []
		manSet = []
		for m in mSet:
			ln = [ ["",m[0]], [str(m[1][1])+" c_sel",m[1][0]], ["",m[2]], ["",m[3]], ["",m[4]] ]		# оригинальные позиции
			for manId in manDict:
				if manId in m[5] and ( not m[5][manId][3]):		# старые позиции
					ln.append( ["cs_"+str(m[5][manId][2])+" c_sel",m[5][manId][0]] )
					ln.append( ["",m[5][manId][1]] )
				elif manId in m[5] and  m[5][manId][3]:			# найденные не сохраненные позиции
					ln.append( ["cs_"+str(m[5][manId][2])+" c_sel my_red",m[5][manId][0]] )
					ln.append( ["",m[5][manId][1]] )
				elif manId in m[6]:		# новые позиции 
					ln.append( ["cs_"+str(m[6][manId][2])+" c_sel my_red",m[6][manId][0]] )
					ln.append( ["",m[6][manId][1]] )
				else:
					ln.append( ["","-"] )
					ln.append( ["","-"] )
			rSet.append ( ln )
		for manId in manDict:
			manSet.append(manDict[manId])

		bst = [ "my_disabled", "my_disabled", "my_btn", "my_btn"]
		context = { "ms": rSet, "mans": manSet, "bs": bst }
		return render ( request, 'tbsite/list_mgr_view.html', context )
