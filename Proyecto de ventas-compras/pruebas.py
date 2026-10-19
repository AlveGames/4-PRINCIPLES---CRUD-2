class mamawevo:


    # ---------- solo para compras ----------
    def crear_compra(self):
        imprimir_titulo("REGISTRAR VENTA")
        proveedor_id = self.pedir_entero("Id del proveedor: ")
        if proveedor_id is None:
            imprimir_error("El id debe ser un número")
            self.pausa()
            return

        imprimir_info("Productos disponibles:")
        for producto in self.productos.leer():
            print(f"  {producto}")

        # Se piden productos hasta que el usuario escriba 0
        items = []
        while True:
            producto_id = self.pedir_entero("\nId del producto (0 para terminar): ")
            if producto_id is None or producto_id == 0:
                break
            cantidad = self.pedir_entero("Cantidad: ")
            if cantidad is None or cantidad <= 0:
                imprimir_error("Cantidad inválida")
                continue
            items.append({"producto_id": producto_id, "cantidad": cantidad})

        exito, mensaje = self.compras.crear({"proveedor_id": proveedor_id, "items": items})
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def ver_orden(self):
        imprimir_titulo("FACTURA")
        id_compra = self.pedir_entero("Id de la compra: ")
        texto = self.compras.orden_compra(id_compra)
        if texto is None:
            imprimir_error("No existe esa compra")
        else:
            print(texto)
        self.pausa()