from sqlalchemy import create_engine, Column, Integer, String,Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import requests
import json

# Crear un engine para comunicarse con la base de datos
user = 'reto'
password = 'contrasena_simple'
host = 'localhost'
port = '5433'
database = 'CalcioPoli'

# Hacemos la conexión
connection_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
# SQLAlchemy engine
engine = create_engine(connection_str)
Session = sessionmaker(bind=engine)


# Definir la base
Base = declarative_base()

def abrir_sesion():
    return Session()

def cerrar_sesion(session):
    # Cerrar la sesión al terminar
    session.close()


import datetime
from datetime import datetime

now = datetime.now() # current date and time
# print(type(now))


date_fecha = now.date()
# print(date_fecha)
# print(type(date_fecha))
# 
#  


class miCRUD:
    @classmethod
    def read(cls, session):
        return session.query(Partidos).order_by(Partidos.fecha.desc()).all()
    def read_eventos_futuros(cls, session):
        return session.query(Partidos).order_by(Partidos.fecha.asc()).all()
    def read_en_vivo(cls, session):
        pass


    @classmethod
    def metodo_inicio_sesion(cls, session, **consulta):
        return session.query(cls).filter_by(**consulta).first()

    

# Definir las tablas
class Usuarios(Base,miCRUD):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True)
    NombreUsuario = Column(String)
    Contrasena = Column(String)
    Email = Column(String)
    relacion_comentarios = relationship("Comentarios", back_populates="relacion_usuarios")

class Comentarios(Base):
    __tablename__ = 'Comentarios'
    id = Column(Integer, primary_key=True)
    maxCaracteres = Column(String)
    Usuario_id = Column(Integer, ForeignKey('Usuarios.id'))
    relacion_usuarios = relationship("Usuarios", back_populates="relacion_comentarios")

class Partidos(Base,miCRUD):
    __tablename__ = 'Partidos'
    id = Column(Integer, primary_key=True)
    equipo_local = Column(String)
    equipo_visitante = Column(String)
    fecha = Column(Date)
    marcador_local = Column(Integer) 
    marcador_visitante = Column(Integer)







class PartidosEnVivo(Base,miCRUD):
    __tablename__ = 'PartidosEnVivo'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date)
    hora = Column(String)
    equipo_local = Column(String)
    equipo_visitante = Column(String)
    marcador_local = Column(Integer) 
    marcador_visitante = Column(Integer)
    estado = Column (String)
    minuto_partido = Column (Integer)
    relacion_Mensajes = relationship("Mensajes", back_populates="relacion_PartidosEnVivo")



class Mensajes(Base,miCRUD):
    __tablename__ = 'Mensajes'
    id = Column(Integer, primary_key=True)
    idPartidoEnVivo = Column(Integer, ForeignKey('PartidosEnVivo.id'))
    mensaje = Column (Text)
    fecha_hora = Column (DateTime)
    minuto_partido = Column (Integer)
    relacion_PartidosEnVivo = relationship("PartidosEnVivo", back_populates="relacion_Mensajes")






Base.metadata.create_all(engine)

def insertar_partidos_desde_json():
    url = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2024-25/it.1.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        partidos = data['matches'] 

        # Crear una sesión
        Sesion = sessionmaker(bind=engine)
        sesion = Sesion()

        for partido in partidos:
           
            
            if 'score' in partido and 'ft' in partido['score']:
                marcador_local = partido['score']['ft'][0]
                marcador_visitante = partido['score']['ft'][1]
            else: 
                marcador_local = None
                marcador_visitante = None

            nuevo_partido = Partidos(
                equipo_local=partido['team1'], 
                equipo_visitante=partido['team2'],
                fecha=partido['date'],
                marcador_local=marcador_local, 
                marcador_visitante=marcador_visitante
            )
            sesion.add(nuevo_partido)

    

        """
        voy a comentar pasao a paso la insercción del json con el bucle:

         - for partido in partidos:
            esto lo que hace es obtener cada registro del json del array matches, es decir, obtiene toda la información de 1 partido cada vez que itera: un ejemplo de partido en la primera iteracción:


        {
            "round": "Matchday 1",
            "date": "2024-08-17",
            "time": "18:30",
            "team1": "Genoa CFC",
            "team2": "FC Internazionale Milano",
            "score": {
                "ht": [
                1,
                1
                ],
                "ft": [
                    2,
                    2
                    ]
            }
        }


        - if 'score' in partido and 'ft' in partido['score']   
            primero comprueba si la clave score es una clave de partido (que es todo el contenido específico de ese partido   y como no asignamos el .value() va a pillar la clave como si fuera .keys()  ) y comprueba también si el campo ft existe en score (que es un campo tipo array de la clave score)

        - else en cuanto al else, le decimos que si el resultado del partido de la API no está actualizado o no se ha jugado se ponga en None en la base de datos

        - marcador_local = partido['score']['ft'][0] y marcador_visitante = partido['score']['ft'][1]
            hacemos 2 variables, una para obtener los goles del equipo local y otra con los goles del visitante
        
        - nuevo_partido = Partidos(
                equipo_local=partido['team1'], 
                equipo_visitante=partido['team2'],
                fecha=partido['date'],
                marcador_local=marcador_local, 
                marcador_visitante=marcador_visitante
            )
                    Insertamos los registros del json en las variables declaradas en la clase Partidos
        """
        sesion.commit()
        sesion.close()
        print("Partidos insertados correctamente.")
    else:
        print("Error al insertar los datos de los partidos")




insertar_partidos_desde_json()


"""
Sesion = sessionmaker(bind=engine)
sesion = Sesion()
partidos = sesion.query(Partidos).all()



leer = miCRUD()

print(leer.read(sesion).fecha)




for partido in partidos:
    if(Partidos.fecha!= 'null'):
        print(f"ID libro disponible: {partido.fecha}")

"""


Sesion = sessionmaker(bind=engine)
sesion = Sesion()


leer = miCRUD()
partidos = leer.read(sesion)  # Obtener todos los partidos


print("Registros en la tabla Partidos:")
for partido in partidos:
    print(f"ID: {partido.id}, Equipo Local: {partido.equipo_local}, Equipo Visitante: {partido.equipo_visitante}, Fecha: {partido.fecha}, Marcador: {partido.marcador_local} - {partido.marcador_visitante}")




sesion.commit()





# Insertamos un partido y 3 mensajes

registro_partido_en_vivo = PartidosEnVivo(fecha = "2024-11-11", hora = "10:30", equipo_local = "AS Roma", equipo_visitante = "Juventus FC",marcador_local = 1, marcador_visitante = 1, estado = "Segundo Tiempo", minuto_partido = 82)
sesion.add(registro_partido_en_vivo)
sesion.commit()


ahora = datetime.now()

PartidosVivo = sesion.query(PartidosEnVivo).all()

for PartidoVivo in PartidosVivo:
    mensaje1 = Mensajes(idPartidoEnVivo = PartidoVivo.id, mensaje = "Tarjeta amarilla para Koné",fecha_hora = ahora,  minuto_partido = 10,)
    mensaje2 = Mensajes(idPartidoEnVivo = PartidoVivo.id, mensaje = "Gol de Vlahovic",fecha_hora = ahora,  minuto_partido = 31,)
    mensaje3 = Mensajes(idPartidoEnVivo = PartidoVivo.id, mensaje = "Gol de Dybala",fecha_hora = ahora,  minuto_partido = 55,)

    sesion.add(mensaje1)
    sesion.add(mensaje2)
    sesion.add(mensaje3)

sesion.commit()


sesion.close()