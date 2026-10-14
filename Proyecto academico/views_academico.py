
import os

from models_academico import Estudiante , Docente , Materia , Matricula
from views import CrudBase
from shared.json_manager import GestorJSON

BASE = os.path.dirname(os.path.abspath(__file__))


class EstudianteController(CrudBase):

    def __init__(self, archivo=os.path.join(BASE, "data", "estudiantes.json")):
        self.nombre = "estudiante"
        self.campos = Estudiante.CAMPOS
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_estudiante):
        for estudiante in self.lista:
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for estudiante in self.lista:
            if (texto in estudiante.nombre.lower()
                    or texto in estudiante.apellido.lower()
                    or texto in estudiante.email
                    or texto in estudiante.carnet.lower()):
                encontrados.append(estudiante)
        return encontrados

    def siguiente(self):
        mayor = 0
        for estudiante in self.lista:
            if estudiante.id > mayor:
                mayor = estudiante.id
        return mayor + 1

    def crear(self, datos):
        carnet = str(datos.get("carnet", "")).strip().upper()
        for estudiante in self.lista:
            if estudiante.carnet == carnet:
                return False, f"El carnet {carnet} ya está registrado"

        try:
            estudiante = Estudiante(self.siguiente(),
                                    datos.get("nombre", ""),
                                    datos.get("apellido", ""),
                                    datos.get("email", ""),
                                    datos.get("carnet", ""))
        except ValueError as error:
            return False, str(error)

        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_estudiante, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe estudiante con id {id_estudiante}"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            for otro in self.lista:
                if otro.carnet == carnet and otro.id != id_estudiante:
                    return False, f"El carnet {carnet} ya está registrado"

        try:
            nuevo = Estudiante(estudiante.id,
                               datos.get("nombre", estudiante.nombre),
                               datos.get("apellido", estudiante.apellido),
                               datos.get("email", estudiante.email),
                               datos.get("carnet", estudiante.carnet))
        except ValueError as error:
            return False, str(error)

        posicion = self.lista.index(estudiante)
        self.lista[posicion] = nuevo
        self.guardar()
        return True, f"Estudiante {id_estudiante} actualizado"

    def eliminar(self, id_estudiante):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe estudiante con id {id_estudiante}"

        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado"


#===========================================================================

#===========================================================================

#===========================================================================

class DocenteController(CrudBase):

    def __init__(self, archivo=os.path.join(BASE, "data", "docentes.json")):
        self.nombre = "docente"
        self.campos = Docente.CAMPOS
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Docente.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for docente in self.lista:
            datos.append(docente.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_docente):
        for docente in self.lista:
            if docente.id == id_docente:
                return docente
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for docente in self.lista:
            if (texto in docente.nombre.lower()
                    or texto in docente.apellido.lower()
                    or texto in docente.email
                    or texto in docente.especialidad.lower()):
                encontrados.append(docente)
        return encontrados

    def siguiente(self):
        mayor = 0
        for docente in self.lista:
            if docente.id > mayor:
                mayor = docente.id
        return mayor + 1

    def crear(self, datos):
        email = str(datos.get("email", "")).strip().lower()
        for docente in self.lista:
            if docente.email == email:
                return False, f"El email {email} ya está registrado"

        try:
            docente = Docente(self.siguiente(),
                datos.get("nombre", ""),
                datos.get("apellido", ""),
                datos.get("email", ""),
                datos.get("titulo", ""),
                datos.get("especialidad", ""))
                            
        except ValueError as error:
            return False, str(error)

        self.lista.append(docente)
        self.guardar()
        return True, f"docente creado: {docente.etiqueta()}"

    def actualizar(self, id_docente, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        docente = self.obtener(id_docente)
        if docente is None:
            return False, f"No existe docente con id {id_docente}"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            for otro in self.lista:
                if otro.email == email and otro.id != id_docente:
                    return False, f"El email {email} ya está registrado"

        try:
            nuevo = Docente(docente.id,
                        datos.get("nombre", docente.nombre),
                        datos.get("apellido", docente.apellido),
                        datos.get("email", docente.email),
                        datos.get("titulo", docente.titulo),
                        datos.get("especialidad", docente.especialidad)),
        except ValueError as error:
            return False, str(error)

        posicion = self.lista.index(docente)
        self.lista[posicion] = nuevo
        self.guardar()
        return True, f"docente {id_docente} actualizado"

    def eliminar(self, id_docente):
        docente = self.obtener(id_docente)
        if docente is None:
            return False, f"No existe docente con id {id_docente}"

        self.lista.remove(docente)
        self.guardar()
        return True, f"docente {id_docente} eliminado"

    #===========================================================================

#===========================================================================

#===========================================================================

class MateriaController(CrudBase):

    def __init__(self, docentes, archivo=os.path.join(BASE, "data", "materias.json")):
        self.nombre = "materia"
        self.campos = Materia.CAMPOS
        self.gestor = GestorJSON(archivo)

        # La materia USA el controlador de docentes para revisar que existan
        self.docentes = docentes

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_materia):
        for materia in self.lista:
            if materia.id == id_materia:
                return materia
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for materia in self.lista:
            if (texto in materia.nombre.lower()
                    or texto in materia.codigo.lower()):
                encontrados.append(materia)
        return encontrados

    def siguiente(self):
        mayor = 0
        for materia in self.lista:
            if materia.id > mayor:
                mayor = materia.id
        return mayor + 1

    def docente_existe(self, docente_id):
        """Si viene vacío, está bien (materia sin docente). Si viene, debe existir."""
        if str(docente_id).strip() in ("", "0", "None"):
            return True
        try:
            return self.docentes.obtener(int(docente_id)) is not None
        except ValueError:
            return False

    def crear(self, datos):
        codigo = str(datos.get("codigo", "")).strip().upper()
        for materia in self.lista:
            if materia.codigo == codigo:
                return False, f"El código {codigo} ya está registrado"

        if not self.docente_existe(datos.get("docente_id", "")):
            return False, f"No existe un docente con id {datos.get('docente_id')}"

        try:
            materia = Materia(self.siguiente(),
                              datos.get("nombre", ""),
                              datos.get("codigo", ""),
                              datos.get("creditos", 0),
                              datos.get("docente_id", None))
        except ValueError as error:
            return False, str(error)

        self.lista.append(materia)
        self.guardar()
        return True, f"Materia creada: {materia.etiqueta()}"

    def actualizar(self, id_materia, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe materia con id {id_materia}"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            for otra in self.lista:
                if otra.codigo == codigo and otra.id != id_materia:
                    return False, f"El código {codigo} ya está registrado"

        if "docente_id" in datos and not self.docente_existe(datos["docente_id"]):
            return False, f"No existe un docente con id {datos['docente_id']}"

        try:
            nueva = Materia(materia.id,
                            datos.get("nombre", materia.nombre),
                            datos.get("codigo", materia.codigo),
                            datos.get("creditos", materia.creditos),
                            datos.get("docente_id", materia.docente_id))
        except ValueError as error:
            return False, str(error)

        posicion = self.lista.index(materia)
        self.lista[posicion] = nueva
        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe materia con id {id_materia}"

        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"

    # --- métodos propios de materias ---
    def asignar_docente(self, id_materia, docente_id):
        return self.actualizar(id_materia, {"docente_id": docente_id})

    def materias_de_docente(self, docente_id):
        resultado = []
        for materia in self.lista:
            if materia.docente_id == docente_id:
                resultado.append(materia)
        return resultado

#===========================================================================

#===========================================================================

#===========================================================================

class MatriculaController(CrudBase):
    """El equivalente académico del VentaController."""

    def __init__(self, estudiantes, materias,
                archivo=os.path.join(BASE, "data", "matriculas.json")):
        self.nombre = "matrícula"
        self.campos = Matricula.CAMPOS
        self.gestor = GestorJSON(archivo)

        # La matrícula USA los controladores de estudiantes y materias
        self.estudiantes = estudiantes
        self.materias = materias

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_matricula):
        for matricula in self.lista:
            if matricula.id == id_matricula:
                return matricula
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        # Las matrículas se buscan por periodo, ej: "2026-1"
        texto = texto.strip()
        encontrados = []
        if texto == "":
            return encontrados

        for matricula in self.lista:
            if texto in matricula.periodo:
                encontrados.append(matricula)
        return encontrados

    def siguiente(self):
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def validar(self, estudiante_id, materia_id, periodo, id_actual=None):
        """Revisa las 3 reglas. Devuelve un mensaje de error, o None si todo está bien."""
        if self.estudiantes.obtener(estudiante_id) is None:
            return f"No existe un estudiante con id {estudiante_id}"
        if self.materias.obtener(materia_id) is None:
            return f"No existe una materia con id {materia_id}"

        for otra in self.lista:
            if (otra.estudiante_id == estudiante_id
                    and otra.materia_id == materia_id
                    and otra.periodo == periodo
                    and otra.id != id_actual):
                return "El estudiante ya está matriculado en esa materia y periodo"
        return None

    def crear(self, datos):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return False, "Los ids de estudiante y materia deben ser números"

        # El modelo pone "2026-1" si el periodo viene vacío; comparamos igual
        periodo = str(datos.get("periodo", "")).strip() or "2026-1"

        error = self.validar(estudiante_id, materia_id, periodo)
        if error:
            return False, error

        matricula = Matricula(self.siguiente(), estudiante_id, materia_id, periodo)
        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula creada: {matricula.etiqueta()}"

    def actualizar(self, id_matricula, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe matrícula con id {id_matricula}"

        try:
            estudiante_id = int(datos.get("estudiante_id", matricula.estudiante_id))
            materia_id = int(datos.get("materia_id", matricula.materia_id))
        except (TypeError, ValueError):
            return False, "Los ids de estudiante y materia deben ser números"
        periodo = str(datos.get("periodo", matricula.periodo)).strip() or "2026-1"

        error = self.validar(estudiante_id, materia_id, periodo, id_actual=id_matricula)
        if error:
            return False, error

        # Las notas se conservan: pasan tal cual a la matrícula nueva
        nueva = Matricula(matricula.id, estudiante_id, materia_id, periodo,
                          list(matricula.notas))
        posicion = self.lista.index(matricula)
        self.lista[posicion] = nueva
        self.guardar()
        return True, f"Matrícula {id_matricula} actualizada"

    def eliminar(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe matrícula con id {id_matricula}"

        # Composición: al borrar la matrícula, sus notas se van con ella
        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula {id_matricula} eliminada"

    # --- métodos propios de matrículas ---
    def agregar_nota(self, id_matricula, tipo, valor, peso=1):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe matrícula con id {id_matricula}"

        try:
            nota = matricula.agregar_nota(tipo, valor, peso)
        except ValueError as error:
            return False, str(error)

        self.guardar()      # sin esto, la nota se pierde al cerrar el programa
        return True, f"Nota agregada ({nota}). Promedio: {matricula.promedio}"

    def matriculas_de_estudiante(self, estudiante_id):
        resultado = []
        for matricula in self.lista:
            if matricula.estudiante_id == estudiante_id:
                resultado.append(matricula)
        return resultado

    def boletin(self, estudiante_id):
        estudiante = self.estudiantes.obtener(estudiante_id)
        if estudiante is None:
            return None

        matriculas = self.matriculas_de_estudiante(estudiante_id)

        texto = f"BOLETÍN DE {estudiante.nombre_completo.upper()}\n"
        texto += f"Carnet: {estudiante.carnet}\n"
        texto += "-" * 50 + "\n"

        if len(matriculas) == 0:
            texto += "  No tiene materias matriculadas\n"
            texto += "-" * 50
            return texto

        suma = 0
        for matricula in matriculas:
            materia = self.materias.obtener(matricula.materia_id)
            if materia is None:
                nombre_materia = "materia eliminada"
            else:
                nombre_materia = materia.nombre
            texto += (f"  {nombre_materia:<20} {matricula.periodo:<8} "
                    f"{matricula.promedio:>6}  {matricula.estado}\n")
            suma += matricula.promedio

        general = round(suma / len(matriculas), 2)
        texto += "-" * 50 + "\n"
        texto += f"  PROMEDIO GENERAL: {general}"
        return texto




    def reprobados(self):
        """LISTA de tuplas (estudiante, materia, promedio) de las matrículas reprobadas."""
        resultado = []
        for matricula in self.lista:
            if matricula.estado == "Reprobado":
                estudiante = self.estudiantes.obtener(matricula.estudiante_id)
                materia = self.materias.obtener(matricula.materia_id)
                nombre_est = estudiante.nombre_completo if estudiante else "eliminado"
                nombre_mat = materia.nombre if materia else "eliminada"
                resultado.append((nombre_est, nombre_mat, matricula.promedio))
        return resultado