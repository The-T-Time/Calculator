import math
import decimal

class CalculatorEngine:
    def __init__(self, max_length=18):
        self.max_length = max_length
        self.current_expression = ""
        self.pending_operation = None
        self.log_number = None
        self.clear_next_input = False

    def append_to_expression(self, char):
        if self.clear_next_input and (char.isdigit() or char == '.'):
            self.current_expression = ""
            self.clear_next_input = False
        elif self.clear_next_input and not char.isdigit():
            self.clear_next_input = False

        #for operators, if the last character is already an operator, replace it.
        if char in '+-*/^':
            if self.current_expression and self.current_expression[-1] in '+-*/^':
                self.current_expression = self.current_expression[:-1]
        if len(self.current_expression) < self.max_length:
            self.current_expression += str(char)
        return self.current_expression

    def change_sign_of_last_number(self):
        if not self.current_expression:
            return self.current_expression

        #find the last operator's index (if any).
        last_index = -1
        for i, ch in enumerate(self.current_expression):
            if ch in '+-*/^':
                last_index = i
        if last_index == -1:
            #no operator exists: change sign of the whole expression.
            if self.current_expression.startswith('-'):
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = '-' + self.current_expression
        else:
            #change sign only for the number after the last operator.
            prefix = self.current_expression[:last_index+1]
            number = self.current_expression[last_index+1:]
            if number.startswith('-'):
                number = number[1:]
            else:
                number = '-' + number
            self.current_expression = prefix + number
        return self.current_expression

    def clear_all(self):
        self.current_expression = ""
        self.clear_next_input = False
        self.pending_operation = None
        self.log_number = None
        return "0"

    def delete_last(self):
        if self.clear_next_input:
            self.current_expression = ""
            self.clear_next_input = False
        else:
            self.current_expression = self.current_expression[:-1]
        if not self.current_expression:
            return "0"
        return self.current_expression

    def safe_eval(self, expr):
        #replace custom '^' with '**' for power calculations.
        expr = expr.replace('^', '**')
        allowed_names = {}
        allowed_names.update(math.__dict__)
        allowed_names.update({'Decimal': decimal.Decimal})
        #disable built-ins for safety.
        return eval(expr, {"__builtins__": None}, allowed_names)

    def evaluate(self):
        try:
            if self.pending_operation:
                operand = float(self.current_expression)
                result = None
                if self.pending_operation == "logyx":
                    result = math.log(self.log_number, operand)
                elif self.pending_operation == "nth_root":
                    result = self.log_number ** (1 / operand)
                self.current_expression = str(result)
                self.pending_operation = None
                self.clear_next_input = True
                return self.format_result(self.current_expression)
            else:
                result = self.safe_eval(self.current_expression)
                if isinstance(result, float):
                    result = round(result, 15)
                    result_str = str(result)
                    if '.' in result_str:
                        result_str = result_str.rstrip('0').rstrip('.')
                    self.current_expression = result_str
                    self.clear_next_input = True
                    return self.format_result(result_str)
                else:
                    self.current_expression = str(result)
                    self.clear_next_input = True
                    return self.format_result(self.current_expression)
        except Exception:
            self.current_expression = ""
            self.clear_next_input = True
            return "ERROR"

    def set_pending_operation(self, operation):
        try:
            self.log_number = float(self.current_expression) if self.current_expression else 0
            self.current_expression = ""
            self.pending_operation = operation
            return f"{self.log_number} pending {operation}"
        except Exception:
            self.current_expression = ""
            self.clear_next_input = True
            return "ERROR"

    def execute_operation(self, func):
        try:
            result = func(float(self.current_expression))
            self.current_expression = str(result)
            self.clear_next_input = True
            return self.format_result(self.current_expression)
        except Exception:
            self.current_expression = ""
            self.clear_next_input = True
            return "ERROR"

    def format_result(self, result):
        try:
            num = float(result)
            if abs(num) > 10 ** self.max_length or (abs(num) < 0.0001 and num != 0):
                formatted = f"{num:.6e}"
            else:
                formatted = result
            if num == int(num):
                formatted = str(int(num))
            return formatted
        except Exception:
            return result
