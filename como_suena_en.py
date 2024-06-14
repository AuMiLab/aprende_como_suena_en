import flet as ft
import librosa as lib
import os

url = os.path.join(os.getcwd(), "respuestas/ref.wav")

def main(page: ft.Page):

    respuestas = ["Ancud","Aula Magna","Catedral","Reverberante"]
    conv = {}
    selected_files = ft.Text()
    selected_filesz = ft.Text(value='HelloWorld')
    audio1 = ft.Audio(
        src=[f for f in selected_filesz.value][0],  # Inicialmente sin fuente
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    ) 
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)
                      ) if e.files else "Cancelled!"
        )
        selected_filesz.value = (f.path for f in e.files)
        audio1.src = [f for f in selected_filesz.value][0]
        audio1.update()
        page.update()

    def volume_down(_):
        audio1.volume -= 0.1
        audio1.update()

    def volume_up(_):
        audio1.volume += 0.1
        audio1.update()

    def close_anchor(e):
        text = f"Recinto {e.control.data}"
        print(f"closing view from {text}")
        anchor.close_view(text)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    def select_convolve(e):
        recinto = e.value
        r,fs1 = lib.load(conv[recinto])

    anchor = ft.SearchBar(
        view_elevation=len(respuestas),
        divider_color=ft.colors.AMBER,
        bar_hint_text="Elige recinto...",
        view_hint_text="Elige un recinto para escuchar",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f), on_click=close_anchor, data=f)
            for f in respuestas
        ],
    )

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    audio1 = ft.Audio(
        src=[f for f in selected_filesz.value][0],  # Inicialmente sin fuente
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: print("Loaded"),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_state_changed=lambda e: print("State changed:", e.data),
        on_seek_complete=lambda _: print("Seek complete"),
    )
    page.overlay.append(pick_files_dialog)
    page.overlay.append(audio1)
    
    page.add(
        ft.ElevatedButton(
            "Pick file",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False)
        ),
        selected_files,
        ft.Row(
            [
                ft.ElevatedButton("Play", on_click=lambda _: audio1.play()),
                ft.ElevatedButton("Pause", on_click=lambda _: audio1.pause())
            ]
        ),
        ft.Row(
            [
                ft.ElevatedButton("Volume down", on_click=volume_down),
                ft.ElevatedButton("Volume up", on_click=volume_up),
            ]
        ),
    )
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    "Recintos",
                    on_click=lambda _: anchor.open_view(),
                ),
            ],
        ),
        anchor,
        ft.Row(
            [
                ft.ElevatedButton("Como sonará?", on_click=lambda _: select_convolve(anchor)), 
                ft.ElevatedButton("a", on_click=lambda _: audio2.play())
            ])
    )

ft.app(target=main)
