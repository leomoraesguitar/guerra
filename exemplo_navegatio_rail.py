import flet as ft



class TabeVertical(ft.Row):
    def __init__(self,  funcao = None, *controls):#controles = ['nome', icone, control]
        super().__init__()
        self.funcao = funcao
        self.controls = list(controls)
        self.barra = ft.NavigationRail(
            selected_index=0,
            min_width=50,
            min_extended_width=400,
            group_alignment=-0.9,
            on_change = self.func
        )


        if len(self.controls) >0:
           for i in self.controls:    
                self.barra.destinations.append(ft.NavigationRailDestination(label=i[0], icon=i[1]))


    def Add(self, nome, icone):
        # self.tabs.append(ft.NavigationRailDestination((icon=icone,content=janela )))
        try:
            self.update()
        except:
             pass

    def func(self,e):
        # self.funcao(e)
        match e.control.selected_index:
            case 0:
                pass
        # pass


def main(page: ft.Page):
    def s(e):
        print(e.control.selected_index)
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=50,
        min_extended_width=400,
        # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, 
                # selected_icon=ft.icons.FAVORITE, 
                label="First",
                # ref = 'casa'

            ),
            # ft.NavigationRailDestination(
            #     icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
            #     selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
            #     label="Second",
            # ),
            # ft.NavigationRailDestination(
            #     icon=ft.icons.SETTINGS_OUTLINED,
            #     selected_icon_content=ft.Icon(ft.icons.SETTINGS),
            #     label_content=ft.Text("Settings"),
            # ),
        ],
        on_change=s,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )

ft.app(target=main)