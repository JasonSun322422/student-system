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
        self.students = ["孙家扬", "杨烨琦", "王来志", "陈浩宇", "陈欣虎", "陈正昊", "程勋虎", "段程逸","段冀嘉妮","段雨泽","刘煜玟","张金祥","张心亦","宗彦孜","皮晨曦","祁梓赫","李思佳","戈慧慧","王赛","余依依","关可可","李伟杰","李露阳","闫佩佩","蒋彦妮","祁浩楠","王雨菲","孙雅婷","钟翊翔","陶佳怡","平凌香","平一诺","方美琪","王旭","杨佳欣","刘子翔","刘若萱","黄淑婷","金康富","徐凯文","刘国庆","顾嘉乐","刘宇航","李浩然","孔祥锐","孙浩诚"]
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
        # 添加折叠功能，默认为隐藏状态
        self.history_visible = False
        self.toggle_button = tk.Button(right_frame, text="显示历史记录", command=self.toggle_history)
        self.toggle_button.pack(pady=5)
        
        history_label = tk.Label(right_frame, text="抽取历史记录", font=("黑体", 16))
        history_label.pack(pady=10)
        
        # 创建一个框架来容纳历史记录相关的组件
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
                messagebox.showinfo("提示", "所有学生都已被抽取过��请重置名单！")
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
        if messagebox.askokcancel(title="确认", message="确定要退出程序吗？", parent=self.window):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = RandomPicker()
    app.run()
