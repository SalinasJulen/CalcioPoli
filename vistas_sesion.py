from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('iniciar_sesion.html')



def spanish_handle_index(environ, start_response, productos, usuario):
    # Lógica para la ruta '/es'
    # response = template.render(productos=productos).encode('utf-8') #renderizar 'index.html' con los productos recogidos de la BD
    response = template.render(productos=None, usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    # return [b'Inicio Sesión']
    return [response]



def sesion_init(environ, start_response):

    response = template.render().encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    # return [b'Inicio Sesión']
    return [response]






def logica_sesion(start_response, hayUser):
    if hayUser:
        start_response('303 See Other', [('Location', '/')])
        return [b'']
    else:
        start_response('303 See Other', [('Location', '/iniciar_sesion.html')])
        return [b'No se ha encontrado el usuario']

def sesion_finish(start_response, hayUser):
    start_response('303 See Other', [('Location', '/')])
    return [b'']






def handle_index(environ, start_response):
    # Lógica para la ruta '/en'
    response = template.render().encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]


def no_user_handle(environ, start_response):
    # Lógica para la ruta '/noUser'
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [b'Usuario no encontrado, redireccionando...']