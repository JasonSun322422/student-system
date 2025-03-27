import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class RandomPicker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("随机点名系统")
        self.window.geometry("600x500")
        
        # 学生名单
        self.students = ["张三"]
        self.used_students = []
        
        # 创建左侧面板
        left_frame = tk.Frame(self.window)
        left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)
        
        # 创建右侧面板（用于历史记录）
        right_frame = tk.Frame(self.window)
        right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # 左侧界面元素
        self.title_label = tk.Label(left_frame, text="课堂随机点名", font=("黑体", 20))
        self.title_label.pack(pady=20)
        
        self.result_label = tk.Label(left_frame, text="等待抽取...", font=("宋体", 16))
        self.result_label.pack(pady=30)
        
        self.pick_button = tk.Button(left_frame, text="抽取学生", command=self.pick_student)
        self.pick_button.pack()
        
        self.reset_button = tk.Button(left_frame, text="重置名单", command=self.reset_list)
        self.reset_button.pack(pady=10)
        
        self.quit_button = tk.Button(left_frame, text="退出程序", command=self.quit_program)
        self.quit_button.pack(pady=10)
        
        # 右侧历史记录
        history_label = tk.Label(right_frame, text="抽取历史记录", font=("黑体", 16))
        history_label.pack(pady=10)
        
        # 创建历史记录文本框
        self.history_text = tk.Text(right_frame, width=30, height=20, font=("宋体", 12))
        self.history_text.pack(pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(right_frame, command=self.history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        # 禁止编辑历史记录
        self.history_text.config(state='disabled')
        
    def pick_student(self):
        try:
            # 检查是否所有学生都已被抽取
            if len(self.used_students) >= len(self.students):
                messagebox.showinfo("提示", "所有学生都已被抽取过，请重置名单！")
                self.result_label.config(text="请重置名单后继续...")
                return
                
            # 从未被抽取的学生中随机选择一个
            available_students = [s for s in self.students if s not in self.used_students]
            student = random.choice(available_students)
            self.used_students.append(student)
            
            # 更新当前抽取结果
            self.result_label.config(text=f"被抽中的学生是：{student}")
            
            # 更新历史记录
            self.history_text.config(state='normal')
            self.history_text.insert(tk.END, f"第{len(self.used_students)}次抽取：{student}\n")
            self.history_text.see(tk.END)  # 自动滚动到最新记录
            self.history_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")
    
    def reset_list(self):
        self.used_students = []
        self.result_label.config(text="等待抽取...")
        # 清空历史记录
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state='disabled')
        messagebox.showinfo("提示", "名单已重置！")
    
    def quit_program(self):
        if messagebox.askokcancel("确认", "确定要退出程序吗？"):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = RandomPicker()
    app.run()
