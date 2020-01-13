from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils import timezone

from db_module import models
from utils.get_number import MySnow


class CreateUnit(APIView):
    '''创建新的单位'''

    def post(self, request, *args, **kwargs):
        name = self.request.data.get('name', None)
        serial_number = self.request.data.get('serial_number', 0)
        assert name is not None, (-101, 'name为必传字段')
        unit_obj = models.Unit.objects.filter(name=name)
        if unit_obj:
            return JsonResponse({'code': -1, 'msg': 'name为' + str(name) + '的unit对象已存在'})
        else:
            try:
                with transaction.atomic():
                    unit_model = models.Unit(
                        name=name,
                        serial_number=serial_number
                    )
                    unit_model.save()
            except Exception as w:
                print(w)
                return JsonResponse({'code': -1, 'msg': '写入失败，错误信息为' + str(w)})
            return JsonResponse({'code': 1, 'msg': '创建成功'})

    def get(self, request, *args, **kwargs):
        name = self.request.GET.get('name')
        re_list = []
        if name:
            unit_obj = models.Unit.objects.filter(name__contains=name)
        else:
            unit_obj = models.Unit.objects.filter(is_del=False)
        for x in unit_obj:
            re_dict = {}
            re_dict['id'] = x.id
            re_dict['name'] = x.name
            re_dict['serial_number'] = x.serial_number
            re_list.append(re_dict)
        data = sorted(re_list, key=lambda e: e.__getitem__('serial_number'))
        return JsonResponse({'code': 1, 'msg': '请求成功', 'data': {'count': len(re_list), 'ret': data}})

    def delete(self, request, *args, **kwargs):
        id = self.request.data.get('id')
        try:
            with transaction.atomic():
                models.Unit.objects.filter(id=id).update(is_del=True, update_time=timezone.now())
        except Exception as w:
            return JsonResponse({'code': -1, 'msg': '删除失败，错误信息为' + str(w)})
        return JsonResponse({'code': 1, 'msg': '更新成功！'})

    def put(self, request, *args, **kwargs):
        id = self.request.data.get('id', None)
        name = self.request.data.get('name', None)
        serial_number = self.request.data.get('serial_number', None)
        assert id is not None, (-101, 'id为必传字段')
        update_dict = {'update_time': timezone.now()}
        if name:
            update_dict['name'] = name
        else:
            update_dict['serial_number'] = serial_number
        try:
            with transaction.atomic():
                models.Unit.objects.filter(id=id).update(**update_dict)
        except Exception as w:
            return JsonResponse({'code': -1, 'msg': '更新失败' + str(w)})
        return JsonResponse({'code': 1, 'msg': '更新成功！'})


class CreateRawMaterial(APIView):
    '''创建新的原料'''

    def post(self, request, *args, **kwargs):
        name = self.request.data.get('name', None)
        unit_id = self.request.data.get('unit_id', None)
        serial_number = self.request.data.get('serial_number', 0)
        assert name, (-101, 'name为必传字段')
        assert unit_id, (-101, 'unit_id为必传字段')
        try:
            with transaction.atomic():
                raw_material = models.RawMaterial(
                    name=name,
                    unit_id=unit_id,
                    serial_number=serial_number
                )
                raw_material.save()
        except Exception as w:
            return JsonResponse({'code': -1, 'msg': '创建失败，错误信息为' + str(w)})
        return JsonResponse({'code': 1, 'msg': '创建成功'})

    def put(self, request, *args, **kwargs):
        id = self.request.data.get('id')
        name = self.request.data.get('name', None)
        unit_id = self.request.data.get('unit_id', None)
        serial_number = self.request.data.get('serial_number', None)
        assert id, (-101, 'id为必传字段')
        update_dict = {'update_time': timezone.now()}
        if name:
            update_dict['name'] = name
        if unit_id:
            update_dict['unit_id'] = unit_id
        if serial_number:
            update_dict['serial_number'] = serial_number
        try:
            with transaction.atomic():
                models.RawMaterial.objects.filter(id=id).update(**update_dict)
        except Exception as w:
            return JsonResponse({'code': -1, 'msg': '更新失败，失败信息为' + str(w)})
        return JsonResponse({'code': 1, 'msg': '更新成功'})

    def get(self, request, *args, **kwargs):
        obj_set = models.RawMaterial.objects.filter(is_del=False)
        re_list = []
        for x in obj_set:
            re_dict = {}
            re_dict['id'] = x.id
            re_dict['name'] = x.name
            re_dict['unit'] = x.unit.name
            re_dict['serial_number'] = x.serial_number
            re_list.append(re_dict)
        return JsonResponse({'code': 1, 'msg': '请求成功', 'data': {'count': len(re_list), 'ret': re_list}})

    def delete(self, request, *args, **kwargs):
        id = self.request.data.get('id')
        assert id, (-101, 'id为必传字段')
        try:
            with transaction.atomic():
                models.RawMaterial.objects.filter(id=id).update(is_del=True)
        except Exception as w:
            return JsonResponse({'code': -1, 'msg': '删除失败，错误信息为' + str(w)})
        return JsonResponse({'code': 1, 'msg': '删除成功'})


class CreateMerchant(APIView):
    def post(self,request,*args,**kwargs):
        mer_name = self.request.data.get('mer_name') #商家名
        cliaddress = self.request.data.get('cliaddress') #商家详细地址
        cliarea = self.request.data.get('cliarea') #商家所在地区
        introduction = self.request.data.get('introduction','') #商家简介
        logo = self.request.data.get('logo') #商家logo
        father_mer_id = self.request.data.get('father_mer',None) #父级商家
        serial_number = self.request.data.get('serial_number',0) #排序编号

        try:
            with transaction.atomic():
                merchant_model = models.Merchant(
                    mer_no=1,
                    mer_name=mer_name,
                    cliaddress=cliaddress,
                    cliarea=cliarea,
                    introduction=introduction,
                    logo=logo,
                    father_mer_id=father_mer_id,
                    serial_number=serial_number
                )
                merchant_model.save()
                dataID = merchant_model.id
                final_mer_no = MySnow(dataID=dataID).get_id()
                models.Merchant.objects.filter(id=dataID).update(mer_no=final_mer_no)
        except Exception as w:
            return JsonResponse({'code':-1,'msg':'创建失败，错误信息：'+str(w)})
        return JsonResponse({'code':1,'msg':'创建成功'})

    def get(self,request,*args,**kwargs):
        id = self.request.GET.get('id',None)
        re_list = []
        try:
            if id:
                merchant_obj = models.Merchant.objects.get(id=id)
                re_dict = {}
                re_dict['id'] = merchant_obj.id
                re_dict['mer_no'] = merchant_obj.mer_no
                re_dict['mer_name'] = merchant_obj.mer_name
                re_dict['cliaddress'] = merchant_obj.cliaddress
                re_dict['cliarea'] = merchant_obj.cliarea
                re_dict['introduction'] = merchant_obj.introduction
                re_dict['logo'] = merchant_obj.logo
                re_dict['father_mer'] = merchant_obj.father_mer
                re_dict['serial_number'] = merchant_obj.serial_number

                return JsonResponse({'code':1,'msg':'请求成功','data':{'ret':[re_dict]}})
            else:
                merchant_set = models.Merchant.objects.filter(is_del=False)
                for x in merchant_set:
                    re_dict = {}
                    re_dict['id'] = x.id
                    re_dict['mer_no'] = x.mer_no
                    re_dict['mer_name'] = x.mer_name
                    re_dict['cliaddress'] = x.cliaddress
                    re_dict['cliarea'] = x.cliarea
                    re_dict['introduction'] = x.introduction
                    re_dict['logo'] = x.logo
                    re_dict['father_mer'] = x.father_mer
                    re_dict['serial_number'] = x.serial_number
                    re_list.append(re_dict)

                size = request.GET.get("size", 10)
                pg = request.GET.get("pg", 1)
                p = Paginator(re_list, size)
                next_page = None
                previous_page = None
                page1 = p.page(pg)
                if page1.has_next():
                    next_page = page1.next_page_number()
                if page1.has_previous():
                    previous_page = page1.previous_page_number()
                data = {"count": p.count, "num_pages": p.num_pages, "next_page": next_page, "previous_page": previous_page,
                        "ret": page1.object_list}

                return JsonResponse({'code': 1, 'msg': '请求成功', 'data': data})
        except Exception as w :
            return JsonResponse({'code': -1, 'msg': '请求失败', 'data': None})

    def delete(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        assert id ,(-101,'id是必传字段')
        try:
            with transaction.atomic():






