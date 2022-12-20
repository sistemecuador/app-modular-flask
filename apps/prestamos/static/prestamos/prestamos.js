let tabla;
let dataPrestamo = {
    array: [],
    list: function () {
        tabla = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            // scrollX: true,
            data: this.array,
            columns: [
                {'data': 'id'},
                {'data': 'codigo_producto'},
                {'data': 'name_producto'},
                {'data': 'name_producto'},
                {'data': 'marca'},
                {'data': 'modelo_producto'},
                {'data': 'precio'},
            ],
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center'
                },
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        //var buttons='<i class="fas fa-edit">';
                        let buttons = '<button rel="eliminar" class="btn btn-sm btn-default"><i style="color: red" class="fas fa-times"></i></button> ';
                        buttons += '<button class="btn btn-sm btn-default"><i class="fas fa-edit"></i></button> ';
                        return buttons;
                    },

                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let image = '<div class="row"><div class="col-lg-12"><img src="' + row.image + '" alt="' + row.name_producto + '" width="75px" height="75px" class="img-fluid"></div></div>';
                        return image;
                    },

                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let select = '<div id="select_estados"><select name="estados_id" id="estados_id_' + row.id + '" class="form-control estados_id_' + row.id + '">'
                        if (row.estados_productos.length > 0) {
                            for (const estado of row.estados_productos) {
                                if (estado[0] === row.estados_id) {
                                    select += '<option id="' + row.id + '" value="' + estado[0] + '" selected>' + estado[1] + '</option>'
                                } else {
                                    select += '<option id="' + row.id + '" value="' + estado[0] + '">' + estado[1] + '</option>'
                                }

                            }
                        } else {
                            select += '<option id="0" value="0">----</option>'
                        }
                        select + '</div>'
                        return select;
                    },

                }

            ]
        })
    }
}

function enviarData() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            action: 'actualizar',
            id: 1
        }
    }).done(function (data) {
        console.log(data)
    }).fail(function (error) {
        console.log("Error", str(e))
    })
}

function selectDepartamento(id) {
    let deparatmento = document.querySelector('select[name="departamento"]')
    if (id !== null) {
        deparatmento.querySelector('[value="' + id + '"]').selected = true
        deparatmento.removeAttribute('disabled')
        // document.querySelector('select[name="departamento"] [value="' + id + '"]').selected = true
    } else {
        deparatmento.querySelector('[value="0"]').selected = true
        deparatmento.setAttribute('disabled', true)
        // document.querySelector('select[name="departamento"] [value="0"]').selected = true

    }
}

function filterArray(obj, id) {
    if (obj.id === id) {
        console.log('id', id, obj)
        return obj
    }
}

let removeRow = () => {
    $('#data tbody').on('click', 'button[rel="eliminar"]', function (e) {
        let tr = tabla.cell($(this).closest('td, li')).index();
        let data = tabla.row(tr.row).data();
        let idx = dataPrestamo.array.indexOf(data)
        dataPrestamo.array.splice(idx, 1)
        dataPrestamo.list()

    })
}

let changeEstadosProductos = () => {

    $('#data tbody').on('change', 'select[name="estados_id"]', function (e) {
        let tr = tabla.cell($(this).closest('td, li')).index();
        let data = tabla.row(tr.row).data();
        let estado = document.querySelector('.estados_id_' + data.id + '').value
        let idx = dataPrestamo.array.indexOf(data)
        dataPrestamo.array[idx].estados_id = Number(estado)
        dataPrestamo.list()
        console.log("cambiada", dataPrestamo.array)
    })
}

let responsable = {
    id: '',
    identificador: '',
    dni: '',
    nombres: '',
    contacto: '',
    corre: '',
    total_p: '',
    departamento: '',
    observacion: '',
    activo: false,
}
let idProducts = []

let resetDatas = (forms = []) => {
    for (const form of forms) {
        form.reset()
    }
    idProducts = []
    dataPrestamo.array = []
    dataPrestamo.list()
}

function setFormTicket(data) {
    document.getElementById('dni').value = data.identificador
    document.getElementById('nombres').value = data.nombre_completo
    document.getElementById('contacto').value = data.contacto
    document.getElementById('correo').value = data.correo
    selectDepartamento(data.id_departamento)


}

let sumarProductos = () => {
    let total = document.getElementById('total_p')
    let valor = dataPrestamo.array.length
    total.value = valor
}

document.addEventListener('DOMContentLoaded', (e) => {
    let form_productos = document.getElementById('form-productos')
    form_productos.addEventListener("submit", (e) => {
        e.preventDefault()
        const data = new FormData(e.target)
        fetch(window.location.pathname, {
            method: 'POST',
            body: data,
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (!data.hasOwnProperty("error")) {
                    if (idProducts.includes(data.id)) {
                        return
                    }
                    idProducts.push(data.id)
                    dataPrestamo.array.push(data)
                    dataPrestamo.list()
                    sumarProductos()
                } else {
                    console.log("Error")
                }
            })
            .catch(error => alert(error.toString()))
        form_productos.reset()

    })


    let eliminacion = document.querySelector('.eliminar-productos')
    eliminacion.addEventListener("click", () => {
        dataPrestamo.array = []
        idProducts = []
        dataPrestamo.list()
        let total_p = document.getElementById('total_p')
        total_p.value = 0
    })


    let form_responsable = document.getElementById('form_responsable')
    form_responsable.addEventListener("submit", (e) => {
        e.preventDefault()
        let data = new FormData(form_responsable)
        fetch(window.location.pathname, {
            method: 'POST',
            body: data
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (!data.hasOwnProperty("error")) {
                    setFormTicket(data)
                    // idProducts.push(data.id)
                } else {
                    console.log('error', data)
                }
            })
            .catch(error => console.log('error', error))

    })


    let form_ticket = document.getElementById('form_tt_salida')
    form_ticket.addEventListener('submit', (e) => {
        // let action = document.querySelector('.action_tt')
        // action.value = 'generar_tt'
        e.preventDefault()
        let arrayProductos = []
        for (const producto of dataPrestamo.array) {
            let json = {'id': producto.id, 'id_estado_producto': producto.estados_id}
            arrayProductos.push(json)
        }
        let data = new FormData(form_ticket)
        data.append('list_productos', JSON.stringify(arrayProductos))
        if (dataPrestamo.array.length > 0) {
            fetch(window.location.pathname, {
                method: 'POST',
                body: data
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    if (!data.hasOwnProperty("error")) {
                        resetDatas([form_ticket,form_responsable,form_ticket])
                    } else {
                        if (data.hasOwnProperty('validate_form')) {
                            let form_validates = data.validate_form
                            let arrayKeys = Object.keys(form_validates)
                            for (const key of arrayKeys) {
                                let input = document.getElementById(key)
                                input.classList.add('is-invalid')
                            }
                        } else {
                            console.log("Error")
                        }
                    }
                })
                .catch(error => console.log('error', error))
        } else {
            console.log("No hay productos seleccionados")
        }

    })


    let btn_limpiar_forms = document.querySelector('.btn-limipar-formularios')
    btn_limpiar_forms.addEventListener('click', (e) => {
        resetDatas([form_ticket,form_responsable,form_ticket])

    })
    removeRow()
    changeEstadosProductos()
    dataPrestamo.list()

})
