import tkinter as tk
from conectar import get_conexion
from tkinter import messagebox, ttk 
from datetime import date   
import pyodbc

class Compras:

    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.title('Compras a Proveedores.')
        self.ancho=650
        self.alto=550
        x = (self.top.winfo_screenwidth() // 2) - (self.ancho // 2)
        y = (self.top.winfo_screenheight() // 2) - (self.alto // 2)
        self.top.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")
        self.top.resizable (False, False)
        # Esto hace que cualquier botón de Tkinter responda a Enter
        self.top.bind_class("Button", "<Return>", lambda event: event.widget.invoke())   
        self.txt_codigo = tk.StringVar()
        self.txt_proveedor = tk.StringVar()
        self.total_general = tk.StringVar()
        self.txt_factura = tk.StringVar()
        self.opcion = tk.IntVar()
        self.txt_fecha_factura = tk.StringVar()
        self.total_general_numeric = tk.IntVar()
        
    
        frame_cabecera = tk.Frame(self.top)
        frame_cabecera.pack(fill='x', padx=10, pady=5)

        lbl_title = tk.Label(frame_cabecera, text='Carga de Facturas', font=("verdana", 20, 'bold'))
        lbl_title.pack(side='top', anchor='s')

        frame_cabecera2 = tk.Frame(self.top)         
        frame_cabecera2.pack(anchor='w',padx=10, pady=5)

        lbl_provee = tk.Label(frame_cabecera2, text='Proveedor', font=("verdana", 7, 'bold'))
        lbl_provee.grid(row=0, column=0, padx=(2,0), sticky='w')

        text_codigo = tk.Entry(frame_cabecera2, textvariable=self.txt_codigo,
                                state='disabled', disabledforeground='black', disabledbackground='white', justify='center', width=10)
        text_codigo.grid(row=0, column=1, padx=2, sticky='w')

        text_descripcion = tk.Entry(frame_cabecera2, textvariable=self.txt_proveedor, justify='left',
                                 width=50, state='disabled', disabledforeground='black')
        text_descripcion.grid(row=0, column=2,columnspan=1, padx=5, sticky='w')

        btn_buscar = tk.Button(frame_cabecera2, text='Buscar', font=("verdana", 7, 'bold'),
                                width=6, height=2, command=self.ventana_buscar)
        btn_buscar.grid(row=0, column=3, padx=10, sticky='w')
        

        lbl_factura = tk.Label(frame_cabecera2, text="Nro. de factura", font=("verdana", 7, "bold"))
        lbl_factura.grid(row=1, column=0, padx=(2,2), sticky='w')

        text_factura = tk.Entry(frame_cabecera2, textvariable=self.txt_factura, width=15)
        text_factura.grid(row=1, column=1, padx=2, sticky='w')
      
        # Bloque de opciones
        frame_opciones = tk.Frame(frame_cabecera2)
        frame_opciones.grid(row=1, column=2,columnspan=3, sticky='w', padx=10)

        lbl_option = tk.Label(frame_opciones, text="Selecciona una opción", font=("verdana",7,"bold"))
        lbl_option.pack(side='left', padx=(0,5))

        radio_option = tk.Radiobutton(frame_opciones, text='Contado', font=("verdana", 7, 'bold'),
                                    variable=self.opcion, value=1)
        radio_option.pack(side='left', padx=(0,5))

        radio_option2 = tk.Radiobutton(frame_opciones, text='Crédito', font=("verdana", 7, 'bold'),
                                    variable=self.opcion, value=2)
        radio_option2.pack(side='left', padx=(0,5))
        
        lbl_fecha = tk.Label(frame_cabecera2, text="Fecha Factura", font=("verdana", 7, "bold"), justify='left')
        lbl_fecha.grid(row=2, column=0, padx=(2,2), sticky='w')

        text_fecha = tk.Entry(frame_cabecera2, textvariable=self.txt_fecha_factura, width=15, justify="center")
        text_fecha.grid(row=2, column=1, padx=(2,10), sticky='w')            

        self.grilla = ttk.Treeview(self.top, columns=("items","descripcion","cantidad","precio_uni","precio","borrar"), show="headings")
        self.grilla.heading("items", text="Items")
        self.grilla.heading("descripcion", text="Descripción")
        self.grilla.heading("cantidad", text="Cantidad")
        self.grilla.heading("precio_uni", text="Precio Unit.")
        self.grilla.heading("precio", text="Precio")
        self.grilla.heading("borrar", text="Borrar")

        #Ajustar ancho de columnas
        self.grilla.column("items", width=10, anchor="w")
        self.grilla.column("descripcion", width=180, anchor='w')
        self.grilla.column("cantidad", width=10, anchor="center")
        self.grilla.column("precio_uni", width=10, anchor="center")
        self.grilla.column("precio", width=50, anchor="center")
        self.grilla.column("borrar", width=30, anchor="center")

        self.grilla.pack(expand=True, fill="both", pady=10)   

        self.clean() 
    
        "----------------------marco inferior principal-----------------------"

        marco_botones = tk.Frame(self.top)
        marco_botones.pack(fill='x', padx=10)

        btn_agregar = tk.Button(marco_botones, text='Agregar', font=('verdana',7,'bold'), width=5,
                                 height=2, padx=10, pady=10, command=self.aregar_articulos)
        btn_agregar.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        btn_guardar = tk.Button(marco_botones, text='Guardar',font=('verdana',7,'bold'), width=5,
                                 height=2, padx=10, pady=10, command=self.guardar)
        btn_guardar.grid(row=0, column=1,  padx=10, pady=10, sticky='w')

        marco_botones.grid_columnconfigure(1, weight=1)

        lbl_total = tk.Label(marco_botones, text='Total Compra:', font=("verdana", 8, "bold"))
        lbl_total.grid(row=0, column=2, padx=5, sticky='e')
                             
        suma_total = tk.Entry(marco_botones,textvariable=self.total_general, 
                            width=20,font=("Cominc Sens", 13, "bold"), state='disabled',
                            disabledbackground='lightblue', foreground='black')
        suma_total.grid(row=0, column=3, padx=5, sticky='e')

        btn_salir = tk.Button(marco_botones, text='Salir', font=('verdana',7,'bold'), width=5, height=2, padx=10, pady=10, command=self.top.destroy)
        btn_salir.grid(row=0, column=4, padx=10, pady=10, sticky='e')     
             
            
        self.grilla.bind("<Button-1>", self.eliminar_compra)   

    def formatear_number(self, value):
                #Formatea un número con separador de miles.
                return "{:,}".format(int(value))                            
    
    def suma_grilla(self):
        importe = 0
        for fila in self.grilla.get_children():
            valor_celda = self.grilla.item(fila)['values'][4]
            valor_celda_limpio = valor_celda.replace(',', '')
            importe += int(valor_celda_limpio)
        self.total_general.set(self.formatear_number(str(importe)))
        self.total_general_numeric = importe
        self.grilla.focus_set() 
      
    def eliminar_compra(self, event):
            item = self.grilla.identify_row(event.y)
            col = self.grilla.identify_column(event.x)
            if col == "#6":
                if item:
                    self.grilla.delete(item)
                    self.suma_grilla()

    def valida_factura(self):
        if self.txt_factura.get().strip()=="":
            messagebox.showerror(title='AVISO', message='INGRESE NUMERO DE FACTURA')
            return False             
        else:
             conn = get_conexion()
             if conn:
                try:
                    cursor = conn.cursor()
                    sql = "select com_nro from comprascab where com_nrodoc=? and prv_cod=?"
                    resultado = cursor.execute(sql, (self.txt_factura.get().strip(), self.txt_codigo.get())).fetchone()
                    if resultado:
                        messagebox.showerror(title='FAVOR VERIFICAR!!!', message='EL NÚMERO DE FACTURA YA SE ENCUENTRA REGISTRADO CON EL PROVEEDOR SELECCIONADO')
                        return
                except pyodbc.IntegrityError as e:
                        messagebox.showerror("Error de integridad", f"No se pudo abir.\n{e}")
                except Exception as e:
                        messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")  
                finally:
                    conn.close()                            
        return True
    
    def to_float(self, texto: str) -> float:
            try:
                # quitar separadores de miles
                limpio = texto.replace(",", "").strip()
                return float(limpio) if limpio else 0.0
            except ValueError:
                return 0.0      
            
    def guardar(self):
         if self.valida_factura():
            conn = get_conexion()
            if conn:
                try :
                    if self.opcion.get()==1:
                        tipodoc = 'FCO'
                    elif self.opcion.get()==2:
                        tipodoc = 'CRE'
                    else:
                        messagebox.showerror('AVISO', 'SELECCIONE CREDTO O CONTADO')
                        return            
                    
                    cursor = conn.cursor() 
                    cursor.execute("""insert into comprascab (com_fecha,
                                prv_cod, com_tipodoc, com_nrodoc, fecins,com_estado, com_total, com_cancelado)
                                values (?,?,?,?,?,?,?,?)""", (self.txt_fecha_factura.get(), self.txt_codigo.get(),
                                                            tipodoc, self.txt_factura.get(),date.today().strftime('%d/%m/%Y'),'A',
                                                            int(self.total_general_numeric), int(self.total_general_numeric)))
                    
                    resultado = cursor.execute('select @@identity from comprascab').fetchone()
                    id_cabecera = resultado[0]
                    itmens = 0
                    for dato in self.grilla.get_children():
                        valores = self.grilla.item(dato, 'values')
                        cod_articulo = valores[6]
                        cantidad = valores[2]
                        precio_uni = valores[3]
                        precio_uni_num = float(precio_uni.replace(',', ''))
                        subtotal = valores[4]
                        porcentaje = valores[7]
                        subtotal_num = subtotal.replace(',', '')
                        precioventa = valores[8]
                        precioventa_num = float(precioventa.replace(",",""))
                        itmens += 1
                        cursor.execute("""
                        INSERT INTO comprasdet (com_nro, com_item, art_cod, com_cantidad, com_preciouni, com_poriva, com_preciototal)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (id_cabecera, itmens, cod_articulo, cantidad, precio_uni_num, porcentaje, subtotal_num)) 

                        query = 'select art_costo, art_preciobase from articulos where art_cod=? '
                        result = cursor.execute(query, (cod_articulo,)).fetchone()    
                        if result[0]!=precio_uni_num and result[1]!=precioventa_num:
                             cursor.execute('update articulos set art_costo = ?, art_preciobase =? where art_cod = ? ', (precio_uni_num, precioventa_num, cod_articulo))
                        elif result[0]!=precio_uni_num:
                             cursor.execute('update articulos set art_costo = ? where art_cod = ? ', (precio_uni_num, cod_articulo))
                        elif result[1]!=precioventa_num:
                             cursor.execute('update articulos set art_preciobase = ? where art_cod = ? ', (precioventa_num, cod_articulo))

                        query_stock = 'select sto_cantidad from stock where art_cod = ?'
                        result_stock = cursor.execute(query_stock, (cod_articulo,)).fetchone()
                        if result_stock and result_stock[0] is not None:
                            nuevo_stock = float(result_stock[0]) + float(cantidad)
                            
                            cursor.execute('update stock set sto_cantidad = ? where art_cod = ?', (nuevo_stock, cod_articulo))
                        else:
                            cursor.execute('insert into stock (art_cod, dep_cod, sto_cantidad) values (?, ?, ?)', (cod_articulo, 1, nuevo_stock))
                                        
                    conn.commit()
                    messagebox.showinfo('Mensaje al Usuario', 'Guardado Correctamente.')
                    self.clean()
                except pyodbc.IntegrityError as e:
                            messagebox.showerror("Error de integridad", f"No se pudo abir.\n{e}")
                except Exception as e:
                            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")  
                finally:
                    conn.close()    

    def clean(self):
        for item in self.grilla.get_children():
            self.grilla.delete(item)

        self.txt_codigo.set("")
        self.txt_proveedor.set("")
        self.txt_factura.set("")
        self.txt_fecha_factura.set(value=date.today().strftime("%d/%m/%Y"))
        self.total_general.set("0")
                                
    def ventana_buscar(self):
        top_buscar = tk.Toplevel(self.top)
        top_buscar.title('Buscar Proveedor')
        self.ancho=550
        self.alto=350
        x = (top_buscar.winfo_screenwidth() // 2) - (self.ancho // 2)
        y = (top_buscar.winfo_screenheight() // 2) - (self.alto // 2)
        top_buscar.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")
        top_buscar.resizable (False, False)
        
        txt_proveedor = tk.StringVar()
    
        frame_cabecera = tk.Frame(top_buscar, width=500, height=100)
        frame_cabecera.grid(row=0, column=0, sticky="w")
        frame_cabecera.config(bg='lightblue')

        lbl_nombre = tk.Label(frame_cabecera, text='Nombre de Proveedor:', font=("verdana", 8, 'bold'), bg='lightblue') 
        lbl_nombre.grid(row=0, column=0, padx=5, pady=3)

        text_nombre = tk.Entry(frame_cabecera, textvariable=txt_proveedor, width=50 )
        text_nombre.grid(row=0, column=1, padx=5, pady=10)
        text_nombre.focus_set()
        
        grd_buscar = ttk.Treeview(frame_cabecera, columns=("codigo", "proveedor"), show="headings")
        grd_buscar.heading("codigo", text='Codigo')
        grd_buscar.heading("proveedor", text="Proveedor")

        grd_buscar.column("codigo", width=7, anchor='w')
        grd_buscar.column("proveedor", width=180, anchor='w')
        
        grd_buscar.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        def to_uppercase(event):
            text = text_nombre.get()
            text_nombre.delete(0, tk.END)
            text_nombre.insert(0, text.upper())

        text_nombre.bind("<KeyRelease>", to_uppercase)
              
        def buscar_proveedor():

            for items in grd_buscar.get_children():
                grd_buscar.delete(items)

            conn = get_conexion()
            if conn:
                try:
                    cursor = conn.cursor()
                    resultado = cursor.execute('select prv_cod, prv_nombre from proveedor where prv_nombre like ?', ('%' + text_nombre.get() + '%',))   .fetchall()
                    if resultado:
                        for fila in resultado:
                            grd_buscar.insert("", tk.END, values=(fila[0], fila[1]))
                    else:
                        messagebox.showinfo('Mensaje del Sistema', 'No se ecnuentra cliente con los parametros ingresados.')        

                except pyodbc.IntegrityError as e:
                    messagebox.showerror("Error de integridad", f"No se pudo guardar.\n{e}")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")         
                finally:
                    conn.close()   
        
        def seleccion(event):
                seleccionado = grd_buscar.item(grd_buscar.focus(), "values")
                if seleccionado:
                    self.txt_codigo.set(seleccionado[0])
                    self.txt_proveedor.set(seleccionado[1])
                    top_buscar.destroy()

        grd_buscar.bind("<Double-1>", seleccion)               

        btn_buscar = tk.Button(frame_cabecera, text='Buscar', font=('verdadna', 8, 'bold'), background='gray', padx=5, pady=5, command=buscar_proveedor)
        btn_buscar.grid(row=0, column=3, padx=5, pady=10)                

                                  
        ### seria el container buscar articulos
    def aregar_articulos(self): ## toplevel, VENTANA BUSCAR ARTICULO
        if self.txt_codigo.get() == "":
            messagebox.showerror(title='AVISO', message='PRIMERO SELECCIONE UN PROVEEDOR')
        else:
            top_articulo = tk.Toplevel(self.top)
            top_articulo.title('Buscar Articulos')
            self.ancho=650
            self.alto=550
            x = (top_articulo.winfo_screenwidth() // 2) - (self.ancho // 2)
            y = (top_articulo.winfo_screenheight() // 2) - (self.alto // 2)
            top_articulo.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")
            top_articulo.resizable (False, False)

            ##variables en la carg de productos
            txt_articulo = tk.StringVar()
            self.text_nombre_prod = tk.StringVar()
            self.text_codprod = tk.StringVar(value="0")
            self.text_cantidad = tk.StringVar(value="0")
            self.text_precio_costo = tk.StringVar(value="0")
            self.text_precio_venta = tk.StringVar(value="0")
            self.text_stock = tk.StringVar(value="0")
            self.text_total = tk.StringVar(value="0")

            def calcular_total(*args):
                try:
                    cant = float(self.text_cantidad.get())
                except:
                    cant = 0

                try:
                    valor_precio = self.text_precio_costo.get().replace(",","")
                    if not valor_precio.strip():
                         return
                    precio = float(valor_precio) 
                except:
                    precio = 0
                total = precio * cant
                self.text_total.set(self.formatear_number(total))

            def agregar_compras():
                if validad_cantidad():
                    try:
                        num_fila = len(self.grilla.get_children()) + 1
                        selccion = grd_articulo.focus()
                        if not selccion:
                             raise ValueError("No selecciono ningún articulo")
                        suvalores =  grd_articulo.item(selccion, 'values')
                        var_porcentaje = suvalores[5]
                        
                    except Exception:
                         messagebox.showerror(title='Mensaje al Usuario', message='Seleccione un Articulo')
                         return
                    
                    self.grilla.insert("", tk.END, values=(num_fila, self.text_nombre_prod.get(),
                                    float(self.text_cantidad.get()),self.text_precio_costo.get(), self.text_total.get(),"❌",
                                    self.text_codprod.get(), var_porcentaje, self.text_precio_venta.get()))  
                    self.suma_grilla() 
                    top_articulo.destroy()
                              
                    
            def buscar_articulos():
                for fila in grd_articulo.get_children():
                    grd_articulo.delete(fila)

                conn = get_conexion()
                if conn:
                    cursor = conn.cursor()
                    sql = """select t1.art_cod, t1.art_nombre, t1.art_costo, t1.art_preciobase, t2.sto_cantidad, t1.art_poriva 
                        from articulos as t1
                        outer apply 
                          (select top 1 sto_cantidad from STOCK as s where S.ART_COD=t1.ART_COD) as t2 
                         where art_nombre like ? and art_estado= ?"""
                    resultado = cursor.execute(sql, ('%' + txt_articulo.get() + '%','S')).fetchall() 
                    if resultado:
                        for fila in resultado:
                            grd_articulo.insert("", tk.END, values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]))  
                    else:        
                        messagebox.showinfo('Aviso', "NO se encuentra Articulo.")

            def seleccion(event):
                #seleccionado = grd_articulo.item(grd_articulo.focus(), "values")
                seleccionado = grd_articulo.focus() # obtiene el item seleccionado
                if not seleccionado:
                    return
                valores = grd_articulo.item(seleccionado, "values") # obtiene los valores de la fila
                self.text_codprod.set(valores[0])
                self.text_nombre_prod.set(valores[1])
                self.text_stock.set(valores[4])
                                
            def mayusculas(event):
                 text = text_articulo.get()
                 text_articulo.delete(0, tk.END)
                 text_articulo.insert(0, text.upper())

            self.text_cantidad.trace_add("write", calcular_total)
            self.text_precio_costo.trace_add("write", calcular_total)   

            def formatear_entry(entry):
                valor = entry.get()
                if not valor.strip():  # si está vacío, no hace nada
                    return
                try:
                    numero = float(valor.replace(",", "")) # quitar separadores para convertir
                    entry.delete(0, "end")
                    entry.insert(0, "{:,}".format(numero))  # insertar con separadores de miles
                except ValueError:
                    pass  # si no es número, lo ignora

            def validad_cantidad():
                cant  = self.to_float(self.text_cantidad.get())
                costo = self.to_float(self.text_precio_costo.get())
                venta = self.to_float(self.text_precio_venta.get())

                try:
                    if cant<=0:  
                        messagebox.showerror(title='Mensaje al Usuario', message='Ingrese Cantidad a comprar')
                        return False
                    elif costo<=0:
                        messagebox.showerror(title='Mensaje al Usuario', message='Ingrese Precio Costo')
                        return False
                    elif venta<=0:
                        messagebox.showerror(title='Mensaje al Usuario', message='Ingrese Precio Venta')
                        return False
                    return True 
                except ValueError:
                     messagebox.showerror(title='Mensaje al Usuario', message='Ingrese un valor númerico')

            frama_art = tk.Frame(top_articulo, relief='sunken', bd=2)
            frama_art.grid(row=0, column=0, sticky="nsew")

            # Configurar expansión dentro del frame
            frama_art.grid_rowconfigure(1, weight=1)       # La fila donde está el treeview
            frama_art.grid_columnconfigure(0, weight=1)    # La columna del treeview
            frama_art.grid_columnconfigure(1, weight=1)    # La columna del entry

            lbl_nombre_art = tk.Label(frama_art, text='Nombre Articulo', font=("verdana",9,"bold"),padx=5, pady=5)
            lbl_nombre_art.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            text_articulo = tk.Entry(frama_art,textvariable=txt_articulo, width=50)
            text_articulo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            text_articulo.focus_set()

            "-----------------------GRILLA DE ARTICULOS------------------" 
            grd_articulo = ttk.Treeview(frama_art, height=7, columns=("codigo", "articulo"), show="headings")
            grd_articulo.heading("codigo", text="Codigo")
            grd_articulo.heading("articulo", text="Articulo")    

            grd_articulo.column("codigo", width=15, minwidth=7, anchor="w")
            grd_articulo.column("articulo", width=200, anchor="w")

            grd_articulo.grid(row=1, column=0,columnspan=4, padx=20, pady=10, sticky="nsew")
            # Configurar expansión del toplevel
            top_articulo.grid_rowconfigure(0, weight=1)
            top_articulo.grid_columnconfigure(0, weight=1)
            
            ## eventos de la grid_articulos
            grd_articulo.bind("<<TreeviewSelect>>", seleccion) 
            text_articulo.bind("<KeyRelease>", mayusculas)    

            btn_buscar_art = tk.Button(frama_art, text='Buscar', font=('verdadna', 8, 'bold'), background='gray', padx=5, pady=5, command=buscar_articulos)
            btn_buscar_art.grid(row=0, column=3, padx=5, pady=10)      
            
            "-----------------------INFORMACIÓN DEL ARTICULO------------------" 
            framemarco = tk.Frame(top_articulo)
            framemarco.grid(row=1, column=0, sticky="nsew")
            framemarco.config(bd=2)
            framemarco.config(relief="sunken")
            
            lbl_info = tk.Label(framemarco, text="Información del Producto", font=("Cominc Sens", 9, "bold"))
            lbl_info.grid(row=0, column=0, padx=5)

            lbl_codigo = tk.Label(framemarco, text='Codigo del Producto', font=("Cominc Sens", 7, "bold"))
            lbl_codigo.grid(row=1, column=0,sticky='s', padx=5, pady=8)

            text_codprod = tk.Entry(framemarco, textvariable=self.text_codprod, width=25, state='readonly', readonlybackground='white')
            text_codprod.grid(row=1, column=1, padx=5, pady=8)

            lbl_nombre_prod = tk.Label(framemarco, text="Nombre del Producto", font=("Cominc Sens", 7, "bold"))
            lbl_nombre_prod.grid(row=2, column=0, sticky='s', padx=5, pady=8)
            text_nombre_prod = tk.Entry(framemarco, textvariable=self.text_nombre_prod, width=25, state='readonly')
            text_nombre_prod.grid(row=2, column=1, padx=5, pady=8)
            
            lbl_stock = tk.Label(framemarco, text="Existencia Actual", font=("Cominc Sens", 7, "bold"))
            lbl_stock.grid(row=3, column=0, sticky='s', padx=5, pady=8)
            text_stock = tk.Entry(framemarco, textvariable=self.text_stock, width=25, state='readonly')
            text_stock.grid(row=3, column=1, padx=5, pady=8)

            lbl_cantidad = tk.Label(framemarco, text="Cantidad", font=("Cominc Sens", 7, "bold"))
            lbl_cantidad.grid(row=1, column=2, sticky='s', padx=5, pady=8)
            text_cantidad = tk.Entry(framemarco,textvariable=self.text_cantidad, width=25)
            text_cantidad.grid(row=1, column=3, padx=5, pady=8)

            lbl_precio_costo = tk.Label(framemarco, text='Precio de costo', font=("Cominc Sens", 7, "bold"))
            lbl_precio_costo.grid(row=2, column=2, sticky='s', padx=5, pady=8)
            text_precio_costo = tk.Entry(framemarco,textvariable=self.text_precio_costo, width=25)
            text_precio_costo.grid(row=2, column=3, padx=5, pady=8)
            text_precio_costo.bind("<FocusOut>", lambda e: formatear_entry(text_precio_costo))

            lbl_precio_venta = tk.Label(framemarco, text='Precio de venta', font=("Cominc Sens", 7, "bold"))
            lbl_precio_venta.grid(row=3, column=2, sticky='s', padx=5, pady=8)
            text_precio_venta = tk.Entry(framemarco,textvariable=self.text_precio_venta, width=25)
            text_precio_venta.grid(row=3, column=3, padx=5, pady=8)
            text_precio_venta.bind("<FocusOut>", lambda e: formatear_entry(text_precio_venta))
            
            lbl_total = tk.Label(framemarco, text='Total', font=("Cominc Sens", 12, "bold"))
            lbl_total.grid(row=4, column=0, sticky='s', padx=5, pady=8)
            text_total = tk.Entry(framemarco,textvariable=self.text_total, width=25,  state='disabled', font=("Cominc Sens", 10, "bold"), disabledforeground='black')
            text_total.grid(row=4, column=1, columnspan=1, padx=2, pady=8)    

            guardar = tk.Button(framemarco, text='Guardar', font=("verdana",8, "bold"), width=8, height=2, command=agregar_compras)
            guardar.grid(row=4, column=2, padx=5, pady=5, sticky='w')

            cerrar = tk.Button(framemarco, text='Cerrar', font=("verdana",8, "bold"), width=8, height=2, command=top_articulo.destroy, padx=2)
            cerrar.grid(row=4, column=3, padx=1, pady=1, sticky="w")           
            
# Para probar
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Compras(root)
    root.mainloop()        

