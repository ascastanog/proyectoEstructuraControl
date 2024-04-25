import grpc
import twitter_pb2
import twitter_pb2_grpc

# Menu de opciones inicial para registrarse y loguearse
def menu_inicial():
    while True:
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = int(input("Ingrese opción: "))
        if opcion < 1 or opcion > 3:
            print("Opción inválida")
        else:
            return opcion

# Menú una vez estás logueado
def menu_logueado():
    while True:
        print("1. Ver usuarios registrados")
        print("2. Seguir a un usuario")
        print("3. Dejar de seguir a un usuario")
        print("4. Ver usuarios seguidos")
        print("5. Enviar tuit")
        print("6. Recibir tuits pendientes")
        print("7. Salir")
        opcion = int(input("Ingrese opción: "))
        if opcion < 1 or opcion > 7:
            print("Opción inválida")
        else:
            return opcion

# Implementar las funciones del cliente por separado
# Cada función recibe el stub, solicita al usuario los datos necesarios, invoca la función remota y muestra el resultado
def registrar_usuario(stub):

    print("Funcionalidad no implementada")
    # Preguntar el usuario y la contraseña
    # Llamar a la función remota Registrar
    request = twitter_pb2.ReguistrarRequest(user=usuario, password=)
    respuesta = stub.Registrar(request)
    respuesta.error
    # Mostrar un mensaje de error si el usuario ya existe


def iniciar_sesion(stub):
    # Preguntar el usuario y la contraseña
    # Llamar a la función remota Login
    # Debe retornar el usuario y la sesión si el login es exitoso o None, None en caso contrario
    # Debe mostrar un mensaje de error si el usuario no existe o la contraseña es incorrecta
    print("Funcionalidad no implementada")

# El resto de funciones deben recibir como parámetros el stub, user y session
def cerrar_sesion(stub, user, session):
    # Llamar a la función remota Logout
    print("Funcionalidad no implementada")


def ver_usuarios_registrados(stub, user, session):
    print("Funcionalidad no implementada")
    #Imprimitr los usuarios registrados menos el propio usuario

def seguir_usuario(stub, user, session):
    print("Funcionalidad no implementada")
    # Preguntar el usuario a seguir
    # Llamar a la función Seguir con el usuario introducido por parámetro
    # Mostrar los mensajes de error según el reply


def dejar_seguir_usuario(stub, user, session):
    print("Funcionalidad no implementada")
    # Preguntar el usuario a dejar de seguir
    # Llamar a la función DejarSeguir con el usuario introducido por parámetro
    # Mostrar los mensajes de error según el reply

def ver_usuarios_seguidos(stub, user, session):
    print("Funcionalidad no implementada")
    # Mostrar los usuarios seguidos por el usuario

def enviar_tuit(stub, user, session):
    # Preguntar el mensaje del tuit
    # Enviar el tuit usando el procedimiento remoto
    print("Funcionalidad no implementada")
    

def recibir_tuits(stub, user, session):
    # Recibir los tuits pendientes invocando al procedimiento remoto
    # Mostrar los tuits recibidos en formato "usuario: mensaje"
    print("Funcionalidad no implementada")                
        

# Función principal. Abre el canal y ejecuta las opciones del menú hasta que se elija la opción de salir.
def main():
    # Iniciar un canal grpc
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crear un stub
        stub = twitter_pb2_grpc.TwitterStub(channel)
        user = None
        session = None

        # Mostrar el menú inicial        
        while True:
            opcion = menu_inicial()
            match opcion:
                case 1:
                    registrar_usuario(stub)
                case 2:
                    user, session = iniciar_sesion(stub)
                    if session != None:
                        break
                case 3:
                    return None
                    
        # Una vez logueado, mostrar el menú de opciones
        while True:
            opcion = menu_logueado()
            match opcion:
                case 1:
                    ver_usuarios_registrados(stub, user, session)
                case 2:
                    seguir_usuario(stub, user, session)
                case 3:
                    dejar_seguir_usuario(stub, user, session)
                case 4:
                    ver_usuarios_seguidos(stub, user, session)
                case 5:
                    enviar_tuit(stub, user, session)
                case 6:
                    recibir_tuits(stub, user, session)
                case 7:
                    cerrar_sesion(stub, user, session)
                    return None  

        

if __name__ == '__main__':
    main()