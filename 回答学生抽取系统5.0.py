import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random
import json
import os
from datetime import datetime

class RandomPicker:
    VERSION = "5.0"
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"随机点名系统 v{self.VERSION}")
        self.window.geometry("1000x600")
        
        # 配置窗口网格权重
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # 配置文件
        self.config_file = "students_list.json"
        self.history_folder = "history_records"
        
        # 确保历史记录文件夹存在
        if not os.path.exists(self.history_folder):
            os.makedirs(self.history_folder)
        
        # 加载配置
        self.load_config()
        
        # 当前历史记录
        self.current_history_file = None
        self.used_students = []
        self.history_visible = True
        
        self.create_gui()
        # 延迟显示版本信息，确保窗口已经完全创建
        self.window.after(100, self.show_version_info)
    
    def create_gui(self):
        # 创建主要面板，设置最小宽度
        self.main_frame = tk.PanedWindow(self.window, orient=tk.HORIZONTAL, sashwidth=5)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板
        left_frame = tk.Frame(self.main_frame, width=450)
        left_frame.pack_propagate(False)
        self.main_frame.add(left_frame)
        
        # 右侧面板
        self.right_frame = tk.Frame(self.main_frame)
        self.main_frame.add(self.right_frame)
        
        # 左侧界面元素
        self.title_label = tk.Label(left_frame, text="课堂随机点名", font=("黑体", 24))
        self.title_label.pack(pady=20)
        
        self.result_label = tk.Label(left_frame, text="等待抽取...", 
                                   font=("宋体", 20), 
                                   wraplength=380)
        self.result_label.pack(pady=30)
        
        # 按钮框架
        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=10)
        
        self.pick_button = tk.Button(button_frame, text="抽取学生", 
                                   command=self.pick_student,
                                   width=12, height=2,
                                   font=("宋体", 12))
        self.pick_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="重置名单", 
                                    command=self.reset_list,
                                    width=12, height=2,
                                    font=("宋体", 12))
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # 历史记录操作按钮
        history_ops_frame = tk.Frame(left_frame)
        history_ops_frame.pack(pady=10)
        
        self.save_history_button = tk.Button(history_ops_frame, text="保存当前记录", 
                                           command=self.save_current_history,
                                           width=12, height=2,
                                           font=("宋体", 12))
        self.save_history_button.pack(side=tk.LEFT, padx=5)
        
        self.load_history_button = tk.Button(history_ops_frame, text="加载历史记录", 
                                           command=self.load_history_file,
                                           width=12, height=2,
                                           font=("宋体", 12))
        self.load_history_button.pack(side=tk.LEFT, padx=5)
        
        # 添加导入名单按钮
        self.import_button = tk.Button(history_ops_frame, text="导入名单", 
                                     command=self.import_students,
                                     width=12, height=2,
                                     font=("宋体", 12))
        self.import_button.pack(side=tk.LEFT, padx=5)
        
        # 添加折叠按钮
        self.toggle_history_button = tk.Button(history_ops_frame, text="隐藏历史栏", 
                                             command=self.toggle_history_panel,
                                             width=12, height=2,
                                             font=("宋体", 12))
        self.toggle_history_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(left_frame, text="退出程序", 
                                   command=self.quit_program,
                                   width=12, height=2,
                                   font=("宋体", 12))
        self.quit_button.pack(pady=20)
        
        # 右侧历史记录
        history_label = tk.Label(self.right_frame, text="抽取历史记录", font=("黑体", 20))
        history_label.pack(pady=10)
        
        # 调整历史记录文本框
        self.history_text = tk.Text(self.right_frame, width=40, height=30, 
                                  font=("宋体", 14))
        self.history_text.pack(side=tk.LEFT, pady=10, padx=5, 
                             fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.right_frame, command=self.history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        # 禁止编辑历史记录
        self.history_text.config(state='disabled')
        
        # 绑定快捷键
        self.window.bind('<Return>', lambda event: self.pick_student())
        self.window.bind('<Escape>', lambda event: self.quit_program())
    
    def show_version_info(self):
        """显示版本信息"""
        messagebox.showinfo("版本信息", 
                          f"随机点名系统 v{self.VERSION}\n"
                          f"更新日期：{datetime.now().strftime('%Y-%m-%d')}\n"
                          "新功能：\n"
                          "- 支持导入外部学生名单\n"
                          "  - 支持TXT文本格式（每行一个名字）\n"
                          "  - 支持JSON格式\n"
                          "- 优化了用户界面\n"
                          "- 改进了错误提示\n"
                          "- 支持历史记录管理\n"
                          "- 支持历史栏显示切换")
    
    def toggle_history_panel(self):
        """切换历史记录面板的显示状态"""
        if self.history_visible:
            self.main_frame.remove(self.right_frame)
            self.toggle_history_button.config(text="显示历史栏")
            self.history_visible = False
            self.window.geometry("550x600")
        else:
            self.main_frame.add(self.right_frame)
            self.toggle_history_button.config(text="隐藏历史栏")
            self.history_visible = True
            self.window.geometry("1000x600")
    
    def import_students(self):
        """导入学生名单"""
        filepath = filedialog.askopenfilename(
            title="选择学生名单文件",
            filetypes=(
                ("文本文件", "*.txt"),
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            )
        )
        
        if not filepath:
            return
            
        try:
            if filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        new_students = data
                    elif isinstance(data, dict) and 'students' in data:
                        new_students = data['students']
                    else:
                        raise ValueError("JSON文件格式不正确")
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    new_students = [name.strip() for name in f.readlines() if name.strip()]
            
            if not new_students:
                raise ValueError("没有找到有效的学生名单")
            
            if messagebox.askyesno("确认", 
                                 f"找到 {len(new_students)} 个学生名字。\n是否替换现有名单？\n"
                                 "注意：这将清空当前的抽取记录。"):
                self.students = new_students
                self.save_config()
                self.reset_list()
                messagebox.showinfo("成功", f"已导入 {len(self.students)} 个学生名字")
                
        except Exception as e:
            messagebox.showerror("错误", f"导入名单时出错：\n{str(e)}")
    
    def save_current_history(self):
        """保存当前历史记录"""
        if not self.used_students:
            messagebox.showwarning("警告", "当前没有历史记录可保存！")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"history_{timestamp}.json"
        filepath = os.path.join(self.history_folder, filename)
        
        try:
            history_data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'used_students': self.used_students
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("成功", "历史记录已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存历史记录时出错：{str(e)}")
    
    def load_history_file(self):
        """加载历史记录文件"""
        filepath = filedialog.askopenfilename(
            initialdir=self.history_folder,
            title="选择历史记录文件",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*"))
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                
            self.used_students = history_data['used_students']
            timestamp = history_data.get('timestamp', '未知时间')
            
            self.history_text.config(state='normal')
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, f"加载的历史记录 ({timestamp})：\n\n")
            for i, student in enumerate(self.used_students, 1):
                self.history_text.insert(tk.END, f"第{i}次抽取：{student}\n")
            self.history_text.config(state='disabled')
            
            self.current_history_file = filepath
            messagebox.showinfo("成功", "历史记录已加载！")
        except Exception as e:
            messagebox.showerror("错误", f"加载历史记录时出错：{str(e)}")
    
    def pick_student(self):
        try:
            if len(self.used_students) >= len(self.students):
                messagebox.showinfo("提示", "所有学生都已被抽取过，请重置名单！")
                self.result_label.config(text="请重置名单后继续...")
                return
                
            available_students = [s for s in self.students if s not in self.used_students]
            student = random.choice(available_students)
            self.used_students.append(student)
            
            self.result_label.config(text=f"被抽中的学生是：{student}")
            
            self.history_text.config(state='normal')
            if len(self.used_students) == 1:
                self.history_text.delete(1.0, tk.END)
                self.history_text.insert(tk.END, f"当前抽取记录 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})：\n\n")
            self.history_text.insert(tk.END, f"第{len(self.used_students)}次抽取：{student}\n")
            self.history_text.see(tk.END)
            self.history_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")
    
    def reset_list(self):
        if messagebox.askyesno("确认", "确定要重置名单吗？\n当前记录将被清空。"):
            self.used_students = []
            self.result_label.config(text="等待抽取...")
            self.history_text.config(state='normal')
            self.history_text.delete(1.0, tk.END)
            self.history_text.config(state='disabled')
            self.current_history_file = None
            messagebox.showinfo("提示", "名单已重置！")
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.students = config.get('students', [])
            else:
                self.students = ["孙家扬", "杨烨琦", "王来志", "陈浩宇", "陈欣虎", "陈正昊", "程勋虎", 
                               "段程逸","段冀嘉妮","段雨泽","刘煜玟","张金祥","张心亦","宗彦孜",
                               "皮晨曦","祁梓赫","李思佳","戈慧慧","王赛","余依依","关可可","李伟杰",
                               "李露阳","闫佩佩","蒋彦妮","祁浩楠","王雨菲","孙雅婷","钟翊翔","陶佳怡",
                               "平凌香","平一诺","方美琪","王旭","杨佳欣","刘子翔","刘若萱","黄淑婷",
                               "金康富","徐凯文","刘国庆","顾嘉乐","刘宇航","李浩然","孔祥锐","孙浩诚"]
                self.save_config()
        except Exception as e:
            messagebox.showerror("错误", f"加载配置文件时出错：{str(e)}")
            self.students = []
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'students': self.students}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件时出错：{str(e)}")
    
    def quit_program(self):
        if messagebox.askokcancel("确认", "确定要退出程序吗？\n未保存的记录将丢失。"):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = RandomPicker()
    app.run()
