from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

directorio_credenciales = 'credentials_module.json'


def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)

    else:
        gauth.Authorize()

    return GoogleDrive(gauth)


def crear_archivo_text(nombre, contenido, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'title': nombre,
                                       'parents': [{'kind': 'drive#fileLink', 'id': id_folder}]})
    archivo.SetContentString(contenido)
    archivo.Upload()


def subir_archivo(ruta_archivo, id_folder, public=True):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [
        {'kind': 'drive#fileLink', 'id': id_folder}]})
    archivo['title'] = ruta_archivo.split('/')[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload(param={'supportsTeamDrives': True})
    if public:
        new_permission = {
            'id': 'anyoneWithLink',
            'type': 'anyone',
            'value': 'anyoneWithLink',
            'withLink': True,
            'role': 'reader'
        }
        archivo.auth.service.permissions().insert(fileId=archivo['id'], body=new_permission, supportsTeamDrives=True,
                                                  ).execute(http=archivo.http)
    return {'id': archivo.get('id'), 'link': archivo.get('webContentLink')}


def descargar_archivo(id_archivo, ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)


def buscar_archivos(query):
    resultados = []
    credenciales = login()
    dic = {}
    # Archivos con el nombre 'isaac' 'title'=isaac
    # Archivos que contengan 'isaac' y 'isaacisto':title contains 'isaac' and title contains isaacisto
    # Archivos que no contengan cierta cadena : not title contains 'isaac'
    # Archivos en el basurero: trashed=true
    lista_archivos = credenciales.ListFile({'q': query}).GetList()

    for f in lista_archivos:
        print(f)
        dic['id'] = f['id']
        dic['embedLink'] = f['embedLink']
        dic['downloadUrl'] = f['downloadUrl']
        dic['webContentLink'] = f['webContentLink']
        dic['alternateLink'] = f['alternateLink']
        dic['title'] = f['title']
        dic['mimeType'] = f['mimeType']
        dic['trashed'] = f['labels']['trashed']
        dic['createdDate'] = f['createdDate']
        dic['modifiedDate'] = f['modifiedDate']
        dic['version'] = f['version']
        dic['fileSize'] = f['fileSize']
        resultados.append(f)
    return resultados


def buscar_foler(query):
    resultados = []
    credenciales = login()
    dic = {}
    # Archivos con el nombre 'isaac' 'title'=isaac
    # Archivos que contengan 'isaac' y 'isaacisto':title contains 'isaac' and title contains isaacisto
    # Archivos que no contengan cierta cadena : not title contains 'isaac'
    # Archivos en el basurero: trashed=true
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    # response = credenciales.auth.service.files().list(q="mimeType='image/jpeg'",
    #                                         spaces='drive',
    #                                         fields='nextPageToken, '
    #                                                'files(id, name)',
    #                                         pageToken=None).execute()
    # print(response)
    print(lista_archivos)
    for f in lista_archivos:
        folder = credenciales.CreateFile({'title': f['id']})

        # file=folder.auth.service.files().list(q='title="images"').execute()
        # print(file)
        # print(file.get("id"))
        # print(credenciales.CreateFile({'id': f['id']}).auth.service.files().list(q='title="images"').execute())
    #     # dic['id'] = f['id']
    #     # dic['embedLink'] = f['embedLink']
    #     # dic['downloadUrl'] = f['downloadUrl']
    #     # dic['webContentLink'] = f['webContentLink']
    #     # dic['alternateLink'] = f['alternateLink']
    #     # dic['title'] = f['title']
    #     # dic['mimeType'] = f['mimeType']
    #     # dic['trashed'] = f['labels']['trashed']
    #     # dic['createdDate'] = f['createdDate']
    #     # dic['modifiedDate'] = f['modifiedDate']
    #     # dic['version'] = f['version']
    #     # dic['fileSize'] = f['fileSize']
    #     resultados.append(f)
    # return resultados


def borrar_recuperar(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    archivo.Trash()
    archivo.UnTrash()
    archivo.Delete()


def crear_carpeta(nombre_carpeta, id_folder=''):
    try:
        credenciales = login()
        if id_folder != '':
            folder = credenciales.CreateFile({'title': nombre_carpeta,
                                              'mimeType': 'application/vnd.google-apps.folder',
                                              'parents': [{"kind": "drive#fileLink",
                                                           "id": id_folder}]})
        else:
            folder = credenciales.CreateFile({'title': nombre_carpeta,
                                              'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        return folder.get('id')
    except Exception as e:
        raise e


# MOVER ARCHIVO
def mover_archivo(id_archivo, id_folder):
    credenciales = login()

    archivo = credenciales.CreateFile({'id': id_archivo})
    propiedades_ocultas = archivo['parents']
    archivo['parents'] = [{'isRoot': False,
                           'kind': 'drive#parentReference',
                           'id': id_folder,
                           'selfLink': 'https://www.googleapis.com/drive/v2/files/' + id_archivo + '/parents/' + id_folder,
                           'parentLink': 'https://www.googleapis.com/drive/v2/files/' + id_folder}]
    archivo.Upload(param={'supportsTeamDrives': True})


#
if __name__ == '__main__':
    # crear_archivo_text('Hola.txt', 'Hola mundo', '1uyQLufNG2wgzF06JJPmguN2uvyI56mPI')
    # subir_archivo(r'C:/Users/isaac/Desktop/desarrollos_flask/app_modular/base/pydrive/5-bootcamp.PNG',
    #               '1uyQLufNG2wgzF06JJPmguN2uvyI56mPI')
    # a = buscar_archivos('title="5-bootcamp.PNG"')
    # a = crear_carpeta('sistemasinventori')
    # b = crear_carpeta('qr', a)
    # c = crear_carpeta('images', a)
    print(buscar_foler('title="sistemasinventori" and title="sistemasinventori/images"'))

    # print("a", a)
