from tkinter import *
from tkinter import END, messagebox, ttk
from venta_modelo import actualizar_treeview, agregar, borrar, cargar_datos, verificar_id, update
from tkinter.font import Font


# ##############################################
# VISTA VENTANA PRINCIPAL
# ##############################################
class VentasListado:
    
    def __init__(self, window):
        self.window = window
        self.ventanaCentrada(1050, 500)  # Centrar ventana
        self.ventas_listado()  # Crear la interfaz

    def ventanaCentrada(self, ancho, alto):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        posX = (screen_width // 2) - (ancho // 2)
        posY = (screen_height // 2) - (alto // 2)
        self.window.geometry(f"{ancho}x{alto}+{int(posX)}+{int(posY)}")

    def ventas_listado(self):
        self.window.title("FERRETERIA - VENTAS REALIZADAS")
        bgcolor = "lightgrey"

        titulo_frame = Frame(self.window, bg="lightgrey")

        titulo_font = Font(family="Helvetica", size=14, weight="bold")
        subtitulo_font = Font(family="Helvetica", size=14, weight="bold")

        titulo = Label(self.window, text="VENTAS REALIZADAS", font=titulo_font, bd="10", bg=bgcolor)
        titulo.place(x=1, y=5, width=800, height=40)


        # frame marco izquierdo  treeview
        frame_treeview = Frame(self.window)
        frame_treeview.grid(row=1, column=0, padx=10, pady=10, sticky=N+S+E+W)

        # frame marco derecho  botones y menu
        frame_controls = Frame(self.window)
        frame_controls.grid(row=1, column=1, padx=10, pady=10, sticky=N+S)

        espacio_1 = Label(frame_treeview)
        espacio_1.grid(row=1)
        espacio_2 = Label(frame_treeview)
        espacio_2.grid(row=2)       
        espacio_3 = Label(frame_treeview)
        espacio_3.grid(row=3)
        espacio_4 = Label(frame_treeview)
        espacio_4.grid(row=4)        
        
        espacio_1 = Label(frame_controls)
        espacio_1.grid(row=1)
        espacio_2 = Label(frame_controls)
        espacio_2.grid(row=2)       
        espacio_3 = Label(frame_controls)
        espacio_3.grid(row=3)
        espacio_4 = Label(frame_controls)
        espacio_4.grid(row=4)

        # COMBOBOX
        cb_forma_pago = ["Débito", "Tarj. Crédito", "Cta. Cte.", "MercadoPago", "MODO", "Transferencia", "Efectivo"]
        cb_tipo_cliente = ["Consumidor Final", "Empresa"]

        # ETIQUETAS DE INPUTS
        Label(frame_controls, text="PRODUCTO").grid(row=3, column=6, sticky=E, pady=2)
        Label(frame_controls, text="CANTIDAD").grid(row=4, column=6, sticky=E, pady=2)
        Label(frame_controls, text="PRECIO UNIT.").grid(row=5, column=6, sticky=E, pady=2)
        Label(frame_controls, text="PRECIO TOTAL").grid(row=6, column=6, sticky=E, pady=2)
        Label(frame_controls, text="FORMA DE PAGO").grid(row=7, column=6, sticky=E, pady=2)
        Label(frame_controls, text="TIPO DE CLIENTE").grid(row=8, column=6, sticky=E, pady=2)

        # Variables
        self.vid = StringVar()
        self.vproducto = StringVar()
        self.vcantidad = StringVar()
        self.vprecio_unit = StringVar()
        self.vprecio_total = StringVar()
        self.vforma_pago = StringVar()
        self.vtipo_cliente = StringVar()

        # Calcular Precio Total
        self.vcantidad.trace("w", self.calcular_precio_total)
        self.vprecio_unit.trace("w", self.calcular_precio_total)

        # Inputs
        Entry(frame_controls, textvariable=self.vid, justify="center", width="10").grid(row=2, column=7, padx=(2, 0))
        Entry(frame_controls, textvariable=self.vproducto).grid(row=3, column=7)
        Entry(frame_controls, textvariable=self.vcantidad, justify="right").grid(row=4, column=7)
        Entry(frame_controls, textvariable=self.vprecio_unit, justify="right").grid(row=5, column=7)
        Entry(frame_controls, textvariable=self.vprecio_total, justify="right", state="readonly").grid(row=6, column=7)

        combo_forma_pago = ttk.Combobox(frame_controls, textvariable=self.vforma_pago, values=cb_forma_pago, state="readonly")
        combo_forma_pago.grid(row=7, column=7)
        combo_forma_pago.set("Forma de Pago")

        combo_tipo_cliente = ttk.Combobox(frame_controls, textvariable=self.vtipo_cliente, values=cb_tipo_cliente, state="readonly")
        combo_tipo_cliente.grid(row=8, column=7, pady=2)
        combo_tipo_cliente.set("Tipo de Cliente")


        # Treeview
        self.tree = ttk.Treeview(frame_treeview)
        #self.tree = ttk.Treeview(self.window)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=25, minwidth=25, anchor=W)
        self.tree.heading("#0", text="ID")
        self.tree.column("col1", width=140, minwidth=80, anchor=W)
        self.tree.heading("col1", text="PRODUCTO")
        self.tree.column("col2", width=65, minwidth=65, anchor=CENTER)
        self.tree.heading("col2", text="CANTIDAD")
        self.tree.column("col3", width=80, minwidth=80, anchor=E)
        self.tree.heading("col3", text="PRECIO UNIT")
        self.tree.column("col4", width=100, minwidth=80, anchor=E)
        self.tree.heading("col4", text="PRECIO TOTAL")
        self.tree.column("col5", width=110, minwidth=100, anchor=CENTER)
        self.tree.heading("col5", text="FORMA DE PAGO")
        self.tree.column("col6", width=110, minwidth=80, anchor=CENTER)
        self.tree.heading("col6", text="TIPO DE CLIENTE")

        self.tree.grid(column=0, row=2, columnspan=6, padx=(25, 0))

        # Botones
        Button(frame_controls, text="Modificar por ID", width=20, command=self.vista_update).grid(row=2, column=6)
        Button(frame_controls, text="Eliminar", width=20, command=self.vista_borrar).grid(row=9, column=7)
        Button(frame_controls, text="Limpiar datos", width=20, command=self.limpiar).grid(row=10, column=7)

        # Cargar los datos en el Treeview al iniciar
        cargar_datos(self.tree)

    def calcular_precio_total(self, *args):
        try:
            cantidad = float(self.vcantidad.get())
            precio_unit = float(self.vprecio_unit.get())
            precio_total = cantidad * precio_unit
            self.vprecio_total.set(f"{precio_total:.2f}")
        except ValueError:
            self.vprecio_total.set("0.00")

    def vista_agregar(self):
        titulo, mensaje = agregar(self.vproducto.get(), self.vcantidad.get(), self.vprecio_unit.get(), 
                                  self.vprecio_total.get(), self.vforma_pago.get(), self.vtipo_cliente.get(), 
                                  self.tree, self.limpiar, actualizar_treeview)
        messagebox.showinfo(titulo, mensaje)

    def vista_borrar(self):
        confirma = messagebox.askquestion("ADVERTENCIA", "¿Está seguro qué desea borrar el registro?")
        if confirma == 'no':
            return
        titulo, mensaje = borrar(self.tree)

    def vista_update(self):
        id = self.vid.get()
        if not id:
            messagebox.showinfo("MODIFICAR", "Debe escribir un ID válido para modificar.")
            return

        if not verificar_id(id):
            messagebox.showinfo("MODIFICAR", "El ID ingresado no existe en la base de datos.")
            return

        titulo, mensaje = update(self.vid.get(), self.vproducto.get(), self.vcantidad.get(), 
                                 self.vprecio_unit.get(), self.vprecio_total.get(), 
                                 self.vforma_pago.get(), self.vtipo_cliente.get(), 
                                 self.tree, self.limpiar, actualizar_treeview)
        messagebox.showinfo(titulo, mensaje)

    def limpiar(self):
        self.vid.set("")
        self.vproducto.set("")
        self.vcantidad.set("")
        self.vprecio_unit.set("")
        self.vprecio_total.set("0.00")
        self.vforma_pago.set("Forma de Pago")
        self.vtipo_cliente.set("Tipo de Cliente")

if __name__ == "__main__":
    root_tk = Tk()
    app = VentasListado(root_tk)
    root_tk.mainloop()
