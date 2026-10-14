# main.py es la VISTA del sistema académico: lo único que habla con el usuario.
# No valida ni guarda nada: le pide todo a los controladores de views_academico.py
# y solo muestra lo que ellos responden.
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views_academico import (
    EstudianteController, DocenteController, MateriaController, MatriculaController
)


class Menu:

    def __init__(self):
        # Se crea UN solo controlador de cada tipo.
        # A materias y matrículas se les pasan los MISMOS que usa el menú.
        self.estudiantes = EstudianteController()
        self.docentes = DocenteController()
        self.materias = MateriaController(self.docentes)
        self.matriculas = MatriculaController(self.estudiantes, self.materias)

    # ---------- ayudas ----------
    def pausa(self):
        input("\nPresione Enter para continuar...")

    def pedir_entero(self, texto):
        try:
            return int(input(texto))
        except ValueError:
            return None

    def mostrar_resultado(self, exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    # ---------- menú principal ----------
    def ejecutar(self):
        while True:
            imprimir_titulo("SISTEMA ACADÉMICO")
            print("  1. Estudiantes")
            print("  2. Docentes")
            print("  3. Materias")
            print("  4. Matrículas")
            print("  5. Reporte general")
            print("  6. Estudiantes reprobados")
            print("  0. Salir\n")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self.menu_crud(self.estudiantes)
            elif opcion == "2":
                self.menu_crud(self.docentes)
            elif opcion == "3":
                self.menu_crud(self.materias)
            elif opcion == "4":
                self.menu_crud(self.matriculas)
            elif opcion == "5":
                self.reporte_general()
            elif opcion == "6":
                self.ver_reprobados()
            elif opcion == "0":
                imprimir_info("¡Hasta luego! 👋")
                break
            else:
                imprimir_error("Opción no válida")
                self.pausa()

    # ---------- menú de cada controlador ----------
    # El mismo menú sirve para las 4 entidades,
    # porque los 4 controladores tienen los mismos métodos.
    def menu_crud(self, controlador):
        titulo = controlador.nombre.upper() + "S"

        while True:
            imprimir_titulo(titulo)
            print(f"  1. Crear {controlador.nombre}")
            print("  2. Ver todos")
            print("  3. Buscar")
            print("  4. Ver por id")
            print("  5. Actualizar")
            print("  6. Eliminar")
            if controlador == self.matriculas:
                print("  7. Agregar nota")
                print("  8. Ver boletín")
            if controlador == self.docentes:
                print("  7. Ver materias del docente")
            print("  0. Volver\n")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self.crear(controlador)
            elif opcion == "2":
                self.ver_todos(controlador)
            elif opcion == "3":
                self.buscar(controlador)
            elif opcion == "4":
                self.ver_por_id(controlador)
            elif opcion == "5":
                self.actualizar(controlador)
            elif opcion == "6":
                self.eliminar(controlador)
            elif opcion == "7" and controlador == self.matriculas:
                self.agregar_nota()
            elif opcion == "8" and controlador == self.matriculas:
                self.ver_boletin()
            elif opcion == "7" and controlador == self.docentes:
                self.materias_de_docente()
            elif opcion == "0":
                break
            else:
                imprimir_error("Opción no válida")
                self.pausa()

    # ---------- operaciones ----------
    def crear(self, controlador):
        imprimir_titulo(f"CREAR {controlador.nombre.upper()}")
        datos = {}
        for campo in controlador.campos:
            datos[campo] = input(f"{campo.capitalize()}: ")

        exito, mensaje = controlador.crear(datos)
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def ver_todos(self, controlador):
        imprimir_titulo(controlador.nombre.upper() + "S")
        lista = controlador.leer()
        if len(lista) == 0:
            imprimir_info("No hay registros todavía.")
        else:
            for objeto in lista:
                print(f"  {objeto}")
            imprimir_info(f"Total: {len(lista)}")
        self.pausa()

    def buscar(self, controlador):
        imprimir_titulo(f"BUSCAR {controlador.nombre.upper()}")
        texto = input("Buscar: ")
        encontrados = controlador.buscar(texto)
        if len(encontrados) == 0:
            imprimir_info(f"Sin coincidencias para '{texto}'.")
        else:
            for objeto in encontrados:
                print(f"  {objeto}")
        self.pausa()

    def ver_por_id(self, controlador):
        imprimir_titulo(f"VER {controlador.nombre.upper()}")
        id_registro = self.pedir_entero("Id: ")
        objeto = controlador.obtener(id_registro)
        if objeto is None:
            imprimir_error("No encontrado")
        else:
            for clave, valor in objeto.a_diccionario().items():
                print(f"  {clave.capitalize()}: {valor}")
        self.pausa()

    def actualizar(self, controlador):
        imprimir_titulo(f"ACTUALIZAR {controlador.nombre.upper()}")
        id_registro = self.pedir_entero("Id: ")
        objeto = controlador.obtener(id_registro)
        if objeto is None:
            imprimir_error("No encontrado")
            self.pausa()
            return

        imprimir_info(f"Editando: {objeto.etiqueta()}")
        print("Deje en blanco lo que no quiera cambiar.\n")
        cambios = {}
        for campo in controlador.campos:
            actual = getattr(objeto, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo != "":
                cambios[campo] = nuevo

        exito, mensaje = controlador.actualizar(id_registro, cambios)
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def eliminar(self, controlador):
        imprimir_titulo(f"ELIMINAR {controlador.nombre.upper()}")
        id_registro = self.pedir_entero("Id: ")
        objeto = controlador.obtener(id_registro)
        if objeto is None:
            imprimir_error("No encontrado")
            self.pausa()
            return

        imprimir_info(f"Se eliminará: {objeto.etiqueta()}")
        if confirmar("¿Confirma?"):
            exito, mensaje = controlador.eliminar(id_registro)
            self.mostrar_resultado(exito, mensaje)
        else:
            imprimir_info("Operación cancelada")
        self.pausa()

    # ---------- solo para matrículas ----------
    def agregar_nota(self):
        imprimir_titulo("AGREGAR NOTA")
        id_matricula = self.pedir_entero("Id de la matrícula: ")
        if id_matricula is None:
            imprimir_error("El id debe ser un número")
            self.pausa()
            return

        tipo = input("Tipo (deber / lección / examen): ")
        valor = input("Nota (0 a 20): ")
        peso = input("Peso (Enter = 1): ").strip() or 1

        exito, mensaje = self.matriculas.agregar_nota(id_matricula, tipo, valor, peso)
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def ver_boletin(self):
        imprimir_titulo("BOLETÍN")
        estudiante_id = self.pedir_entero("Id del estudiante: ")
        texto = self.matriculas.boletin(estudiante_id)
        if texto is None:
            imprimir_error("No existe ese estudiante")
        else:
            print(texto)
        self.pausa()

    # ---------- solo para docentes ----------
    def materias_de_docente(self):
        imprimir_titulo("MATERIAS DEL DOCENTE")
        docente_id = self.pedir_entero("Id del docente: ")
        docente = self.docentes.obtener(docente_id)
        if docente is None:
            imprimir_error("No existe ese docente")
        else:
            imprimir_info(docente.etiqueta())
            materias = self.materias.materias_de_docente(docente_id)
            if len(materias) == 0:
                print("  No tiene materias asignadas")
            for materia in materias:
                print(f"  {materia}")
        self.pausa()

    # ---------- reportes ----------
    def reporte_general(self):
        # POLIMORFISMO: el mismo bucle sirve para los 4 controladores.
        # Cada objeto se imprime distinto porque cada modelo tiene su etiqueta().
        imprimir_titulo("REPORTE GENERAL")
        for controlador in (self.estudiantes, self.docentes,
                            self.materias, self.matriculas):
            print(f"=== {controlador.nombre.upper()}S ({len(controlador.leer())}) ===")
            for objeto in controlador.leer():
                print(f"  {objeto}")
            print()
        self.pausa()

    def ver_reprobados(self):
        imprimir_titulo("ESTUDIANTES REPROBADOS")
        reprobados = self.matriculas.reprobados()
        if len(reprobados) == 0:
            imprimir_info("No hay estudiantes reprobados")
        else:
            for estudiante, materia, promedio in reprobados:
                print(f"  {estudiante:<25} {materia:<20} {promedio}")
            imprimir_info(f"Total: {len(reprobados)}")
        self.pausa()


# Solo arranca si se ejecuta "python main.py"
if __name__ == "__main__":
    try:
        Menu().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")