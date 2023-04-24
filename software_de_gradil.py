import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import datetime as dt
import math

orders = []

# INPUT VALIDATOR FUNCTION


def validator():
    colors_ = ['Sem pintura', 'Branco', 'Preto', 'Verde']
    heights_ = [1.03, 1.53, 2.03]
    label_validator.config(text='')

    try:
        float(entry_length.get())

        try:
            heights_.index(float(select_height.get()))

            try:
                colors_.index(select_color.get())
                label_validator.config(text='Pedido confirmado!')
                calculate()

            except ValueError:
                label_validator.config(text='Cor indisponível!')

        except ValueError:
            label_validator.config(text='Altura indisponível!')

    except ValueError:
        label_validator.config(text='Comprimento precisa ser númerico!')


# CALCULATE FUNCTION
def calculate():
    label_information.configure(
        text='')

    # STORE ORDER
    date = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    orders.append((entry_length.get(), select_height.get(),
                  select_color.get(), date))

    # NUMBER OF PARTS
    grids_number = math.ceil(float(entry_length.get())/2.5)
    tree_number = grids_number + 1
    screw_number = tree_number*4
    fix_number = 0

    if select_height.get() == "1.03":
        fix_number = grids_number*6

    elif select_height.get() == "1.53":
        fix_number = grids_number*8

    else:
        fix_number = grids_number*12

    # SET TABLE
    if quote_table.get_children():
        quote_table.delete(quote_table.get_children())

    quote_table.insert(parent='', index='end', iid=0, text='',
                       values=(grids_number, tree_number, fix_number, screw_number))

    # SET_HISTORY

    history_table.insert(parent='', index='end', iid=len(orders), text='', values=(
        len(orders), entry_length.get(), select_height.get(), select_color.get(), date))

    grid_lenght = grids_number*2.5
    diff = grid_lenght - float(entry_length.get())

    if grid_lenght > float(entry_length.get()):
        label_information.configure(
            text=f'Diferença entre comprimento solicitado e orçado de {diff} metros')


# GRAPHIC GENERATION FUNCION


def graphic():
    plt.close()
    colors_ = ['Sem pintura', 'Branco', 'Preto', 'Verde']
    heights_ = [1.03, 1.53, 2.03]

    def plot():
        pinturas = {'Branco': 'whitesmoke', 'Preto': 'black', 'Verde': 'green'}

        # plot grid
        x = [0, 0, 2.5, 2.5, 0]
        y = [0, float(select_height.get()), float(select_height.get()), 0, 0]
        try:
            plt.plot(x, y, color=pinturas[select_color.get()])
        except KeyError:
            plt.plot(x, y, color=pinturas['Preto'])

        for i in range(25):
            x1 = [0.1*i, 0.1*i]
            y1 = [0, float(select_height.get())]

            try:
                plt.plot(x1, y1, color=pinturas[select_color.get()])
            except KeyError:
                plt.plot(x1, y1, color=pinturas['Preto'])

        # plot screw
        for i in range(2):
            x1 = [2.5*i, 2.5*i]
            y1 = [-0.2, float(select_height.get())]

            try:
                plt.plot(x1, y1, color=pinturas[select_color.get()])
            except KeyError:
                plt.plot(x1, y1, color=pinturas['Preto'])

        plt.show()

    try:
        heights_.index(float(select_height.get()))

        try:
            colors_.index(select_color.get())
            label_validator.config(text='Esboço gerado!')
            plot()

        except ValueError:
            label_validator.config(text='Cor indisponível!')

    except ValueError:
        label_validator.config(text='Altura indisponível!')


# --FABRICATION DATA--
colors = ['Sem pintura', 'Branco', 'Preto', 'Verde']
heights = [1.03, 1.53, 2.03]

window = tk.Tk()
window.title('Orçamento de gradil')
# window.configure(background='#1e3743')
window.geometry('1040x600')

# --SET LENGTH---
label_1 = tk.Label(text='Comprimento da cerca (metros):')
label_1.grid(row=1, column=0, padx=5, pady=5, sticky='nswe', columnspan=1)
entry_length = tk.Entry()
entry_length.grid(row=1, column=1, padx=5, pady=5,
                  sticky='nswe', columnspan=1)

# --SET HEIGHT---
label_2 = tk.Label(text='Selecione a altura desejada (metros):')
label_2.grid(row=2, column=0, padx=10, pady=10, sticky='nswe', columnspan=1)
select_height = ttk.Combobox(values=heights)
select_height.grid(row=2, column=1, padx=5, pady=5,
                   sticky='nswe', columnspan=1)

# --SET COLOR---
label_3 = tk.Label(text='Selecione a cor desejada:')
label_3.grid(row=3, column=0, padx=10, pady=10, sticky='nswe', columnspan=1)
select_color = ttk.Combobox(values=colors)
select_color.grid(row=3, column=1, padx=5, pady=5,
                  sticky='nswe', columnspan=1)

# --CONFIRM BUTTON--
confirm_button = tk.Button(text='Confirmar pedido', command=validator)
confirm_button.grid(row=4, column=0, padx=5, pady=5,
                    sticky='nswe', columnspan=1)

# --GRAPHIC BUTTON--
calculate_button = tk.Button(
    text='Gerar esboço', command=graphic)
calculate_button.grid(row=4, column=1, padx=5, pady=5,
                      sticky='nswe', columnspan=1)

# --LABEL VALIDATOR--
label_validator = tk.Label(text='')
label_validator.grid(row=5, column=0, padx=5, pady=5,
                     sticky='nswe', columnspan=2)
label_validator.configure(background='yellow')

# LABEL INFORMATION
label_information = tk.Label(text='')
label_information.grid(row=6, column=0, padx=5, pady=5,
                       sticky='nswe', columnspan=2)


# --TABLE FRAME--
label_historic = tk.Label(text='Quantidade de peças necessárias:')
label_historic.grid(row=7, column=0, padx=5, pady=5,
                    sticky='nswe', columnspan=2)


quote_table = ttk.Treeview(window)
quote_table.grid(row=8, column=0, padx=5, pady=5, sticky='nswe', columnspan=2)
quote_table.configure(height=1)

quote_table['columns'] = ("telas", "postes", "fixadores", "parafusos")
quote_table.column("#0", width=0, stretch='NO')
quote_table.column('telas', anchor='center')
quote_table.column('postes', anchor='center')
quote_table.column('fixadores', anchor='center')
quote_table.column('parafusos', anchor='center')

quote_table.heading("telas", text="Qtd. telas", anchor='center')
quote_table.heading("postes", text="Qtd. postes", anchor='center')
quote_table.heading("fixadores", text="Qtd. fixadores", anchor='center')
quote_table.heading("parafusos", text="Qtd. parafusos", anchor='center')


# --HISTORIC FRAME--
label_history = tk.Label(text='Histórico de pedidos')
label_history.grid(row=9, column=0, padx=5, pady=5,
                   sticky='nswe', columnspan=2)

history_table = ttk.Treeview(window)
history_table.grid(row=10, column=0, padx=5, pady=5,
                   sticky='nswe', columnspan=2)

history_table['columns'] = ("ID", "Comprimento", "Altura", "Pintura", "Data")
history_table.column("#0", width=0, stretch='NO')
history_table.column('ID', anchor='center')
history_table.column('Comprimento', anchor='center')
history_table.column('Altura', anchor='center')
history_table.column('Pintura', anchor='center')
history_table.column('Data', anchor='center')

history_table.heading("ID", text="ID", anchor='center')
history_table.heading("Comprimento", text="Comprimento", anchor='center')
history_table.heading("Altura", text="Altura", anchor='center')
history_table.heading("Pintura", text="Pintura", anchor='center')
history_table.heading("Data", text="Data", anchor='center')

############################################################################

window.mainloop()
