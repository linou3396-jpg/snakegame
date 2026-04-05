# snake_flet.py
import flet as ft
import random
import time

class SnakeGame:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "لعبة الثعبان"
        self.page.bgcolor = ft.Colors.BLACK
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.grid_size = 20
        self.cell_size = 20
        self.speed = 0.15
        
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.food = self.random_food()
        self.score = 0
        self.best_score = self.load_best_score()
        self.game_over = False
        
        self.setup_ui()
        self.start_game()
    
    def random_food(self):
        while True:
            food = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
            if food not in self.snake:
                return food
    
    def load_best_score(self):
        # بسيط - يمكن تخزينه لاحقاً
        return 0
    
    def setup_ui(self):
        # شاشة اللعبة
        self.canvas = ft.Container(
            width=self.grid_size * self.cell_size,
            height=self.grid_size * self.cell_size,
            bgcolor=ft.Colors.GREY_900,
        )
        
        # أزرار التحكم
        controls = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.icons.ARROW_UP, on_click=lambda e: self.change_direction(0, -1)),
                ft.IconButton(ft.icons.ARROW_DOWN, on_click=lambda e: self.change_direction(0, 1)),
                ft.IconButton(ft.icons.ARROW_LEFT, on_click=lambda e: self.change_direction(-1, 0)),
                ft.IconButton(ft.icons.ARROW_RIGHT, on_click=lambda e: self.change_direction(1, 0)),
            ]
        )
        
        # عرض النقاط
        self.score_text = ft.Text(f"النقاط: {self.score}", size=20, color=ft.Colors.WHITE)
        self.best_text = ft.Text(f"الأفضل: {self.best_score}", size=20, color=ft.Colors.YELLOW)
        
        self.page.add(
            ft.Column([
                ft.Row([self.score_text, self.best_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.canvas,
                controls
            ])
        )
    
    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]) and not self.game_over:
            self.direction = (dx, dy)
    
    def start_game(self):
        self.update_loop()
    
    def update_loop(self):
        if self.game_over:
            return
        
        # تحريك الثعبان
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # التحقق من أكل التفاحة
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.food = self.random_food()
            self.score += 1
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_text.value = f"الأفضل: {self.best_score}"
            self.score_text.value = f"النقاط: {self.score}"
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
        
        # التحقق من الاصطدام
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake[1:]):
            self.game_over = True
            self.show_game_over()
            return
        
        self.draw()
        
        # تحديث كل 0.15 ثانية
        self.canvas.update()
        time.sleep(self.speed)
        self.page.run_task(self.update_loop)
    
    def draw(self):
        self.canvas.content = ft.Stack([
            ft.Container(
                width=self.grid_size * self.cell_size,
                height=self.grid_size * self.cell_size,
                bgcolor=ft.Colors.BLACK,
                content=ft.GridView(
                    runs_count=self.grid_size,
                    children=self.draw_snake_and_food()
                )
            )
        ])
    
    def draw_snake_and_food(self):
        children = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = ft.Colors.GREEN if (x, y) in self.snake else ft.Colors.BLACK
                if (x, y) == self.food:
                    color = ft.Colors.RED
                children.append(
                    ft.Container(
                        width=self.cell_size,
                        height=self.cell_size,
                        bgcolor=color,
                        border=ft.border.all(1, ft.Colors.GREY)
                    )
                )
        return children
    
    def show_game_over(self):
        self.page.add(ft.Text("GAME OVER", size=30, color=ft.Colors.RED))
        restart_btn = ft.ElevatedButton("العب مرة أخرى", on_click=lambda e: self.restart())
        self.page.add(restart_btn)
        self.page.update()
    
    def restart(self):
        self.page.clean()
        SnakeGame(self.page)

def main(page: ft.Page):
    SnakeGame(page)

ft.app(target=main)
