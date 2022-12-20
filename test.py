# from config.db import db
#
#
# class MiMeta(type):
#
#     def __new__(cls, class_name, bases, attrs):
#         new_class = {}
#         for elemento, valor in attrs.items():
#             new_class[elemento] = valor
#         new_class['Meta'] = attrs.pop('Meta', None)
#         meta = new_class.get("Meta")
#         if meta:
#             new_class['app_label'] = getattr(meta, 'app_label', None)
#             new_class['verbose_name'] = getattr(meta, 'verbose_name', None)
#         print("new_class", new_class)
#         print(cls.implement_field)
#         return type(class_name, bases, new_class)
#
#     def implement_field(cls, *args, **kwargs):
#         app_label = cls.new_class.pop('app_label', None)
#         if app_label:
#             app_label = db.Column(db.Integer)
#             return app_label
#
#
# class MiClase(metaclass=MiMeta):
#     a = 5
#     nombre = 'inicio'
#
#     def __init__(self, *args, **kwargs):
#         pass
#
#     def imprime(self):
#         print("imprime")
#         print(self.nombre * self.a)
#
#     class Meta:
#         app_label = 'miclase'
#         verbose_name = 'prueba'
import datetime


class Carro:
    CONSTANTE = 5
    anio_act = datetime.datetime.today().year
    marca = ''
    modelo = ''
    numero_de_llantas = 4

    def __init__(self, marca, modelo, anio):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    def __str__(self):
        return f'Carro del anio {self.anio} - marca: {self.marca} modelo: {self.modelo}'

    def get_antiguedad(self):
        anio = self.anio_act - self.anio
        return f'El carro tiene {anio} anios'

    def get_estado(self):
        antiguedad = self.anio_act - self.anio
        if antiguedad >= self.CONSTANTE:
            return "Viejo"
        else:
            return "Nuevo"

    @classmethod
    def comprobar_estado(cls, anio):
        """
        Este metodo de clase no tiene acceso a los atributos
        que se inicializan en el constructor, solo los que se definene en un estado inicial,
        al declarar un metodo de clase hacemos uso de la palabra reservada cls
        :param anio:
        :return: bool
        """
        print("marca", cls.marca)
        antiguedad = cls.anio_act - anio
        if antiguedad >= cls.CONSTANTE:
            return True
        else:
            return False

    @staticmethod
    def peso_kg(peso):
        """
        Este metodo estatico no tiene interacción con los atributos de la clase ni metodos
        es totalmente independiente y se puede acceder sin instanciar la clase
        :param peso:
        :return: str
        """
        lb = 2.20462
        return lb * peso


carro = Carro(marca='Mazda', modelo='bt-50', anio=2018)

print(carro.get_antiguedad())
print(carro.comprobar_estado(2020))


# isinstance
# La clase no necesariamente debe tener un constructor

class PC:

    def __init__(self, so, marca, procesador):
        self.procesador = procesador
        self.marca = marca
        self.so = so


class Laptop(PC):
    pass
    # def __init__(self, so, marca, procesador, pantalla):
    #     super(Laptop, self).__init__(so, marca, procesador)


# pc = Laptop()
