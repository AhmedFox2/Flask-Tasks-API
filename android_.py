import flet as ft
import requests

API_URL = "http://127.0.0.1:5000/tasks"  # غيّر الرابط حسب API الخاص بك

def main(page: ft.Page):
    page.title = "مهامي"
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 600
    page.padding = 20
    page.scroll = "auto"

    input_task = ft.TextField(
        hint_text="اكتب اسم المهمة",
        text_align=ft.TextAlign.RIGHT,
        expand=True
    )

    task_list = ft.Column(spacing=10)

    status_text = ft.Text("", color="red", text_align=ft.TextAlign.RIGHT)

    def load_tasks():
        task_list.controls.clear()
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                tasks = response.json()
                for task_id, task in tasks.items():
                    task_item = ft.Text(task["title"], text_align=ft.TextAlign.RIGHT)
                    task_list.controls.append(task_item)
                status_text.value = ""
            else:
                status_text.value = "فشل في تحميل المهام"
        except Exception as e:
            status_text.value = f"خطأ في الاتصال: {e}"
        page.update()

    def add_task(e):
        title = input_task.value.strip()
        if not title:
            status_text.value = "يرجى إدخال اسم المهمة"
            page.update()
            return

        data = {"title": title, "done": False}
        try:
            r = requests.post(API_URL, json=data)
            if r.status_code == 201:
                input_task.value = ""
                load_tasks()
                status_text.value = "تمت الإضافة"
            else:
                status_text.value = "فشل في إضافة المهمة"
        except Exception as e:
            status_text.value = f"خطأ في الاتصال: {e}"
        page.update()

    page.add(
        ft.Column([
            ft.Text("قائمة المهام", size=24, weight="bold", text_align=ft.TextAlign.RIGHT),
            input_task,
            ft.Row([
                ft.ElevatedButton("إضافة المهمة", on_click=add_task),
                ft.ElevatedButton("تحديث", on_click=lambda e: load_tasks()),
            ], alignment="spaceBetween"),
            status_text,
            ft.Divider(),
            task_list,
        ], alignment=ft.MainAxisAlignment.START, spacing=20)
    )

    load_tasks()

ft.app(target=main)
