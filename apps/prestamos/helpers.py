class GuardarDatosForms:

    @classmethod
    def save_model_productos(cls, model, lista_obj):
        object_productos = []
        for item in lista_obj:
            id = int(item['id'])
            id_estado_producto = int(item['id_estado_producto'])
            producto = model.query.get_or_404(id)
            producto.estados_id = id_estado_producto
            producto.activo = False
            object_productos.append(producto)
        return object_productos

    @classmethod
    def save_model_personal(cls, instancia, contacto, correo):
        # Personal.query.filter_by(identificador=dni).first()
        responsable = instancia
        if responsable:
            responsable.contacto = contacto
            responsable.correo = correo
        return responsable

    @classmethod
    def save_model_tt_salida(cls, instancia, ins_responsable, list_instance_productos):
        list_objects = []
        try:

            for item in list_instance_productos:
                instancia.tt_productos.append(item)
                item.save()
            instancia.save()
            instancia.generate_unix_time()
            instancia.save()
            ins_responsable.save()
            return {'message': f'Se genero el ticket {instancia.tt_salida} se envio un correo a : isaac',
                    'tt_salida': instancia.tt_salida}
        except Exception as e:
            raise Exception("Ocurrio un error al guardar el ticket de salida")
