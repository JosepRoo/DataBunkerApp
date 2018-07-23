from app.common.tree import Tree
from app.models.brands.brand import Brand
from app.models.categories.category import Category
from app.models.privileges.errors import WrongElementType, WrongPrivilegeAssignment, PrivilegeDoesNotExist


class Privilege:
    def __init__(self, privilege_tree=None):
        self.privilege_tree = Tree(privilege_tree) if privilege_tree is not None else Tree()

    def add_privilege(self, element_type, element_to_add):
        """
        Function to add a privilege to the privilege tree of a user
        :param element_type: string of type element to add ex: channel
        :param element_to_add: dictionary with ids of elements to add as privilege
               dict['channel_id']['category_id']['brand_id']['product_id'] = 1
               dict['channel_id']['category_id']['brand_id'] = 1
               dict['channel_id']['category_id'] = 1
               dict['channel_id']= 1
        :return: returns the privilege_tree after update
        """
        try:
            channel = list(element_to_add.keys())[0]
            if element_type == "channel":
                self.privilege_tree[channel] = int(element_to_add[channel])
            else:
                category = list(element_to_add.get(channel).keys())[0]
                if element_type == "category":
                    self.privilege_tree[channel][category] = int(element_to_add[channel][category])
                else:
                    brand = list(element_to_add.get(channel).get(category).keys())[0]
                    if element_type == "brand":
                        self.privilege_tree[channel][category][brand] = int(element_to_add[channel][category][brand])
                    else:
                        if element_type == "product":
                            product = list(element_to_add.get(channel).get(category).get(brand).keys())[0]
                            self.privilege_tree[channel][category][brand][product] = int(
                                element_to_add[channel][category][brand][product])
        except TypeError as e:
            message = str(e)
            if 'object does not support' in message:
                raise WrongPrivilegeAssignment(
                    "No puedes assignar el privilegio, porque un privilegio mayor existe, borralo e intentalo de nuevo")
            elif 'argument must be a string' in message:
                raise WrongElementType("El tipo de elemento dado es incorrecto")
        return self.privilege_tree

    def remove_privilege(self, element_type, element_to_remove):
        """
        Function to remove a privilege from the privilege tree of a user
        :param element_type: string of type element to add ex: channel
        :param element_to_remove: dictionary with ids of elements to add as privilege
               dict['channel_id']['category_id']['brand_id']['product_id'] = 1
               dict['channel_id']['category_id']['brand_id'] = 1
               dict['channel_id']['category_id'] = 1
               dict['channel_id']= 1
        :return: returns the privilege_tree after update
        """
        try:
            channel = list(element_to_remove.keys())[0]
            if element_type == "channel":
                del self.privilege_tree[channel]
            else:
                category = list(element_to_remove.get(channel).keys())[0]
                if element_type == "category":
                    del self.privilege_tree[channel][category]
                else:
                    brand = list(element_to_remove.get(channel).get(category).keys())[0]
                    if element_type == "brand":
                        del self.privilege_tree[channel][category][brand]
                    else:
                        if element_type == "product":
                            product = list(element_to_remove.get(channel).get(category).get(brand).keys())[0]
                            del self.privilege_tree[channel][category][brand][product]
        except KeyError:
            raise PrivilegeDoesNotExist("No se puede borrar el privilegio ya que no existe en este usuario")
        return self.privilege_tree

    def get_privilege(self, element_type, element_id=None):
        """
        Function to find if given an element_id it is on the user privileges
        :param element_type: parameter to know the type of element we are searching for
        :param element_id:
        :return: returns the _id of the elements
        """
        # cargar todos los canales en los privilegios
        if element_type == "channel":
            channels = list(self.privilege_tree.keys())
            if not channels:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            return channels
        elif element_type == "category":
            # checar si el channel_id es padre de las categorias de los privilegios
            channel = self.privilege_tree.get(element_id)
            # si es int cargar todas las categorias del canal
            if isinstance(channel, int):
                return "All"
            # si es un diccionario cargar las cateogrias de los privilegios
            elif isinstance(channel, dict):
                return list(channel.keys())
            # si es None lanzar excpecion
            else:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
        elif element_type == "brand":
            # obtener la categoria dado el category_id
            category = Category.get_by_id(element_id)
            # obtener el canal en los privilegios de la cateogria dada
            priv_channel = self.privilege_tree.get(category.parentElementId)
            # si no existe lanzar excepcion
            if priv_channel is None:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            else:
                # si es int mandar todas las marcas de ese category en ese canal
                if isinstance(priv_channel, int):
                    return "All"
                else:
                    # obtener la cateogria en los privilegios
                    priv_category = priv_channel.get(element_id)
                    # si es int regresar todas las marcas de esa categoria
                    if isinstance(priv_category, int):
                        return "All"
                    # si es un dict todas las marcar de esa categoria
                    elif isinstance(priv_category, dict):
                        return list(priv_category.keys())
                    # si es None lanzar una excepcion
                    else:
                        raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
        elif element_type == "product":
            brand = Brand.get_by_id(element_id)
            category = Category.get_by_id(brand.parentElementId)
            priv_channel = self.privilege_tree.get(category.parentElementId)
            if priv_channel is None:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            else:
                if isinstance(priv_channel, int):
                    return "All"
                else:
                    priv_category = priv_channel.get(category._id)
                    # si es int regresar todas las marcas de esa categoria
                    if isinstance(priv_category, int):
                        return "All"
                    elif isinstance(priv_category, dict):
                        priv_brand = priv_category.get(element_id)
                        if isinstance(priv_brand, int):
                            return "All"
                        elif isinstance(priv_brand, dict):
                            return list(priv_brand.keys())
                        else:
                            raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
                    # si es None lanzar una excepcion
                    else:
                        raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")

    def json(self):
        return self.privilege_tree
