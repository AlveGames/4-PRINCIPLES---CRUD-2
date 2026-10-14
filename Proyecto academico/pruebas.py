from views_academico import *

e = EstudianteController()
d = DocenteController()
m = MateriaController(d)
mt = MatriculaController(e, m)

print(mt.crear({"estudiante_id": "1", "materia_id": "1"}))
print(mt.crear({"estudiante_id": "1", "materia_id": "1", "periodo": "2026-1"}))
print(mt.crear({"estudiante_id": "1", "materia_id": "2"}))
print(mt.crear({"estudiante_id": "9", "materia_id": "1"}))
print(mt.agregar_nota(1, "deber", 18))
print(mt.agregar_nota(1, "examen", 15, 2))
print(mt.agregar_nota(2, "examen", 10))
print(mt.agregar_nota(1, "tarea", 15))
print()
print(mt.boletin(1))