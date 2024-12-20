from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('registro_sesion.html')

def registro_sesion(environ, start_response):
    response = template.render().encode('utf-8') 
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]