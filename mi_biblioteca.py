# Autor: Antony Rangel
# Fecha: 
# Descripción: Libreria para el manejo de libros y autores en una biblioteca

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import re


# Nombre del archivo Excel
archivo_excel = 'biblioteca-LQ.xlsx'


# Verificar si el archivo Excel existe, si no, crearlo
try:
    df = pd.read_excel(archivo_excel, engine='openpyxl', dtype={'Fecha de préstamo': str, 'Fecha de devolución': str})
except FileNotFoundError:
    df = pd.DataFrame(columns=['ID', 'Título', 'Autor', 'Año publicacion', 'Editorial', 'Categoría', 'ISBN', 'Estado', 'Prestado a', 'Carnet', 'Telefono', 'Correo', 'Carrera', 'Fecha de préstamo', 'Fecha de devolución'])
    df.to_excel(archivo_excel, index=False, engine='openpyxl')

   

# Clase BibliotecaApp
class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Biblioteca")
        self.root.geometry("1200x600")
        self.root.config(bg="#6a1b9a")
        
        

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame para las etiquetas y entradas
        self.frame_entries = tk.Frame(self.root, bg="#ce93d8", bd=2, relief=tk.GROOVE)
        self.frame_entries.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label_titulo = tk.Label(self.frame_entries, text="Título:")
        self.label_titulo.grid(row=0, column=0, sticky="e", pady=5)
        self.entry_titulo = tk.Entry(self.frame_entries)
        self.entry_titulo.grid(row=0, column=1, columnspan=2, pady=5)

        self.label_autor = tk.Label(self.frame_entries, text="Autor:")
        self.label_autor.grid(row=1, column=0, sticky="e",pady=5)
        self.entry_autor = tk.Entry(self.frame_entries)
        self.entry_autor.grid(row=1, column=1, columnspan=2,pady=5)

        self.label_anio = tk.Label(self.frame_entries, text="Año:")
        self.label_anio.grid(row=2, column=0, sticky="e", pady=5)
        self.entry_anio = tk.Entry(self.frame_entries)
        self.entry_anio.grid(row=2, column=1, columnspan=2, pady=5)

        self.label_editorial = tk.Label(self.frame_entries, text="Editorial:")
        self.label_editorial.grid(row=3, column=0, sticky="e", pady=5)
        self.entry_editorial = tk.Entry(self.frame_entries)
        self.entry_editorial.grid(row=3, column=1, columnspan=2, pady=5)

        self.label_categoria = tk.Label(self.frame_entries, text="Categoría:")
        self.label_categoria.grid(row=4, column=0, sticky="e", pady=5)
        self.entry_categoria = tk.Entry(self.frame_entries)
        self.entry_categoria.grid(row=4, column=1, columnspan=2, pady=5)

        self.label_isbn = tk.Label(self.frame_entries, text="ISBN:")
        self.label_isbn.grid(row=5, column=0, sticky="e", pady=5)
        self.entry_isbn = tk.Entry(self.frame_entries)
        self.entry_isbn.grid(row=5, column=1, columnspan=2, pady=5)

        #Boton para añadir libro
        self.button_add = tk.Button(self.frame_entries, text="Añadir Libro", command=self.anadir_libro)
        self.button_add.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)

        # Frame para el Treeview
        self.frame_treeview = tk.Frame(self.root)
        self.frame_treeview.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.frame_treeview, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.frame_treeview, columns=('ID', 'Título', 'Autor', 'Año publicacion', 'Editorial', 'Categoría', 'ISBN'), show='headings', yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Título', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Año publicacion', text='Año Publicación')
        self.tree.heading('Editorial', text='Editorial')
        self.tree.heading('Categoría', text='Categoría')
        self.tree.heading('ISBN', text='ISBN')

        self.tree.column('ID', width=30, anchor='center')
        self.tree.column('Título', width=150, anchor='center')
        self.tree.column('Autor', width=150, anchor='center')
        self.tree.column('Año publicacion', width=150, anchor='center')
        self.tree.column('Editorial', width=150, anchor='center')
        self.tree.column('Categoría', width=150, anchor='center')
        self.tree.column('ISBN', width=150, anchor='center')

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para los botones
        self.frame_buttons = tk.Frame(self.root, bg="#ce93d8", bd=2, relief=tk.GROOVE)
        self.frame_buttons.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.button_search = tk.Button(self.frame_buttons, text="Buscar Libro", command=self.buscar_libro)
        self.button_search.grid(row=0, column=0,sticky="nsew", padx=3, pady=3)

        self.button_view = tk.Button(self.frame_buttons, text="Ver Libros", command=self.ver_libros)
        self.button_view.grid(row=0, column=1,sticky="nsew", padx=3, pady=3)

        self.button_clear = tk.Button(self.frame_buttons, text="Limpiar Campos", command=self.limpiar_campos)
        self.button_clear.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

        self.button_delete = tk.Button(self.frame_buttons, text="Eliminar Libro", command=self.eliminar_libro)
        self.button_delete.grid(row=2, column=0,sticky="nsew", padx=3, pady=3)

        self.button_update = tk.Button(self.frame_buttons, text="Actualizar Libro", command=self.actualizar_libro)
        self.button_update.grid(row=2, column=1,sticky="nsew", padx=3, pady=3)

        self.button_mostrar_acerca_de = tk.Button(self.frame_buttons, text="Acerca de", command=self.mostrar_acerca_de)
        self.button_mostrar_acerca_de.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

        # Frame para el estado del libro
        self.frame_estado = tk.Frame(self.root,bg="#ce93d8", bd=2, relief=tk.GROOVE)
        self.frame_estado.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Etiquetas y entradas para la información del estado del libro
        self.label_estado = tk.Label(self.frame_estado, text="Estado:")
        self.label_estado.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.label_estado_valor = tk.Label(self.frame_estado, text="")
        self.label_estado_valor.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.label_prestado_a = tk.Label(self.frame_estado, text="Prestado a:")
        self.label_prestado_a.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_prestado_a = tk.Entry(self.frame_estado, justify='center')
        self.entry_prestado_a.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.label_carnet = tk.Label(self.frame_estado, text="Carnet:")
        self.label_carnet.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_carnet = tk.Entry(self.frame_estado, justify='center')
        self.entry_carnet.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        self.telefeno = tk.Label(self.frame_estado, text="Teléfono:")
        self.telefeno.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_telefono = tk.Entry(self.frame_estado, justify='center')
        self.entry_telefono.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        self.correo = tk.Label(self.frame_estado, text="Correo:")
        self.correo.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_correo = tk.Entry(self.frame_estado, justify='center')
        self.entry_correo.grid(row=4, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.carrera = tk.Label(self.frame_estado, text="Carrera:")
        self.carrera.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_carrera = tk.Entry(self.frame_estado, justify='center')
        self.entry_carrera.grid(row=5, column=1,columnspan=2, sticky="nsew", padx=5, pady=5)

        self.label_fecha_prestamo = tk.Label(self.frame_estado, text="Fecha de Préstamo:")
        self.label_fecha_prestamo.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_fecha_prestamo = tk.Entry(self.frame_estado, justify='center')
        self.entry_fecha_prestamo.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)

        self.label_fecha_devolucion = tk.Label(self.frame_estado, text="Fecha de Devolución:")
        self.label_fecha_devolucion.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
        self.entry_fecha_devolucion = tk.Entry(self.frame_estado, justify='center')
        self.entry_fecha_devolucion.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)

        self.button_prestar = tk.Button(self.frame_estado, text="Prestar Libro", command=self.prestar_libro)
        self.button_prestar.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.button_devolver = tk.Button(self.frame_estado, text="Devolver Libro", command=self.devolver_libro)
        self.button_devolver.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.button_actualizar_estado = tk.Button(self.frame_estado, text="Actualizar Estado", command=self.actualizar_estado)
        self.button_actualizar_estado.grid(row=9, column=0, columnspan=2, sticky="nsew",padx=5, pady=5)

        self.button_ver_libros_disponibles = tk.Button(self.frame_estado, text="Ver Libros Disponibles", command=self.ver_libros_disponibles)
        self.button_ver_libros_disponibles.grid(row=8, column=2, sticky="nsew", padx=5, pady=5)

        self.button_ver_libros_prestados = tk.Button(self.frame_estado, text="Ver Libros Prestados", command=self.ver_libros_prestados)
        self.button_ver_libros_prestados.grid(row=9, column=2, sticky="nsew", padx=5, pady=5)


        # Configurar el evento de doble clic en el árbol de libros
        self.tree.bind("<Double-1>", self.mostrar_estado_libro)

        # Frame para el Treeview_2 de libros disponibles y prestados
        self.frame_treeview_2 = tk.Frame(self.root)
        self.frame_treeview_2.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.scrollbar_2 = tk.Scrollbar(self.frame_treeview_2, orient=tk.VERTICAL)
        self.tree_2 = ttk.Treeview(self.frame_treeview_2,columns=('ID', 'Título'), show='headings', yscrollcommand=self.scrollbar_2.set)
        self.scrollbar_2.config(command=self.tree_2.yview)

        self.tree_2.heading('ID', text='ID')
        self.tree_2.heading('Título', text='Título')

        self.tree_2.column('ID', width=10, anchor='center')
        self.tree_2.column('Título', width=150, anchor='center')

        self.scrollbar_2.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar el evento de doble clic en el árbol de libros disponibles y prestados
        self.tree_2.bind("<Double-1>", self.mostrar_estado_libro)

        # Asociar los eventos hover de a los botones
        self.button_add.bind("<Enter>", self.on_enter)
        self.button_add.bind("<Leave>", self.on_leave)
        self.button_search.bind("<Enter>", self.on_enter)
        self.button_search.bind("<Leave>", self.on_leave)
        self.button_view.bind("<Enter>", self.on_enter)
        self.button_view.bind("<Leave>", self.on_leave)
        self.button_clear.bind("<Enter>", self.on_enter)
        self.button_clear.bind("<Leave>", self.on_leave)
        self.button_delete.bind("<Enter>", self.on_enter)
        self.button_delete.bind("<Leave>", self.on_leave)
        self.button_update.bind("<Enter>", self.on_enter)
        self.button_update.bind("<Leave>", self.on_leave)
        self.button_prestar.bind("<Enter>", self.on_enter)
        self.button_prestar.bind("<Leave>", self.on_leave)
        self.button_devolver.bind("<Enter>", self.on_enter)
        self.button_devolver.bind("<Leave>", self.on_leave)
        self.button_actualizar_estado.bind("<Enter>", self.on_enter)
        self.button_actualizar_estado.bind("<Leave>", self.on_leave)
        self.button_ver_libros_disponibles.bind("<Enter>", self.on_enter)
        self.button_ver_libros_disponibles.bind("<Leave>", self.on_leave)
        self.button_ver_libros_prestados.bind("<Enter>", self.on_enter)
        self.button_ver_libros_prestados.bind("<Leave>", self.on_leave)
        self.button_mostrar_acerca_de.bind("<Enter>", self.on_enter)
        self.button_mostrar_acerca_de.bind("<Leave>", self.on_leave)


    # Funciones para el hover
    def on_enter(self, event):
        event.widget['background'] = 'lightgrey'  # Cambia el color de fondo al pasar el cursor
        event.widget['cursor'] = 'hand2'  # Cambia el cursor al pasar el cursor

    def on_leave(self, event):
        event.widget['background'] = 'SystemButtonFace'  # Restaura el color de fondo original
        event.widget['cursor'] = ''  # Restaura el cursor original
    

        


    # Funciones
    def limpiar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_anio.delete(0, tk.END)
        self.entry_editorial.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)
        self.entry_prestado_a.delete(0, tk.END)
        self.entry_carnet.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_carrera.delete(0, tk.END)
        self.entry_fecha_prestamo.delete(0, tk.END)
        self.entry_fecha_devolucion.delete(0, tk.END)


    def buscar_libro(self):
        # Obtener el texto de búsqueda desde los campos de entrada
        titulo_buscado = self.entry_titulo.get().strip()
        autor_buscado = self.entry_autor.get().strip()
        anio_buscado = self.entry_anio.get().strip()
        editorial_buscada = self.entry_editorial.get().strip()
        categoria_buscada = self.entry_categoria.get().strip()
        isbn_buscado = self.entry_isbn.get().strip()

        # Crear una máscara de búsqueda combinada
        mask = pd.Series([True] * len(df))
        if titulo_buscado:
            mask &= df['Título'].str.contains(titulo_buscado, case=False, na=False)
        if autor_buscado:
            mask &= df['Autor'].str.contains(autor_buscado, case=False, na=False)
        if anio_buscado:
            mask &= df['Año publicacion'].astype(str).str.contains(anio_buscado, case=False, na=False)
        if editorial_buscada:
            mask &= df['Editorial'].str.contains(editorial_buscada, case=False, na=False)
        if categoria_buscada:
            mask &= df['Categoría'].str.contains(categoria_buscada, case=False)
        if isbn_buscado:
            mask &= df['ISBN'].str.contains(isbn_buscado, case=False, na=False)

        resultados = df[mask]

        # Limpiar el Treeview antes de mostrar los resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar los resultados en el Treeview
        for _, fila in resultados.iterrows():
            self.tree.insert("", tk.END, values=(fila['ID'], fila['Título'], fila['Autor'], fila['Año publicacion'], fila['Editorial'], fila['Categoría'], fila['ISBN']))

        if resultados.empty:
            messagebox.showinfo("Sin Resultados", "No se encontraron libros que coincidan con los criterios de búsqueda.")

    def anadir_libro(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        anio = self.entry_anio.get()
        editorial = self.entry_editorial.get()
        categoria = self.entry_categoria.get()
        isbn = self.entry_isbn.get()

        if titulo and autor and anio and editorial and categoria and isbn:
            global df
            nuevo_id = df['ID'].max() + 1 if not df.empty else 1
            nuevo_libro = pd.DataFrame([[nuevo_id, titulo, autor, anio, editorial, categoria, isbn]], columns=['ID', 'Título', 'Autor', 'Año publicacion', 'Editorial', 'Categoría', 'ISBN'])
            df = pd.concat([df, nuevo_libro], ignore_index=True)
            df.to_excel(archivo_excel, index=False, engine='openpyxl')
            messagebox.showinfo("Éxito", "El libro ha sido añadido exitosamente.")
            self.limpiar_campos()
            self.ver_libros()
        else:
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos antes de añadir el libro.")

    def ver_libros(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        global df
        for _, fila in df.iterrows():
            self.tree.insert("", tk.END, values=(fila['ID'], fila['Título'], fila['Autor'], fila['Año publicacion'], fila['Editorial'], fila['Categoría'], fila['ISBN']))

    def eliminar_libro(self):
        seleccion = self.tree.selection()
        if seleccion:
            respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar el libro seleccionado?")
            if respuesta:
                global df
                item = self.tree.item(seleccion)
                libro_id = item['values'][0]
                df = df[df['ID'] != libro_id]

                # Reasignar IDs para mantener la consecutividad
                df.reset_index(drop=True, inplace=True)
                df['ID'] = df.index + 1

                df.to_excel(archivo_excel, index=False, engine='openpyxl')
                messagebox.showinfo("Éxito", "El libro ha sido eliminado exitosamente.")
                self.ver_libros()
        else:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione un libro para eliminar.")

    def actualizar_libro(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion)
            libro_id = item['values'][0]

            nuevo_titulo = self.entry_titulo.get().strip()
            nuevo_autor = self.entry_autor.get().strip()
            nuevo_anio = self.entry_anio.get().strip()
            nueva_editorial = self.entry_editorial.get().strip()
            nueva_categoria = self.entry_categoria.get().strip()
            nuevo_isbn = self.entry_isbn.get().strip()

            # Verificar si al menos un campo ha sido completado
            if nuevo_titulo or nuevo_autor or nuevo_anio or nueva_editorial or nueva_categoria or nuevo_isbn:
                global df
                if nuevo_titulo:
                    df.loc[df['ID'] == libro_id, 'Título'] = nuevo_titulo
                if nuevo_autor:
                    df.loc[df['ID'] == libro_id, 'Autor'] = nuevo_autor
                if nuevo_anio:
                    df.loc[df['ID'] == libro_id, 'Año publicacion'] = nuevo_anio
                if nueva_editorial:
                    df.loc[df['ID'] == libro_id, 'Editorial'] = nueva_editorial
                if nueva_categoria:
                    df.loc[df['ID'] == libro_id, 'Categoría'] = nueva_categoria
                if nuevo_isbn:
                    df.loc[df['ID'] == libro_id, 'ISBN'] = nuevo_isbn

                df.to_excel(archivo_excel, index=False, engine='openpyxl')
                messagebox.showinfo("Éxito", "El libro ha sido actualizado exitosamente.")
                self.limpiar_campos()
                self.ver_libros()
            else:
                messagebox.showerror("Error", "Por favor, complete al menos un campo para actualizar el libro.")
        else:
            messagebox.showwarning("Seleccion vacia", "Por favor, seleccione un libro para actualizar.")
    
    def mostrar_estado_libro(self, event):
       # Determinar cuál widget generó el evento
        widget = event.widget

        if widget == self.tree:
            selected_item = self.tree.selection()
            selected_item_2 = []
        elif widget == self.tree_2:
            selected_item = []
            selected_item_2 = self.tree_2.selection()

        # Verificar si hay alguna selección en cualquiera de los árboles
        if selected_item or selected_item_2:
            # Priorizar la selección de tree, pero usar tree_2 si tree está vacío
            if selected_item:
                item = self.tree.item(selected_item[0])
            else:
                item = self.tree_2.item(selected_item_2[0])

            libro_id = item['values'][0] 
            libro = df[df['ID'] == libro_id].iloc[0]

            estado = libro['Estado'] if pd.notna(libro['Estado']) else 'Disponible'
            self.label_estado_valor.config(text=estado, bg='green' if estado.lower() == 'disponible' else 'red', fg='white')

            self.entry_prestado_a.delete(0, tk.END)
            if pd.notna(libro['Prestado a']):
                self.entry_prestado_a.insert(0, libro['Prestado a'])

            self.entry_carnet.delete(0, tk.END)
            if pd.notna(libro['Carnet']):
                self.entry_carnet.insert(0, libro['Carnet'])

            self.entry_telefono.delete(0, tk.END)
            if pd.notna(libro['Telefono']):
                self.entry_telefono.insert(0, libro['Telefono'])

            self.entry_correo.delete(0, tk.END)
            if pd.notna(libro['Correo']):
                self.entry_correo.insert(0, libro['Correo'])

            self.entry_carrera.delete(0, tk.END)
            if pd.notna(libro['Carrera']):
                self.entry_carrera.insert(0, libro['Carrera'])

            self.entry_fecha_prestamo.delete(0, tk.END)
            if pd.notna(libro['Fecha de préstamo']):
                self.entry_fecha_prestamo.insert(0, libro['Fecha de préstamo'])

            self.entry_fecha_devolucion.delete(0, tk.END)
            if pd.notna(libro['Fecha de devolución']):
                self.entry_fecha_devolucion.insert(0, libro['Fecha de devolución'])

            # Verificar si el libro ya está prestado y eliminar el botón si es necesario
            if estado.lower() != 'disponible':
                self.button_prestar.grid_remove()
                self.button_devolver.grid() # Asegurarse de que el botón se muestre si el libro está prestado
            else:
                self.button_prestar.grid()   # Asegurarse de que el botón se muestre si el libro está disponible
                self.button_devolver.grid_remove()
        else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un libro para ver su estado.")


    def prestar_libro(self):
        # Determinar cuál widget tiene la selección
        selected_item = self.tree.selection()
        selected_item_2 = self.tree_2.selection()

        # Usar el primer ítem seleccionado válido
        if selected_item:
            item = self.tree.item(selected_item[0])
        elif selected_item_2:
            item = self.tree_2.item(selected_item_2[0])
        else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un libro para prestar.")
            return

        libro_id = item['values'][0]
        prestado_a = self.entry_prestado_a.get()
        carnet = self.entry_carnet.get()
        telefono = self.entry_telefono.get()
        correo = self.entry_correo.get()
        carrera = self.entry_carrera.get()
        fecha_prestamo = self.entry_fecha_prestamo.get()
        fecha_devolucion = self.entry_fecha_devolucion.get()

        if not prestado_a or not carnet or not telefono or not correo or not carrera or not fecha_prestamo or not fecha_devolucion:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios para prestar un libro.")
            return
        
        # Validar formato de fecha DD/MM/YY
        fecha_regex = r'^\d{2}/\d{2}/\d{4}$'
        
        if not re.match(fecha_regex, fecha_prestamo):
            messagebox.showerror("Formato de Fecha Inválido", "Por favor, ingrese la Fecha de Préstamo en el formato DD/MM/YY.")
            return
        
        if not re.match(fecha_regex, fecha_devolucion):
            messagebox.showerror("Formato de Fecha Inválido", "Por favor, ingrese la Fecha de Devolución en el formato DD/MM/YY.")
            return
        
        # Validar formato de carnet XX-XXXXX
        carnet_regex = r'^\d{2}-\d{5}$'

        if not re.match(carnet_regex, carnet):
            messagebox.showerror("Formato de Carnet Inválido", "Por favor, ingrese el Carnet en el formato XX-XXXXX.")
            return
        
        # Validar formato de telefono XXXX-XXXXXXX
        telefono_regex = r'^\d{4}-\d{7}$'

        if not re.match(telefono_regex, telefono):
            messagebox.showerror("Formato de Teléfono Inválido", "Por favor, ingrese el Teléfono en el formato XXXX-XXXXXXX.")
            return
        
        # Validar formato de correo
        correo_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(correo_regex, correo):
            messagebox.showerror("Formato de Correo Inválido", "Por favor, ingrese el Correo en un formato válido.")
            return

        # Actualizar los campos correspondientes en el DataFrame
        df.loc[df['ID'] == libro_id, 'Estado'] = 'Prestado'
        df.loc[df['ID'] == libro_id, 'Prestado a'] = prestado_a
        df.loc[df['ID'] == libro_id, 'Carnet'] = carnet
        df.loc[df['ID'] == libro_id, 'Telefono'] = telefono
        df.loc[df['ID'] == libro_id, 'Correo'] = correo
        df.loc[df['ID'] == libro_id, 'Carrera'] = carrera
        df.loc[df['ID'] == libro_id, 'Fecha de préstamo'] = fecha_prestamo
        df.loc[df['ID'] == libro_id, 'Fecha de devolución'] = fecha_devolucion
        df.to_excel(archivo_excel, index=False, engine='openpyxl')
        
        messagebox.showinfo("Éxito", "Libro prestado con éxito.")
        self.ver_libros()
        self.limpiar_campos()


    def devolver_libro(self):
        selected_item = self.tree.selection()
        selected_item_2 = self.tree_2.selection()
        
        # Usar el primer ítem seleccionado válido
        if selected_item:
            item = self.tree.item(selected_item[0])
        elif selected_item_2:
            item = self.tree_2.item(selected_item_2[0])
        else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un libro para devolver.")
            return
        
        libro_id = item['values'][0]

        df.loc[df['ID'] == libro_id, 'Estado'] = 'Disponible'
        df.loc[df['ID'] == libro_id, 'Prestado a'] = None
        df.loc[df['ID'] == libro_id, 'Carnet'] = None
        df.loc[df['ID'] == libro_id, 'Telefono'] = None
        df.loc[df['ID'] == libro_id, 'Correo'] = None
        df.loc[df['ID'] == libro_id, 'Carrera'] = None
        df.loc[df['ID'] == libro_id, 'Fecha de préstamo'] = None
        df.loc[df['ID'] == libro_id, 'Fecha de devolución'] = None
        df.to_excel(archivo_excel, index=False, engine='openpyxl')
        messagebox.showinfo("Éxito", "Libro devuelto con éxito.")
        self.ver_libros()
        self.limpiar_campos()
        
        

    def actualizar_estado(self):
        selected_item = self.tree.selection()
        selected_item_2 = self.tree_2.selection()

        # Usar el primer ítem seleccionado válido
        if selected_item:
            item = self.tree.item(selected_item[0])
        elif selected_item_2:
            item = self.tree_2.item(selected_item_2[0])
        else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un libro para actualizar su estado.")
            return

        libro_id = item['values'][0]
        libro = df[df['ID'] == libro_id].iloc[0]
        nuevo_estado = self.label_estado_valor.cget("text")

        nuevo_prestado_a = self.entry_prestado_a.get()
        nuevo_carnet = self.entry_carnet.get()
        nuevo_telefono = self.entry_telefono.get()
        nuevo_correo = self.entry_correo.get()
        nueva_carrera = self.entry_carrera.get()
        nueva_fecha_prestamo = self.entry_fecha_prestamo.get()
        nueva_fecha_devolucion = self.entry_fecha_devolucion.get()

        # Verificar si el libro ya ha sido prestado antes de permitir la actualización
        if pd.notna(libro['Prestado a']):
            # Validar formato de fecha DD/MM/YY
            fecha_regex = r'^\d{2}/\d{2}/\d{4}$'

            if nueva_fecha_prestamo and not re.match(fecha_regex, nueva_fecha_prestamo):
                messagebox.showerror("Formato de Fecha Inválido", "Por favor, ingrese la Fecha de Préstamo en el formato DD/MM/YY.")
                return

            if nueva_fecha_devolucion and not re.match(fecha_regex, nueva_fecha_devolucion):
                messagebox.showerror("Formato de Fecha Inválido", "Por favor, ingrese la Fecha de Devolución en el formato DD/MM/YY.")
                return

            # Validar formato de carnet XX-XXXXX
            carnet_regex = r'^\d{2}-\d{5}$'

            if nuevo_carnet and not re.match(carnet_regex, nuevo_carnet):
                messagebox.showerror("Formato de Carnet Inválido", "Por favor, ingrese el Carnet en el formato XX-XXXXX.")
                return

            # Validar formato de teléfono XXXX-XXXXXXX
            telefono_regex = r'^\d{4}-\d{7}$'

            if nuevo_telefono and not re.match(telefono_regex, nuevo_telefono):
                messagebox.showerror("Formato de Teléfono Inválido", "Por favor, ingrese el Teléfono en el formato XXXX-XXXXXXX.")
                return

            # Validar formato de correo
            correo_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            if nuevo_correo and not re.match(correo_regex, nuevo_correo):
                messagebox.showerror("Formato de Correo Inválido", "Por favor, ingrese el Correo en un formato válido.")
                return

            # Actualizar los campos correspondientes en el DataFrame
            df.loc[df['ID'] == libro_id, 'Estado'] = nuevo_estado
            df.loc[df['ID'] == libro_id, 'Prestado a'] = nuevo_prestado_a
            df.loc[df['ID'] == libro_id, 'Carnet'] = nuevo_carnet
            df.loc[df['ID'] == libro_id, 'Telefono'] = nuevo_telefono
            df.loc[df['ID'] == libro_id, 'Correo'] = nuevo_correo
            df.loc[df['ID'] == libro_id, 'Carrera'] = nueva_carrera
            df.loc[df['ID'] == libro_id, 'Fecha de préstamo'] = nueva_fecha_prestamo
            df.loc[df['ID'] == libro_id, 'Fecha de devolución'] = nueva_fecha_devolucion

            # Guardar los cambios en el archivo Excel
            df.to_excel(archivo_excel, index=False, engine='openpyxl')
            messagebox.showinfo("Éxito", "Estado del libro actualizado con éxito.")
            self.ver_libros()
        else:
            messagebox.showwarning("Acción no permitida", "El estado solo se puede actualizar si el libro ha sido prestado.")


    def ver_libros_disponibles(self):
        for item in self.tree_2.get_children():
            self.tree_2.delete(item)
        
        global df
        # Filtrar libros disponibles o sin estado
        disponibles = df[(df['Estado'] == 'Disponible') | (df['Estado'].isnull()) | (df['Estado'] == '')]
        for _, fila in disponibles.iterrows():
            self.tree_2.insert("", tk.END, values=(fila['ID'], fila['Título']))

    def ver_libros_prestados(self):
        for item in self.tree_2.get_children():
            self.tree_2.delete(item)
        
        global df
        prestados = df[df['Estado'] == 'Prestado']
        for _, fila in prestados.iterrows():
            self.tree_2.insert("", tk.END, values=(fila['ID'], fila['Título']))


    
    def mostrar_acerca_de(self):
        acerca_de_texto = (
            "Nombre de la Aplicación: Mi Biblioteca\n"
            "Versión: 1.0.0\n"
            "Autor: Antony Rangel\n"
            "Fecha de Creación: Julio 2024\n"
            "Última Actualización: Julio 2024\n"
            "Descripción: Esta aplicación permite gestionar el inventario, préstamo y devolución de libros en una biblioteca.\n"
            "Contacto: tonyrdev26@gmail.com\n"
            "Licencia: MIT License\n\n"
            "De Tony para Yei <3"
        )
        messagebox.showinfo("Acerca de", acerca_de_texto)



# Crear instancia de tkinter
root = tk.Tk()
app = BibliotecaApp(root)

# Ejecutar la aplicación
root.mainloop()
