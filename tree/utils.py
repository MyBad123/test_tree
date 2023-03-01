class ParseData:
    def __init__(self, db_data):
        self.data = db_data

    def str_or_none(self, obj):
        if type(obj) is int:
            return True

        if obj is None:
            return True

        return False

    def valid_data(self):
        if type(self.data) is not list:
            return False

        try:
            for i in self.data:
                if type(i.get('id')) is not int:
                    return False

                if type(i.get('name')) is not str:
                    return False

                if not self.str_or_none(i.get('parent')):
                    return False
        except AttributeError:
            return False

        return True

    def get_first_level(self):
        first_level = []
        for i in self.data:
            if i.get('parent') is None:
                first_level.append({
                    'id': i.get('id'),
                    'name': i.get('name'),
                    'position': ['level']
                })

        return first_level

    def get_parent_from_parent(self, new_struct: list):
        if new_struct[0].get('parent') is None:
            return new_struct
        else:
            for i in self.data:
                if new_struct[0].get('parent') == i.get('id'):
                    new_struct.insert(0, {
                        'id': i.get('id'),
                        'name': i.get('name'),
                        'position': ['level'],
                        'parent': i.get('parent')
                    })
                    break

            return self.get_parent_from_parent(new_struct)

    def work_with_levels(self, arr: list):
        index = 1
        for i in range(0, len(arr)):
            if arr[i].get('position') == ['level']:
                new_level = []
                for j in range(0, index):
                    new_level.append('level')

                arr[i]['position'] = new_level
                index += 1

            elif arr[i].get('position') == ['level', 'level', 'level']:
                new_level = []
                for j in range(0, index):
                    new_level.append('level')

                new_level.append('level')
                arr[i]['position'] = new_level

            else:
                new_level = []
                for j in range(0, index):
                    new_level.append('level')

                arr[i]['position'] = new_level

        return arr

    def union_data_tree(self, arr: list):
        first_level = self.get_first_level()
        index = 0
        for i in range(0, len(first_level)):
            if arr[0].get('id') == first_level[i].get('id'):
                index = i
                break

        first_level.pop(index)
        for i in range(len(arr) - 1, -1, -1):
            first_level.insert(index, arr[i])

        return first_level

    def get_level_by_id(self, id_obj):
        # search level
        new_struct = []
        for i in self.data:
            if id_obj == i.get('id'):
                first_id = i.get('id')
                new_struct.append({
                    'id': i.get('id'),
                    'name': i.get('name'),
                    'position': ['level'],
                    'parent': i.get('parent')
                })

        if not new_struct:
            return {
                'result': False,
                'data': []
            }

        # get child
        for i in self.data:
            if i.get('parent') == new_struct[0].get('id'):
                new_struct.append({
                    'id': i.get('id'),
                    'name': i.get('name'),
                    'position': ['level', 'level'],
                })

        # search parent of element
        if new_struct[0].get('parent') is not None:
            for i in self.data:
                if i.get('id') == new_struct[0].get('parent'):
                    parent_struct = i
                    break

            # change first elem
            if len(new_struct) == 1:
                new_struct[0]['position'] = ['level', 'level']
            else:
                new_struct[0]['position'] = ['level', 'level']
                for i in range(1, len(new_struct)):
                    new_struct[i]['position'] = ['level', 'level', 'level']

            # set parent to new struct
            new_struct.insert(0, {
                'id': parent_struct.get('id'),
                'name': parent_struct.get('name'),
                'position': ['level'],
                'parent': parent_struct.get('parent')
            })

            # get elements from this level
            for i in self.data:
                if parent_struct.get('id') == i.get('parent') and i.get('id') != first_id:
                    new_struct.append({
                        'id': i.get('id'),
                        'name': i.get('name'),
                        'position': ['level', 'level']
                    })

        new_struct = self.get_parent_from_parent(new_struct)
        new_struct = self.work_with_levels(new_struct)
        new_struct = self.union_data_tree(new_struct)

        return {
            'result': False,
            'data': new_struct
        }
