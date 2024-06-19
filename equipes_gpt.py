import json
import flet as ft

class ConfirmarSaida:
    def __init__(self, page, funcao=None):
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

    def yes_click(self, e):
        if self.funcao:
            self.funcao(e)
        self.page.window_destroy()

    def no_click(self, e):
        self.confirm_dialog.open = False
        self.page.update()

class Resize:
    def __init__(self, page):
        self.page = page
        self.page.on_resize = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
        self.page.overlay.append(self.pw)

    def page_resize(self, e):
        self.pw.value = f"{self.page.window_width}*{self.page.window_height} px"
        self.pw.update()

class Saida(ft.Column):
    def __init__(self):
        super().__init__()
        self.saidad = ft.Text('', selectable=True)
        self.controls.append(ft.Container(ft.ListView([self.saidad], auto_scroll=True, height=150), bgcolor='white,0.03'))

    def pprint(self, *texto):
        for i in texto:
            self.saidad.value += f'{i}\n'
        self.page.update()

class LayoutEquipes(ft.Column):
    def __init__(self, printt=None, page=None):
        super().__init__()
        self.printt = printt
        self.page = page
        self.equipe_fields = {
            "GRUPO ELITE": ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO A": ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO B": ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO C": ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO D": ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.salvar),
            "GRUPO E": ft.TextField(width=70, dense=True, content_padding=10, bgcolor='white,0.08', on_change=self.salvar),
        }
        self.controls = [
            ft.Row([ft.Text(name), field, ft.Text(details, size=13, color='white,0.6')]) 
            for name, field, details in [
                ("GRUPO ELITE", self.equipe_fields["GRUPO ELITE"], '3 em cv14-, 2 em cv15+'),
                ("GRUPO A", self.equipe_fields["GRUPO A"], '3 em cv13-, 2 em cv13+'),
                ("GRUPO B", self.equipe_fields["GRUPO B"], '3 em cv12-, 2 em cv12+'),
                ("GRUPO C", self.equipe_fields["GRUPO C"], '3 em cv11-, 2 em cv12 e cv13, 1 + cv expoto em cv14+'),
                ("GRUPO D", self.equipe_fields["GRUPO D"], '3 em cv10-, 2 em cv11 e cv12, 1 + cv expoto em cv13, 1 em cv14 se cv exposto'),
                ("GRUPO E", self.equipe_fields["GRUPO E"], '3 em cv9-, 2 em cv10, 1 + cv expoto em cv11, 1 em cv12, 1 em cv13 se cv exposto'),
            ]
        ]
        self.iniciar()

    def iniciar(self):
        self.arquiv = self.ler_json('config_guerra', default={
            "equipe A": {
                "Nome da Equipe": "equipe A",
                "GRUPO ELITE": "1093",
                "GRUPO A": "1000",
                "GRUPO B": "840",
                "GRUPO C": "790",
                "GRUPO D": "700",
                "GRUPO E": "500"
            }
        })
        for key in self.equipe_fields:
            self.equipe_fields[key].value = self.arquiv["equipe A"].get(key, "")

    def salvar(self, e):
        self.arquiv = self.ler_json('config_guerra')
        for key, field in self.equipe_fields.items():
            self.arquiv["equipe A"][key] = field.value
        self.escrever_json(self.arquiv, 'config_guerra')
        print('Configurações salvas com sucesso')

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default or {}

def main(page: ft.Page):
    page.window_width = 700
    page.window_height = 350
    page.title = "Guerra de Clans"
    page.vertical_alignment = ft.MainAxisAlignment.START
    ConfirmarSaida(page)
    saida = Saida()
    Resize(page)
    layout = LayoutEquipes(printt=saida.pprint, page=page)
    page.add(layout)

if __name__ == '__main__':
    ft.app(main)
