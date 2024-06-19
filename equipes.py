


import json
import flet as ft

class ConfirmarSaida:
    def __init__(self,page, funcao = None):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.on_window_event = self.window_event
        self.page.window_prevent_close = True 
   


    def window_event(self, e):
            if e.data == "close":
                self.page.dialog = self.confirm_dialog
                
                self.confirm_dialog.open = True
                self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window_destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()

class Resize:
    def __init__(self,page):
        self.page = page
        self.page.on_resize = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
        self.page.overlay.append(self.pw)   

    def page_resize(self, e):
        self.pw.value = f"{self.page.window_width}*{self.page.window_height} px"
        self.pw.update()

  
class Saida(ft.Column):
    def __init__(self):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad],auto_scroll = True, height=150,  ),bgcolor='white,0.03' ))
    def pprint(self, *texto):
        for i in list(texto):
            self.saidad.value += f'{i}\n'  
        self.page.update()

class layout_equipes(ft.Column):
    def __init__(self, printt = None, page = None):
        super().__init__()
        self.printt = printt
        self.page = page
        equipe_A = {
            "GRUPO ELITE": "1298",  # 3 em cv14-, 2 em cv15+
            "GRUPO A": "1060",  # 3 em cv13-, 2 em cv13+
            "GRUPO B": "910",  # 3 em cv12-, 2 em cv12+
            "GRUPO C": "840",  # 3 em cv11-, 2 em cv12 e cv13, 1 + cv expoto em cv14+            
            "GRUPO D": "800",# 3 em cv10-, 2 em cv11 e cv12, 1 + cv expoto em cv13, 1 em cv14 se cv exposto            
            "GRUPO E": "500"# 3 em cv9-, 2 em cv10, 1 + cv expoto em cv11, 1 em cv12, 1 em cv13 se cv exposto
        }
        self.GRUPO_ELITE = ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.Salvar)
        self.GRUPO_A = ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.Salvar)
        self.GRUPO_B = ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.Salvar)
        self.GRUPO_C = ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.Salvar)
        self.GRUPO_D = ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.Salvar)
        self.GRUPO_E = ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.Salvar)
        self.controls = [
            ft.Row([ft.Text("GRUPO ELITE"),self.GRUPO_ELITE,ft.Text('3 em cv14-, 2 em cv15+', size = 13, color='white,0.6')]),
            ft.Row([ft.Text("GRUPO A      "),self.GRUPO_A,ft.Text('3 em cv13-, 2 em cv13+', size = 13, color='white,0.6')]),
            ft.Row([ft.Text("GRUPO B      "),self.GRUPO_B,ft.Text('3 em cv12-, 2 em cv12+', size = 13, color='white,0.6')]),
            ft.Row([ft.Text("GRUPO C      "),self.GRUPO_C,ft.Text('3 em cv11-, 2 em cv12 e cv13, 1 + cv expoto em cv14+', size = 13, color='white,0.6')]),
            ft.Row([ft.Text("GRUPO D      "),self.GRUPO_D,ft.Text('3 em cv10-, 2 em cv11 e cv12, 1 + cv expoto em cv13, 1 em cv14 se cv exposto', size = 13, color='white,0.6')]),
            ft.Row([ft.Text("GRUPO E      "),self.GRUPO_E,ft.Text('3 em cv9-, 2 em cv10, 1 + cv expoto em cv11, 1 em cv12, 1 em cv13 se cv exposto', size = 13, color='white,0.6')]),
        ]
        self.Iniciar()


    def Iniciar(self):
        try:
            self.arquiv = self.Ler_json('config_guerra')
            self.GRUPO_ELITE.value =  self.arquiv[ "equipe A"]["GRUPO ELITE"]
            self.GRUPO_A.value =  self.arquiv[ "equipe A"]["GRUPO A"]
            self.GRUPO_B.value =  self.arquiv[ "equipe A"]["GRUPO B"]
            self.GRUPO_C.value =  self.arquiv[ "equipe A"]["GRUPO C"]
            self.GRUPO_D.value =  self.arquiv[ "equipe A"]["GRUPO D"]
            self.GRUPO_E.value =  self.arquiv[ "equipe A"]["GRUPO E"]
        except:
            self.arquiv =  {"equipe A": {
                            "Nome da Equipe": "equipe A",
                            "GRUPO ELITE": "1093",
                            "GRUPO A": "1000",
                            "GRUPO B": "840",
                            "GRUPO C": "790",
                            "GRUPO D": "700",
                            "GRUPO E": "500"}
                        }
            self.Escrever_json(self.arquiv,'config_guerra')
            self.GRUPO_ELITE.value =  self.arquiv[ "equipe A"]["GRUPO ELITE"]
            self.GRUPO_A.value =  self.arquiv[ "equipe A"]["GRUPO A"]
            self.GRUPO_B.value =  self.arquiv[ "equipe A"]["GRUPO B"]
            self.GRUPO_C.value =  self.arquiv[ "equipe A"]["GRUPO C"]
            self.GRUPO_D.value =  self.arquiv[ "equipe A"]["GRUPO D"]
            self.GRUPO_E.value =  self.arquiv[ "equipe A"]["GRUPO E"]            


    def Salvar(self,e):
        self.arquiv = self.Ler_json('config_guerra')

        self.arquiv[ "equipe A"]["GRUPO ELITE"] = self.GRUPO_ELITE.value  
        self.arquiv[ "equipe A"]["GRUPO A"] = self.GRUPO_A.value 
        self.arquiv[ "equipe A"]["GRUPO B"] = self.GRUPO_B.value 
        self.arquiv[ "equipe A"]["GRUPO C"]  = self.GRUPO_C.value
        self.arquiv[ "equipe A"]["GRUPO D"] = self.GRUPO_D.value
        self.arquiv[ "equipe A"]["GRUPO E"]  = self.GRUPO_E.value                   
        
        self.Escrever_json(self.arquiv, 'config_guerra')
        print('Configurações salvas com sucesso')






    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'w') as f2:
            json.dump(nomedodicionario, f2, indent=4)

    def Ler_json(self, nomedoarquivo):  # retorna um dicionário
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'r') as f2:
            try:
                a = json.load(f2)
                return a
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                return {}

def main(page: ft.Page):
    page.window_width = 700  # Define a largura da janela como 800 pixels
    page.window_height = 350  #    
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START  
    ConfirmarSaida(page)
    saida = Saida() 

    Resize(page) 
    e =  layout_equipes( printt = saida.pprint, page = page)    
    page.add(e)




if __name__ == '__main__':    
    ft.app(main) 
