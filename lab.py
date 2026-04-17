import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# 1. Autenticacion usando el archivo JSON
cred = credentials.Certificate('credentials/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# 2. Instanciar el cliente de Firestore
db = firestore.client()
print("Conexion a Firestore establecida correctamente.")


def agregar_muestra(nombre, descripcion):  # CREATE
    try:
        datos_muestra = {
            'nombre': nombre,
            'descripcion': descripcion,
            'fecha_registro': datetime.now(timezone.utc),
            'estado': 'pendiente'
        }

        update_time, doc_ref = db.collection('muestras').add(datos_muestra)
        print(f"Muestra agregada con exito. ID asignado: {doc_ref.id}")

    except Exception as e:
        print(f"Error al agregar la muestra: {e}")


def leer_muestras():  # READ
    print("\n--- Listado de Muestras Registradas ---")
    try:
        docs = db.collection('muestras').order_by('fecha_registro').stream()
        contador = 0

        for doc in docs:
            data = doc.to_dict()
            print(f"ID: {doc.id} | Nombre: {data.get('nombre', 'N/A')} | Estado: {data.get('estado', 'N/A')}")
            contador += 1

        if contador == 0:
            print("No hay muestras registradas actualmente.")

    except Exception as e:
        print(f"Error al leer las muestras: {e}")


def actualizar_muestra(doc_id, nuevos_datos):  # UPDATE
    try:
        doc_ref = db.collection('muestras').document(doc_id)
        doc_ref.update(nuevos_datos)
        print(f"Muestra {doc_id} actualizada correctamente.")
    except Exception as e:
        print(f"Error al actualizar (Seguro que el ID existe?): {e}")


def borrar_muestra(doc_id):  # DELETE
    try:
        doc_ref = db.collection('muestras').document(doc_id)
        doc_ref.delete()
        print(f"Muestra {doc_id} eliminada definitivamente.")
    except Exception as e:
        print(f"Error al intentar borrar: {e}")


def menu():
    while True:
        print("\n" + "=" * 30)
        print("GESTOR DE LABORATORIO V1")
        print("=" * 30)
        print("1. Agregar nueva muestra")
        print("2. Listar todas las muestras")
        print("3. Cambiar estado ")
        print("4. Borrar una muestra")
        print("5. Salir")

        opcion = input("\nSeleccione una opcion (1-5): ")

        if opcion == "1":
            nombre = input("Ingrese el nombre de la muestra: ").strip()
            if not nombre:
                print("El nombre no puede estar vacio.")
                continue
            descripcion = input("Ingrese la descripcion: ")
            agregar_muestra(nombre, descripcion)

        elif opcion == "2":
            leer_muestras()

        elif opcion == "3":
            leer_muestras()
            doc_id = input("\nCopie y pegue el ID de la muestra a actualizar: ").strip()
            estado = input("\nIntroduzca el nuevo estado: ").strip()
            actualizar_muestra(doc_id, {'estado': estado})

        elif opcion == "4":
            leer_muestras()
            doc_id = input("\nCopie y pegue el ID de la muestra a BORRAR: ").strip()
            confirmacion = input("Esta seguro? (s/n): ").lower()
            if confirmacion == 's':
                borrar_muestra(doc_id)

        elif opcion == "5":
            print("Saliendo del gestor...")
            break

        else:
            print("Opcion no valida. Intente nuevamente.")




























if __name__ == "__main__":
    menu()
