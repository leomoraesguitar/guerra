import flet as ft
import pandas as pd
class My_Dropdown(ft.Dropdown):
    def __init__(self, nome,on_change, *itens):
        super().__init__()
        self.label = nome
        self.options = [ft.dropdown.Option(i) for i in list(itens)]
        self.on_change = on_change
        self.width = 150


    
class My_tabela(ft.DataTable):
    def __init__(self, df#DataFrame ou dicionário
                 ):
        super().__init__()
        self.df = df if type(df) != dict else pd.DataFrame(df)
        self.border = ft.border.all(1,'white,0.9')
        self.heading_row_color = 'white,0.5'
        self.heading_row_height = 35
        self.column_spacing = 15
        # self.heading_row_color=colors.BLACK12
        self.vertical_lines = ft.border.all(20,'white')
        self.horizontal_margin = 0
        self.data_row_max_height = 35
        # self.data_row_min_height = 50
        self.divider_thickness = 0
        self.show_checkbox_column = True
        self.sort_column_index = 4
        self.sort_ascending = True
        # self.data_row_color={"hovered": "0x30FF0000"}
                            
        self.textsize = 15
        self.Colunas_tabela()
        self.Linhas_tabela()

    def Colunas_tabela(self):
        self.columns = [ft.DataColumn(ft.Row([ft.Text(i,selectable = True,theme_style=ft.TextThemeStyle.TITLE_MEDIUM)],alignment='center')) for i in list(self.df.columns)]
        
    
    def Linhas_tabela(self):
        linhas = []
        df_lista = self.df.values.tolist()
        for l,i in enumerate(df_lista):
            cell = [ ft.DataCell(ft.Row([ft.Text(j,text_align='center',selectable = True, size = self.textsize)],alignment='center',spacing = 3,vertical_alignment='center')) for j in i]
            cor  = 'black' if l % 2 == 0 else 'white,0.01'
            linhas.append(ft.DataRow(cells = cell, color = cor))
        self.rows = linhas
            



class LayoutGuerra(ft.Row):
    def __init__(self):
        super().__init__()
        self.num_estrelas = False, False, False, True
        self.alignment=ft.MainAxisAlignment.START

        def Valor(e):
            match e.data:
                case 'poucas_0_estrelas':
                    self.num_estrelas =  True, False, False, False                
                case  'poucas_1_estrelas':
                    self.num_estrelas =  False, True, False, False                  
                case 'poucas_2_estrelas':
                    self.num_estrelas =  False, False, True, False                  
                case  'poucas_3_estrelas':
                    self.num_estrelas =  False, False, False, True   
                               

        estrelas = My_Dropdown('estrelas',Valor,'poucas_0_estrelas', 'poucas_1_estrelas', 'poucas_2_estrelas', 'poucas_3_estrelas' 
            
        )
        inverter =  ft.Checkbox(label="Inverter", value=False) 
        metodo = My_Dropdown('Método',None, 1,2,3,4)
        metodo.width = 100
        rodar =ft.ElevatedButton('Rodar')
        parar =ft.ElevatedButton('parar')
        gerar_mapa =ft.ElevatedButton('gerar_mapa')
        resultado2 =ft.ElevatedButton('resultado2')
        self.saida = ft.Text('')
        
        df = pd.DataFrame({'Jogador':list(range(15)), 'Vila':list(range(15)), 'Estrelas': list(range(15))})

        tabela = My_tabela(df)
        self.controls = [
            ft.Column([
                ft.Row([estrelas, inverter,metodo]),
                ft.Row([rodar, resultado2,gerar_mapa,]),
                parar,
                ft.Container(content = ft.Column([self.saida], auto_scroll=True, scroll=ft.ScrollMode.ADAPTIVE,height = 400, width=350), bgcolor='white,0.01')
            ],alignment=ft.MainAxisAlignment.START, width=350),
            ft.Column([tabela])
            
        ]

    # # happens when example is added to the page (when user chooses the FilePicker control from the grid)
    # def did_mount(self):
    #     self.page.overlay.append(self.pick_files_dialog)
    #     self.page.update()

    # # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    # def will_unmount(self):
    #     self.page.overlay.remove(self.pick_files_dialog)
    #     self.page.update()





def main(page: ft.Page):
    page.window_width = 600  # Define a largura da janela como 800 pixels
    page.window_height = 660  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START
    layout = LayoutGuerra()

    def print(texto):
        layout.saida.value += f'{texto}\n'
        layout.saida.update()

    page.add(layout)




ft.app(main,
    #    view = ft.AppView.WEB_BROWSER
    # port = 8050
       )