from models import Compra
from views import CrudBase
from shared.json_manager import GestorJSON








class CompraController(CrudBase):

    def __init__(self, proveedores, productos, archivo="data/compras.json"):
        self.nombre = "compra"
        self.campos = Compra.CAMPOS
        self.gestor = GestorJSON(archivo)

        # La compra USA los controladores de proveedores y productos.
        # Hay que pasarle los MISMOS que usa el menú.
        self.proveedores = proveedores
        self.productos = productos

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Compra.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for compra in self.lista:
            datos.append(compra.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_compra):
        for compra in self.lista:
            if compra.id == id_compra:
                return compra
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        # Las compras se buscan por fecha, ej: "2026-10"
        texto = texto.strip()
        encontrados = []
        if texto == "":
            return encontrados

        for compra in self.lista:
            if texto in compra.fecha:
                encontrados.append(compra)
        return encontrados

    def siguiente(self):
        mayor = 0
        for compra in self.lista:
            if compra.id > mayor:
                mayor = compra.id
        return mayor + 1

    def crear(self, datos):
        # datos = {"proveedor_id": 1, "items": [{"producto_id": 2, "cantidad": 3}, ...]}
        try:
            proveedor_id = int(datos.get("proveedor_id", 0))
        except (TypeError, ValueError):
            return False, "El proveedor_id debe ser un número"

        if self.proveedores.obtener(proveedor_id) is None:
            return False, f"No existe un proveedor con id {proveedor_id}"

        items = datos.get("items", [])
        if len(items) == 0:
            return False, "La compra debe tener al menos un producto"

        # Revisamos TODOS los productos antes de vender: si uno falla, no se vende nada
        ids_vistos = []
        for item in items:
            producto = self.productos.obtener(item["producto_id"])
            if producto is None:
                return False, f"No existe producto con id {item['producto_id']}"
            if producto.id in ids_vistos:
                return False, f"El producto {producto.nombre} está repetido en la compra"
            if not producto.hay_stock(item["cantidad"]):
                return False, (f"Stock insuficiente de {producto.nombre}: "
                               f"hay {producto.stock}, piden {item['cantidad']}")
            ids_vistos.append(producto.id)

        # Todo bien: armamos la compra y descontamos el stock
        compra = Compra(self.siguiente(), proveedor_id, datos.get("fecha", ""))
        for item in items:
            producto = self.productos.obtener(item["producto_id"])
            compra.agregar_detalle(producto, item["cantidad"])
            producto.descontar_stock(item["cantidad"])
        self.productos.guardar()          # guarda el stock nuevo en productos.json

        self.lista.append(compra)
        self.guardar()                    # guarda la compra en compras.json
        return True, f"Compra {compra.id} registrada por ${compra.total:.2f}"

    def actualizar(self, id_compra, datos):
        # Una compra ya registrada no se modifica (como una factura real)
        return False, "Las compras registradas no se pueden modificar"

    def eliminar(self, id_compra):
        compra = self.obtener(id_compra)
        if compra is None:
            return False, f"No existe compra con id {id_compra}"

        self.lista.remove(compra)
        self.guardar()
        return True, f"Compra {id_compra} eliminada"

    # --- métodos propios de compras ---
    def factura(self, id_compra):
        compra = self.obtener(id_compra)
        if compra is None:
            return None

        proveedor = self.proveedores.obtener(compra.proveedor_id)
        if proveedor is None:
            nombre_proveedor = "eliminado"
        else:
            nombre_proveedor = proveedor.nombre_completo

        texto = f"FACTURA #{compra.id}   fecha: {compra.fecha}\n"
        texto += f"Proveedor: {nombre_proveedor}\n"
        texto += "-" * 46 + "\n"
        for detalle in compra.detalles:
            texto += f"  {detalle}\n"
        texto += "-" * 46 + "\n"
        texto += f"  TOTAL: ${compra.total:.2f}  ({compra.cantidad_items} ítems)"
        return texto

    def compras_de_proveedor(self, proveedor_id):
        resultado = []
        for compra in self.lista:
            if compra.proveedor_id == proveedor_id:
                resultado.append(compra)
        return resultado
