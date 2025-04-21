from tkinter import *
import math
from calculator_engine import CalculatorEngine

class ScientificCalculatorUI:
    def __init__(self, master):
        self.master = master
        self.engine = CalculatorEngine()
        self.second_mode = False
        self.setup_ui()
        self.bind_keys()

    def setup_ui(self):
        self.master.configure(bg="#293C4A", bd=10)
        self.master.title("Scientific Calculator")
        self.master.geometry("400x600")

        self.display_font = ('Helvetica', 24, 'bold')
        self.button_font = ('Helvetica', 16, 'bold')

        self.text_input = StringVar()
        self.text_input.set("0")

        #display Frame
        display_frame = Frame(self.master, bg="#293C4A", bd=5)
        display_frame.pack(fill=X, padx=5, pady=5)
        self.text_display = Entry(
            display_frame,
            font=self.display_font,
            textvariable=self.text_input,
            bd=10,
            insertwidth=5,
            bg='#111', fg='#FFF', justify='right'
        )
        self.text_display.pack(fill=X, padx=5, pady=10)

        #button Frame
        self.button_frame = Frame(self.master, bg="#293C4A")
        self.button_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        #responsive grid
        for r in range(10):
            self.button_frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.button_frame.grid_columnconfigure(c, weight=1)

        #styles
        self.btn_special = {'bd':3,'fg':'#FFF','bg':'#222','font':self.button_font,'relief':'raised','activebackground':'#444','activeforeground':'#FFF'}
        self.btn_orange  = {'bd':3,'fg':'#FFF','bg':'#db701f','font':self.button_font,'relief':'raised','activebackground':'#ff8c38','activeforeground':'#FFF'}
        self.btn_number  = {'bd':3,'fg':'#000','bg':'#BBB','font':self.button_font,'relief':'raised','activebackground':'#DDD'}
        self.btn_operator= {'bd':3,'fg':'#FFF','bg':'#444','font':self.button_font,'relief':'raised','activebackground':'#666','activeforeground':'#FFF'}
        self.btn_equal   = {'bd':3,'fg':'#FFF','bg':'#0066cc','font':self.button_font,'relief':'raised','activebackground':'#0099ff'}
        self.btn_mode    = {'bd':3,'fg':'#FFF','bg':'#6B5B95','font':self.button_font,'relief':'raised','activebackground':'#8A7CB4','activeforeground':'#FFF'}

        self.create_buttons()

    def create_buttons(self):
        self.button_widgets = {}

        #mode-specific
        self.first_page_buttons = [
            (1,0,'2nd',self.btn_mode,self.toggle_second_mode),
            (1,1,'log₁₀',self.btn_special,lambda: self.button_special(lambda: self.engine.execute_operation(lambda x: math.log10(x) if x>0 else float('nan')))),
            (1,2,'ln',self.btn_special,lambda: self.button_special(lambda: self.engine.execute_operation(lambda x: math.log(x) if x>0 else float('nan')))),
            (1,3,'AC',self.btn_orange,self.button_clear_all),
            
            (2,0,'sin',self.btn_special,lambda: self.button_special(lambda: self.engine.execute_operation(lambda x: math.sin(math.radians(x))))),
            (2,1,'cos',self.btn_special,lambda: self.button_special(lambda: self.engine.execute_operation(lambda x: math.cos(math.radians(x))))),
            (2,2,'tan',self.btn_special,lambda: self.button_special(lambda: self.engine.execute_operation(lambda x: math.tan(math.radians(x))))),
            (2,3,'DEL',self.btn_orange,self.button_delete),
            
            (3,0,'√',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.sqrt(v) if v>=0 else float('nan'))())),
            (3,1,'x²',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: v**2)())),
            (3,2,'10ˣ',self.btn_special,lambda: self.button_input('10^')),
            (3,3,'1/x',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: 1/v if v!=0 else float('nan'))())),
            
            (4,0,'x!',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.factorial(int(v)) if v>=0 and v==int(v) else float('nan'))())),
            (4,1,'eˣ',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.exp(v))())),
            (4,2,'e',self.btn_special,lambda: self.button_input(str(math.e))),
            (4,3,'π',self.btn_special,lambda: self.button_input(str(math.pi)))
        ]
        self.second_page_buttons = [
            (1,0,'2nd',self.btn_mode,self.toggle_second_mode),
            (1,1,'logᵧx',self.btn_special,lambda: self.button_set_pending('logyx')),
            (1,2,'ln',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.log(v) if v>0 else float('nan'))())),
            (1,3,'AC',self.btn_orange,self.button_clear_all),
            
            (2,0,'sin',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.sin(math.radians(v)))())),
            (2,1,'cos',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.cos(math.radians(v)))())),
            (2,2,'tan',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.tan(math.radians(v)))())),
            (2,3,'DEL',self.btn_orange,self.button_delete),
            
            (3,0,'ʸ√x',self.btn_special,lambda: self.button_set_pending('nth_root')),
            (3,1,'xʸ',self.btn_special,lambda: self.button_input('^')),
            (3,2,'10ˣ',self.btn_special,lambda: self.button_input('10^')),
            (3,3,'1/x',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: 1/v if v!=0 else float('nan'))())),
            
            (4,0,'x!',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: math.factorial(int(v)) if v>=0 and v==int(v) else float('nan'))())),
            (4,1,'|x|',self.btn_special,lambda: self.button_special(lambda x=None: self.engine.execute_operation(lambda v: abs(v))())),
            (4,2,'e',self.btn_special,lambda: self.button_input(str(math.e))),
            (4,3,'π',self.btn_special,lambda: self.button_input(str(math.pi)))
        ]
        self.common_buttons = [
            (5,0,'(',self.btn_operator,lambda: self.button_input('(')),
            (5,1,')',self.btn_operator,lambda: self.button_input(')')),
            (5,2,'%',self.btn_operator,self.button_percent),
            (5,3,'÷',self.btn_operator,lambda: self.button_input('/')),

            (6,0,'7',self.btn_number,lambda: self.button_input('7')),
            (6,1,'8',self.btn_number,lambda: self.button_input('8')),
            (6,2,'9',self.btn_number,lambda: self.button_input('9')),
            (6,3,'×',self.btn_operator,lambda: self.button_input('*')),

            (7,0,'4',self.btn_number,lambda: self.button_input('4')),
            (7,1,'5',self.btn_number,lambda: self.button_input('5')),
            (7,2,'6',self.btn_number,lambda: self.button_input('6')),
            (7,3,'−',self.btn_operator,lambda: self.button_input('-')),

            (8,0,'1',self.btn_number,lambda: self.button_input('1')),
            (8,1,'2',self.btn_number,lambda: self.button_input('2')),
            (8,2,'3',self.btn_number,lambda: self.button_input('3')),
            (8,3,'+',self.btn_operator,lambda: self.button_input('+')),

            (9,0,'0',self.btn_number,lambda: self.button_input('0')),
            (9,1,'.',self.btn_number,lambda: self.button_input('.')),
            (9,2,'±',self.btn_operator,self.button_sign_change),
            (9,3,'=',self.btn_equal,self.button_equal)
        ]
        self.update_page_buttons()

    def update_page_buttons(self):
        #clear rows 1-4
        for r in range(1,5):
            for c in range(4):
                for w in self.button_frame.grid_slaves(row=r, column=c):
                    w.destroy()
        #draw mode-specific
        active = self.second_mode and self.second_page_buttons or self.first_page_buttons
        for r,c,t,st,cmd in active:
            btn = Button(self.button_frame, text=t, command=cmd, **st)
            btn.grid(row=r, column=c, sticky='nesw', padx=2, pady=2)
            self.button_widgets[(r,c)] = btn
        #draw common
        for r,c,t,st,cmd in self.common_buttons:
            for w in self.button_frame.grid_slaves(row=r,column=c): w.destroy()
            btn = Button(self.button_frame, text=t, command=cmd, **st)
            btn.grid(row=r, column=c, sticky='nesw', padx=2, pady=2)
            self.button_widgets[(r,c)] = btn

    def update_display(self):
        expr = self.engine.current_expression
        if expr == str(math.pi):
            self.text_input.set("π")
        elif expr == str(math.e):
            self.text_input.set("e")
        else:
            self.text_input.set(expr)

    def button_input(self, char):
        self.engine.append_to_expression(char)
        self.update_display()

    def button_sign_change(self):
        self.engine.change_sign_of_last_number()
        self.update_display()

    def button_clear_all(self):
        self.engine.clear_all()
        self.update_display()

    def button_delete(self):
        self.engine.delete_last()
        self.update_display()

    def button_equal(self):
        self.engine.evaluate()
        self.update_display()

    def button_percent(self):
        self.engine.percent()
        self.update_display()

    def button_special(self, func):
        func()
        self.update_display()

    def button_set_pending(self, op):
        self.engine.set_pending_operation(op)
        self.update_display()

    def toggle_second_mode(self):
        self.master.after(50, self._animate_toggle)

    def _animate_toggle(self):
        self.second_mode = not self.second_mode
        self.update_page_buttons()

    def bind_keys(self):
        self.master.bind("<Key>", self.key_handler)

    def key_handler(self, event):
        char = event.char
        key = event.keysym.lower()
        if char in '0123456789.()+-*/^': self.button_input(char)
        elif key == 'return': self.button_equal()
        elif key == 'backspace': self.button_delete()
        elif key == 'q': self.button_special(lambda: self.engine.execute_operation(lambda x: x**2)())
        elif key == 'r': self.button_special(lambda: self.engine.execute_operation(lambda x: 1/x if x!=0 else float('nan'))())
        elif key == 't': self.button_special(lambda: self.engine.execute_operation(lambda x: math.tan(math.radians(x)))())
        elif key == 'y': self.button_input('^')
        elif key == 'o': self.button_special(lambda: self.engine.execute_operation(lambda x: math.cos(math.radians(x)))())
        elif key == 'p': self.button_input(str(math.pi))
        elif key == 's': self.button_special(lambda: self.engine.execute_operation(lambda x: math.sin(math.radians(x)))())
        elif key == 'l': self.button_special(lambda: self.engine.execute_operation(lambda x: math.log10(x) if x>0 else float('nan'))())
        elif key == 'n': self.button_special(lambda: self.engine.execute_operation(lambda x: math.log(x) if x>0 else float('nan'))())

if __name__ == '__main__':
    root = Tk()
    ui = ScientificCalculatorUI(root)
    root.mainloop()
