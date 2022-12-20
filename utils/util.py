import os


def create_file(ruta, name, package: str = None, blueprint: bool = False):
    """
    :param ruta: ruta absoluta -> str
    :param name: nombre del archivo -> str
    :param package: nombre del packete -> str
    :param blueprint: True si desea crear el blueprint
    :return: None
    """
    path_file = os.path.join(ruta, name)
    if os.path.exists(ruta):
        if not os.path.exists(path_file):
            with open(path_file, 'w') as file:
                if path_file.endswith('__init__.py') and package and blueprint:
                    codigo = f'from flask import Blueprint \n\n' \
                             f'{package} = Blueprint("{package}",__name__, template_folder="templates")'
                    file.write(codigo)
                    file.close()
                if path_file.endswith('__init__.py') and package and not blueprint:
                    file.close()
                else:
                    file.close()

    else:
        if not os.path.exists(path_file):
            with open(path_file, 'w') as file:
                if path_file.endswith('__init__.py') and package and blueprint:
                    codigo = f'from flask import Blueprint \n\n' \
                             f'{package} = Blueprint("{package}",__name__, template_folder="templates")'
                    file.write(codigo)
                    file.close()
                if path_file.endswith('__init__.py') and package and not blueprint:
                    file.close()
                else:
                    file.close()
        raise Exception("la ruta no existe para crear el archivo")
