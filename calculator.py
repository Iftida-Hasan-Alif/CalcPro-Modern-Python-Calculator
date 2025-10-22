import tkinter as tk
from tkinter import font
import math

class ModernCalculator:
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.window.title("CalcPro")
        self.window.geometry("350x550")
        self.window.resizable(False, False)
        self.window.configure(bg='#1E1E1E')
        
        # Calculator state
        self.current_input = "0"
        self.full_expression = ""
        self.result_displayed = False
        
        # Custom fonts
        self.display_font = font.Font(family='Arial', size=32, weight='bold')
        self.expression_font = font.Font(family='Arial', size=12)
        self.button_font = font.Font(family='Arial', size=16, weight='bold')
        
        # Create UI
        self.create_display()
        self.create_buttons()
        self.setup_bindings()
        
    def create_display(self):
        """Create the display area with modern styling"""
        display_frame = tk.Frame(self.window, bg='#1E1E1E', height=150)
        display_frame.pack(fill='x', padx=20, pady=20)
        
        # Expression label (shows calculation history)
        self.expression_label = tk.Label(
            display_frame,
            text="",
            bg='#1E1E1E',
            fg='#888888',
            font=self.expression_font,
            anchor='e'
        )
        self.expression_label.pack(fill='x', pady=(20, 5))
        
        # Result label (shows current input/result)
        self.result_label = tk.Label(
            display_frame,
            text="0",
            bg='#1E1E1E',
            fg='white',
            font=self.display_font,
            anchor='e'
        )
        self.result_label.pack(fill='x', pady=(0, 20))
        
        # Separator line
        separator = tk.Frame(display_frame, height=1, bg='#444444')
        separator.pack(fill='x')

    def create_button(self, parent, text, bg_color, fg_color='white', command=None, width=5, height=2):
        """Helper function to create consistent buttons with hover effects"""
        btn = tk.Button(
            parent,
            text=text,
            bg=bg_color,
            fg=fg_color,
            font=self.button_font,
            borderwidth=0,
            relief='flat',
            width=width,
            height=height,
            command=command,
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(e):
            btn.configure(bg=self.lighten_color(bg_color))
            
        def on_leave(e):
            btn.configure(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def lighten_color(self, color):
        """Lighten color for hover effect"""
        if color == '#404040':  # Number buttons
            return '#505050'
        elif color == '#FF9500':  # Operator buttons
            return '#FFB143'
        elif color == '#A6A6A6':  # Special buttons
            return '#B8B8B8'
        return color

    def create_buttons(self):
        """Create all calculator buttons"""
        button_frame = tk.Frame(self.window, bg='#1E1E1E')
        button_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Configure grid
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        
        # Button definitions: (text, row, col, bg_color, fg_color, command)
        buttons = [
            # Row 1: Special functions
            ('C', 0, 0, '#A6A6A6', 'black', self.clear_display),
            ('±', 0, 1, '#A6A6A6', 'black', self.toggle_sign),
            ('%', 0, 2, '#A6A6A6', 'black', self.percentage),
            ('÷', 0, 3, '#FF9500', 'white', lambda: self.apply_operator('÷')),
            
            # Row 2: Numbers 7-9 and multiply
            ('7', 1, 0, '#404040', 'white', lambda: self.add_digit('7')),
            ('8', 1, 1, '#404040', 'white', lambda: self.add_digit('8')),
            ('9', 1, 2, '#404040', 'white', lambda: self.add_digit('9')),
            ('×', 1, 3, '#FF9500', 'white', lambda: self.apply_operator('×')),
            
            # Row 3: Numbers 4-6 and subtract
            ('4', 2, 0, '#404040', 'white', lambda: self.add_digit('4')),
            ('5', 2, 1, '#404040', 'white', lambda: self.add_digit('5')),
            ('6', 2, 2, '#404040', 'white', lambda: self.add_digit('6')),
            ('−', 2, 3, '#FF9500', 'white', lambda: self.apply_operator('−')),
            
            # Row 4: Numbers 1-3 and add
            ('1', 3, 0, '#404040', 'white', lambda: self.add_digit('1')),
            ('2', 3, 1, '#404040', 'white', lambda: self.add_digit('2')),
            ('3', 3, 2, '#404040', 'white', lambda: self.add_digit('3')),
            ('+', 3, 3, '#FF9500', 'white', lambda: self.apply_operator('+')),
            
            # Row 5: Zero, decimal, equals, and square root
            ('0', 4, 0, '#404040', 'white', lambda: self.add_digit('0')),
            ('.', 4, 1, '#404040', 'white', self.add_decimal),
            ('=', 4, 2, '#FF9500', 'white', self.calculate_result),
            ('√', 4, 3, '#FF9500', 'white', self.square_root),
        ]
        
        # Create buttons
        for text, row, col, bg_color, fg_color, command in buttons:
            # Make zero button wider
            col_span = 2 if text == '0' else 1
            col_pos = col if text != '0' else 0
            
            btn = self.create_button(
                button_frame, 
                text, 
                bg_color, 
                fg_color, 
                command
            )
            btn.grid(
                row=row, 
                column=col_pos, 
                columnspan=col_span,
                sticky='nsew',
                padx=2,
                pady=2
            )

    def setup_bindings(self):
        """Set up keyboard bindings"""
        # Number keys
        for digit in '0123456789':
            self.window.bind(digit, lambda event, d=digit: self.add_digit(d))
        
        # Operators
        self.window.bind('+', lambda event: self.apply_operator('+'))
        self.window.bind('-', lambda event: self.apply_operator('−'))
        self.window.bind('*', lambda event: self.apply_operator('×'))
        self.window.bind('/', lambda event: self.apply_operator('÷'))
        
        # Special keys
        self.window.bind('<Return>', lambda event: self.calculate_result())
        self.window.bind('<Escape>', lambda event: self.clear_display())
        self.window.bind('<BackSpace>', lambda event: self.backspace())
        self.window.bind('.', lambda event: self.add_decimal())
        self.window.bind('%', lambda event: self.percentage())

    def update_display(self):
        """Update the display with current values"""
        self.result_label.config(text=self.current_input)
        self.expression_label.config(text=self.full_expression)

    def add_digit(self, digit):
        """Add a digit to current input"""
        if self.result_displayed or self.current_input == "0":
            self.current_input = digit
            self.result_displayed = False
        else:
            self.current_input += digit
        self.update_display()

    def add_decimal(self):
        """Add decimal point"""
        if '.' not in self.current_input:
            if self.result_displayed or self.current_input == "0":
                self.current_input = "0."
                self.result_displayed = False
            else:
                self.current_input += "."
            self.update_display()

    def apply_operator(self, operator):
        """Apply operator to current calculation"""
        if self.full_expression and not self.result_displayed:
            self.full_expression += f" {self.current_input}"
        
        python_operator = self.convert_operator(operator)
        
        if not self.full_expression or self.result_displayed:
            self.full_expression = f"{self.current_input} {python_operator}"
        else:
            self.full_expression += f" {python_operator}"
        
        self.current_input = "0"
        self.result_displayed = False
        self.update_display()

    def convert_operator(self, operator):
        """Convert display operator to Python operator"""
        conversion = {'÷': '/', '×': '*', '−': '-'}
        return conversion.get(operator, operator)

    def calculate_result(self):
        """Calculate and display result"""
        if not self.full_expression:
            return
            
        try:
            full_expression = self.full_expression + " " + self.current_input
            
            # Convert display operators
            for display_op, python_op in [('÷', '/'), ('×', '*'), ('−', '-')]:
                full_expression = full_expression.replace(display_op, python_op)
            
            result = eval(full_expression)
            
            # Format result nicely
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = str(round(result, 10)).rstrip('0').rstrip('.')
            
            self.current_input = result_str
            self.full_expression = full_expression + " ="
            self.result_displayed = True
            self.update_display()
            
        except ZeroDivisionError:
            self.current_input = "Cannot divide by zero"
            self.full_expression = ""
            self.result_displayed = True
            self.update_display()
        except:
            self.current_input = "Error"
            self.full_expression = ""
            self.result_displayed = True
            self.update_display()

    def clear_display(self):
        """Clear everything"""
        self.current_input = "0"
        self.full_expression = ""
        self.result_displayed = False
        self.update_display()

    def toggle_sign(self):
        """Toggle between positive and negative"""
        if self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()

    def percentage(self):
        """Convert to percentage"""
        try:
            value = float(self.current_input)
            self.current_input = str(value / 100)
            self.update_display()
        except:
            self.current_input = "Error"
            self.update_display()

    def square_root(self):
        """Calculate square root"""
        try:
            value = float(self.current_input)
            if value >= 0:
                result = math.sqrt(value)
                if result == int(result):
                    self.current_input = str(int(result))
                else:
                    self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')
                self.full_expression = f"√{value} ="
                self.result_displayed = True
                self.update_display()
            else:
                self.current_input = "Invalid input"
                self.update_display()
        except:
            self.current_input = "Error"
            self.update_display()

    def backspace(self):
        """Remove last character"""
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.update_display()

    def run(self):
        """Start the application"""
        self.window.mainloop()

# Run the calculator
if __name__ == "__main__":
    print("🚀 Starting Modern Calculator...")
    print("💡 Tips: Use keyboard numbers and operators, or click buttons!")
    calc = ModernCalculator()
    calc.run()