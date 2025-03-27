import tkinter as tk
from tkinter import messagebox
import random

class RandomPicker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("随机点名系统")
        self.window.geometry("400x300")
        
        # 学生名单
        self.students = ["张三"]  # 可以修改为实际的学生名单
        self.used_students = []
        
        # 创建界面元素
        self.title_label = tk.Label(self.window, text="课堂随机点名", font=("黑体", 20))
        self.title_label.pack(pady=20)
        
        self.result_label = tk.Label(self.window, text="等待抽取...", font=("宋体", 16))
        self.result_label.pack(pady=30)
        
        self.pick_button = tk.Button(self.window, text="抽取学生", command=self.pick_student)
        self.pick_button.pack()
        
        self.reset_button = tk.Button(self.window, text="重置名单", command=self.reset_list)
        self.reset_button.pack(pady=10)
        
    def pick_student(self):
        if len(self.students) == len(self.used_students):
            messagebox.showinfo("提示", "所有学生都已被抽取过，请重置名单！")
            return
            
        while True:
            student = random.choice(self.students)
            if student not in self.used_students:
                self.used_students.append(student)
                self.result_label.config(text=f"被抽中的学生是：{student}")
                break
    
    def reset_list(self):
        self.used_students = []
        self.result_label.config(text="等待抽取...")
        messagebox.showinfo("提示", "名单已重置！")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = RandomPicker()
    app.run()
