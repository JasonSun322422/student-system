import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import json
import os

class RandomPicker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("随机点名系统")
        self.window.geometry("600x500")
        
        # 配置窗口网格权重，使其能够自适应调整大小
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # 加载配置文件
        self.config_file = "students_list.json"
        self.history_file = "history.json"
        self.load_config()
        
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
        self.history_visible = False
        self.toggle_button = tk.Button(right_frame, text="显示历史记录", command=self.toggle_history)
        self.toggle_button.pack(pady=5)
        
        history_label = tk.Label(right_frame, text="抽取历史记录", font=("黑体", 16))
        history_label.pack(pady=10)
        
        # 创建历史记录框架
        self.history_frame = tk.Frame(right_frame)
        
        # 创建历史记录文本框
        self.history_text = tk.Text(self.history_frame, width=30, height=20, font=("宋体", 12))
        self.history_text.pack(side=tk.LEFT, pady=10, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.history_frame, command=self.history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        # 禁止编辑历史记录
        self.history_text.config(state='disabled')
        
        # 绑定快捷键
        self.window.bind('<Return>', lambda event: self.pick_student())  # 回车键抽取
        self.window.bind('<Escape>', lambda event: self.quit_program())  # ESC键退出
        
        # 加载历史记录
        self.load_history()
        
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.students = config.get('students', [])
            else:
                # 默认学生名单
                self.students = ["张三"]
                self.save_config()
            self.used_students = []
        except Exception as e:
            messagebox.showerror("错误", f"加载配置文件时出错：{str(e)}")
            self.students = []
            self.used_students = []
            
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'students': self.students}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件时出错：{str(e)}")
            
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    self.used_students = history.get('used_students', [])
                    # 恢复历史记录显示
                    self.history_text.config(state='normal')
                    for i, student in enumerate(self.used_students, 1):
                        self.history_text.insert(tk.END, f"第{i}次抽取：{student}\n")
                    self.history_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("错误", f"加载历史记录时出错：{str(e)}")
            
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({'used_students': self.used_students}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存历史记录时出错：{str(e)}")
        
    def toggle_history(self):
        if self.history_visible:
            self.history_frame.pack_forget()
            self.toggle_button.config(text="显示历史记录")
            self.history_visible = False
        else:
            self.history_frame.pack(fill=tk.BOTH, expand=True)
            self.toggle_button.config(text="隐藏历史记录")
            self.history_visible = True
        
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
            
            # 保存历史记录
            self.save_history()
            
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")
    
    def reset_list(self):
        self.used_students = []
        self.result_label.config(text="等待抽取...")
        # 清空历史记录
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state='disabled')
        # 清空历史记录文件
        self.save_history()
        messagebox.showinfo("提示", "名单已重置！")
    
    def quit_program(self):
        if messagebox.askokcancel(title="确认", message="确定要退出程序吗？", parent=self.window):
            self.save_history()  # 保存历史记录
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = RandomPicker()
    app.run()
