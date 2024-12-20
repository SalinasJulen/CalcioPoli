from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import vistas
import modelos
import vistas_eventos_anteriores
import vistas_eventos_posteriores
import vistas_registro
import vistas_sesion
import vistas_merch

import vistas_en_vivo

from datetime import datetime  # Asegúrate de importar datetime

def mostar_eventos():
    sesion = modelos.abrir_sesion()
    hoy = datetime.now().strftime("%Y-%m-%d")
    eventos = sesion.query(modelos.Partidos).filter(modelos.Partidos.fecha <= hoy).filter(modelos.Partidos.marcador_local != None).order_by(modelos.Partidos.fecha.desc()).all()
    modelos.cerrar_sesion(sesion) 
    return eventos


def mostar_eventos_futuros():
    sesion = modelos.abrir_sesion()
    hoy = datetime.now().strftime("%Y-%m-%d")

    
    eventos_futuros = sesion.query(modelos.Partidos).filter(modelos.Partidos.fecha > hoy).order_by(modelos.Partidos.fecha.asc()).all()

    modelos.cerrar_sesion(sesion) 
    return eventos_futuros




def mostar_eventos_en_vivo():
    sesion = modelos.abrir_sesion()
    en_vivo = sesion.query(modelos.PartidosEnVivo).filter(modelos.PartidosEnVivo.id != None).all()
   
    modelos.cerrar_sesion(sesion) 
    return en_vivo
    

def mostar_mensajes_en_vivo():
    sesion = modelos.abrir_sesion()
    mensajes_en_vivo = sesion.query(modelos.Mensajes).filter(modelos.Mensajes.id != None).all()

    modelos.cerrar_sesion(sesion) 
    return mensajes_en_vivo



def add_user(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            params = parse_qs(data)
            
            
            producto = modelos.Usuarios(
                NombreUsuario=params['NombreUsuario'][0],
                Contrasena=params['Contrasena'][0],
                Email=params['Email'][0]
            )
            sesion = modelos.abrir_sesion()
            sesion.add(producto)
            sesion.commit()
            modelos.cerrar_sesion(sesion)
            sesion = None

            # en vez de llamar al método create() hacemos el sesion.add() directamente como en sqlalchemy, además tengo que hacer el sesion.comit()        ya que importamos modelos.py importamos a su vez sqlalchemy
            
        
            start_response('303 See Other', [('Location', '/es')])
            return [b'']
        except Exception as e:
            print(f"Error al agregar usuario: {e}") 
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [b'Error interno del servidor.']
    else:
        return vistas.handle_404(environ, start_response)





def iniciar_sesion(environ, start_response):
    hayUser = False # Declaramos hayUser como false

    if environ['REQUEST_METHOD'] == 'POST':
        size = int(environ.get('CONTENT_LENGTH', 0))
        data = environ['wsgi.input'].read(size).decode()
        params = parse_qs(data)
        NombreUsuario = params.get('NombreUsuario', [None])[0]
        Contrasena = params.get('Contrasena', [None])[0]
        print('contrasena: ' +  Contrasena)
        sesion = modelos.abrir_sesion()
        
        consulta = {"NombreUsuario": NombreUsuario, "Contrasena": Contrasena}
        usuarios = modelos.Usuarios.metodo_inicio_sesion(sesion, **consulta)
        

        # usuarios = sesion.query(modelos.Usuarios).filter(modelos.Usuarios.NombreUsuario == NombreUsuario).filter(modelos.Usuarios.Contrasena == Contrasena).all()
        #print('usuario de BD: ' +  usuarios.user)
        if usuarios:
            hayUser = True
            return NombreUsuario, sesion, hayUser
        else:
            sesion.close()
            sesion = None
            return None, None, None
            
        
    return None,None, hayUser # tenemos que asegurar que devuelva algo aunque no se haga la solicitud el POST
        

def finalizar_sesion(session):
    # Cerrar la sesión al terminar
    modelos.cerrar_sesion(session)


def app(environ, start_response):
    global sesion, usuario, hayUser
    path = environ.get('PATH_INFO')
    if path == '/':
        return vistas.spanish_handle_index(environ, start_response) # aquí no pongo los productos ya que no es un campo obligatorio
    if path == '/index.html':
        return vistas.spanish_handle_index(environ, start_response) # aquí no pongo los productos ya que no es un campo obligatorio
    elif path == '/es':
        return vistas.spanish_handle_index(environ, start_response) # aquí no pongo los productos ya que no es un campo obligatorio
    elif path == '/add_user':
        return add_user(environ, start_response)
    elif path.startswith('/static/'):
        return vistas.serve_static(environ, start_response)
    elif path == '/favicon.ico':
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Favicon no encontrado.']
    elif path == '/logoEmpresa.png':
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Foto no encontrada.']
    elif path == '/kebab.png':
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Foto no encontrada.']
    elif path == '/venezia.jpg':
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Foto no encontrada.']
    elif path == '/roma.jpg':
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Foto no encontrada.']
    
    elif path == '/registro_sesion.html':  # Nueva ruta para el registro
        return vistas_registro.registro_sesion(environ, start_response)  # Llamar a la nueva vista
    


    elif path == '/merch.html':
        return vistas_merch.merchandising(environ, start_response)
    


    elif path == '/eventos_pasados.html':
        eventos = mostar_eventos()
        return vistas_eventos_anteriores.eventos_anteriores(environ, start_response, eventos)
    elif path == '/eventos_futuros.html':
        eventos_futuros = mostar_eventos_futuros()
        return vistas_eventos_posteriores.eventos_posteriores(environ, start_response, eventos_futuros)
    
    elif path == '/en_vivo.html':
        en_vivo = mostar_eventos_en_vivo()
        mensajes_en_vivo = mostar_mensajes_en_vivo()
        return vistas_en_vivo.eventos_en_vivo(environ, start_response, en_vivo)



    elif path == '/login':
        usuario, sesion, hayUser = iniciar_sesion(environ, start_response)
      
        return vistas_sesion.logica_sesion(start_response, hayUser)
    elif path == '/noUser':
        return vistas_sesion.no_user_handle(environ, start_response)    
    elif path == '/logout':
        finalizar_sesion(sesion)
        sesion = None
        return vistas_sesion.sesion_finish(start_response, hayUser)
    
    elif path == '/iniciar_sesion.html':
        # Mostrar el formulario de inicio de sesión
        return vistas_sesion.sesion_init(environ, start_response) 
    else:
        return vistas.handle_404(environ, start_response)






if __name__ == "__main__":
    host = 'localhost'
    port = 888

    httpd = make_server(host, port, app)
    print(f"Servidor en http://{host}:{port}")
    httpd.serve_forever()
