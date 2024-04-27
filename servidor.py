# Importamos los módulos necesarios
import grpc
from concurrent import futures

from numpy import int32

# Importamos las librerías generadas por el compilador gRPC donde se encuentran las definiciones de las funciones y mensajes
import twitter_pb2
import twitter_pb2_grpc
import admindata

registrados = admindata.Registrados()
# Añadimos 3 usuarios registrados para agilizar pruebas
registrados.registrar_usuario("ana", "ana")
registrados.registrar_usuario("paco", "paco")
registrados.registrar_usuario("juan", "juan")
# Añadimos algún usuario siguiendo a otro para pruebas
# Ana sigue a paco y juan, debe ver sus mensajes
registrados.seguir_usuario("ana", "paco")
registrados.seguir_usuario("ana", "juan")
# Paco sigue a juan, debe ver sus mensajes
registrados.seguir_usuario("juan", "paco")
logueados = admindata.Logueados()

# Implementar las funciones definidas en twitter.proto. 
# Estas funciones son métodos de la clase TwitterServicer, que hereda de la clase generada por el compilador gRPC
# El argumento context no es necesario usarlo en nuestra práctica, pero es necesario incluirlo en la firma de la función
# El argumento request es el mensaje que envía el cliente cuando invoca la función remota, del formato definido en el archivo .proto
# Cada función remota debe retornar un mensaje de respuesta, que es el que recibe el cliente, del formato definido en el archivo .proto
# Una vez un usuario está logueado, el resto de acciones requieren que se compruebe en primer lugar el id session
class TwitterService(twitter_pb2_grpc.TwitterServicer):

    # Registrar un usuario nuevo si no existe el nombre de usuario ya registrado
    def Registrar(self, request, context):
        if registrados.existe_usuario(request.user):
            error: int32 = 1

        else:
            registrados.registrar_usuario(request.user, request.password)
            error: int32 = 0
        return twitter_pb2.RegistrarReply(error=error)


        # Verificar si el usuario ya está registrado
        # Error 1: Usuario ya existe



    # Iniciar sesión de un usuario si el nombre de usuario y contraseña son correctos    
    def Login(self, request, context):
        # Verificar si el usuario está registrado
        # Error 1: Usuario no existe
        if registrados.comprobar_credenciales(request.user, request.password) == None:
            error: int32 =1
        elif not registrados.comprobar_credenciales(request.user, request.password) :
            error: int32 =2
        else:
            if logueados.comprobar_logueado(user=request.user):
                sesion_id=logueados.regenerar_sesion(user=request.user)
                error: int32 = 0
                print("Sesion renovada")
            else:
                error: int32 = 0
                sesion_id =logueados.loguear_usuario(user=request.user)

        return twitter_pb2.LoginReply(error=error, session=sesion_id)
        
        # Verificar la contraseña del usuario
        # Error 2: Contraseña incorrecta
        
        # Verificar si el usuario ya está logueado. Regenerar session si ya está logueado. Sino loguear usuario
        

    # Cerrar sesión de un usuario    
    def Logout(self, request, context):
        if logueados.comprobar_logueado(request.user):
            logueados.cerrar_sesion(request.user)
            print("Sesion cerrada")
        else:
            print("No estas logueado")
        return twitter_pb2.Void()


    

    # Devolver una lista de los usuarios registrados
    def VerUsuarios(self, request, context):
        if logueados.comprobar_sesion(request.user, request.session):
            respuesta = registrados.ver_usuarios(request.user)
            return twitter_pb2.VerUsuariosReply(user=respuesta)
        else:
            print("No estas logueado")
            return None
        # Verificar si el usuario está conectado y la session es correcta

        print("Funcionalidad no implementada")




    # Añadir un nuevo usuario a la lista de suguiendo de un usuario
    def Seguir(self, request, context):
        # Verificar si el usuario está conectado y la session es correcta
        if logueados.comprobar_sesion(request.user, request.session):
            # Verificar si el usuario a seguir existe
            if registrados.existe_usuario(request.user_to_follow):
                seguidos = registrados.ver_siguiendo(request.user)
                # Verificar si el usuario ya está siguiendo al usuario a seguir
                if request.user_to_follow not in seguidos:
                    # Añadir el usuario a la lista de siguiendo
                    registrados.seguir_usuario(request.user, request.user_to_follow)
                    error:int32 = 0
                else:
                    # Error 2: Usuario ya está siguiendo al usuario a seguir
                    error:int32 = 2
            else:
                # Error 1: Usuario a seguir no existe
                error: int32 = 1
        return twitter_pb2.SeguirReply(error=error)

        

    # Quitar un usuario de la lista siguiendo de un usuario 
    def DejarSeguir(self, request, context):
        # Verificar si el usuario está conectado y la session es correcta
        if logueados.comprobar_sesion(request.user, request.session):
            if registrados.existe_usuario(request.user_to_follow):
                seguidos = registrados.ver_siguiendo(request.user)
                # Verificar si el usuario ya está siguiendo al usuario a seguir
                if request.user_to_follow in seguidos:
                    registrados.dejar_seguir_usuario(request.user, request.user_to_follow)
                    error: int32 = 0
                #Si no lo esta siguiendo no hacemos nada
                else:
                    # Error 2: Usuario ya está siguiendo al usuario a seguir
                    error: int32 = 0
            else:
                # Error 1: Usuario a seguir no existe
                error: int32 = 1
        return twitter_pb2.SeguirReply(error=error)



    # Devolver una lista de usuarios que está siguiendo el usuario request.user
    def VerSeguidos(self, request, context):
        # Verificar si el usuario está conectado y la session es correcta
        #PREGUNTAR
        if logueados.comprobar_sesion(request.user, request.session):
            seguidos = registrados.ver_siguiendo(request.user)

            return twitter_pb2.VerSeguidosReply(user=seguidos)


        


    # Registrar un tuit en la lista de mensajes pendientes de enviar en función de los seguidores del usuario
    def EnviarTuit(self, request, context):
        # Verificar si el usuario está conectado y la session es correcta
        if logueados.comprobar_sesion(request.user, request.session):
            # Posteriormente registrar el mensaje pasando la lista de seguidores
            seguidores = registrados.ver_seguidores(request.user)
            logueados.registrar_mensaje(user=request.user,mensaje=request.tuit.mensaje,destinatarios=seguidores)
        print("tweet enviado")
        return twitter_pb2.Void()
    
    
    # Recibir tuits pendientes
    def RecibirTuits(self, request, context):
        # Verificar si el usuario está conectado y la session es correcta
        if logueados.comprobar_sesion(request.user, request.session):
            logueados.registrar_mensaje("paco", "hola mundo", registrados.ver_seguidores("paco"))
            logueados.registrar_mensaje("juan", "hola mundo", registrados.ver_seguidores("juan"))
            logueados.registrar_mensaje("ana", "hola mundo", registrados.ver_seguidores("ana"))
            logueados.registrar_mensaje("ana", "mensaje2", registrados.ver_seguidores("ana"))
            logueados.registrar_mensaje("juan", "hola mundo2", registrados.ver_seguidores("juan"))
            lista = logueados.recibir_mensajes(request.user)
            tuits = []
            for fila in lista.iterrows():
                user= fila[1]['user']
                mensaje= fila[1]['mensaje']
                tuit = twitter_pb2.Tuit(user=user, mensaje=mensaje)
                tuits.append(tuit)

            return twitter_pb2.RecibirTuitsReply(tuit=tuits)
        print("Hola")

        # Leer la lista de listas con los mensajes pendientes construir el Reply como lista de twitter_pb2.Tuit
        print("Funcionalidad no implementada")

        


# Función para iniciar el servidor
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    twitter_pb2_grpc.add_TwitterServicer_to_server(TwitterService(), server) 
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado")
    while True:
        print("""Menu:
              1. Mostrar usuarios registrados
              2. Mostrar usuarios conectados
              3. Mostrar mensajes pendientes de enviar
              4: Salir
              Este menú está siempre disponible aunque se muestren mensajes de log""")
        opcion = input("")
        match opcion:
            case "1":
                print("*** USUARIOS REGISTRADOS ***")
                registrados.mostrar_registrados()
            case "2":
                print("*** USUARIOS CONECTADOS ***")
                logueados.mostrar_logueados()
            case "3":
                print("*** MENSAJES PENDIENTES DE ENVIAR ***")
                logueados.mostrar_mensajes()
            case "4":
                server.stop(0)
                break
            case _:
                print("Opción no válida")

if __name__ == '__main__':
    try:
        serve()
    except KeyboardInterrupt:
        print("Servidor detenido")