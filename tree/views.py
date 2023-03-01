from django.views import View
from django.shortcuts import render
from .models import TreeElements
from .utils import ParseData


class ViewMethods:
    def data_from_query(self):
        data = []
        for i in TreeElements.objects.all():
            try:
                data.append({
                    'id': i.id,
                    'name': i.name,
                    'parent': i.parent.id
                })
            except AttributeError:
                data.append({
                    'id': i.id,
                    'name': i.name,
                    'parent': None
                })

        return data


class GetParentElements(View, ViewMethods):
    """get all elements from menu"""

    def get(self, request):
        obj_tree = ParseData(db_data=super().data_from_query())

        return render(request, 'index.html', context={
            'elements': obj_tree.get_first_level()
        })


class GetElement(View, ViewMethods):
    """get one element by id"""

    def get(self, request, pk):
        obj_tree = ParseData(db_data=super().data_from_query())

        return render(request, 'index.html', context={
            'elements': obj_tree.get_level_by_id(id_obj=pk).get('data')
        })
