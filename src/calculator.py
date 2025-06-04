import tkinter as tk
from tkinter import messagebox
from typing import Union, List

class Calculator:
    def __init__(self):
        # 메인 윈도우 생성 및 기본 설정
        self.root = tk.Tk()
        self.root.title("간단한 계산기")  # 창 제목 설정
        self.root.geometry("300x400")    # 창 크기 설정 (너비x높이)
        
        # 계산 결과를 표시할 Entry 위젯 생성
        # width=20: 입력창의 너비, font: 폰트 종류와 크기 설정
        self.display = tk.Entry(self.root, width=20, font=('Arial', 16))
        # grid로 위치 지정 (첫 번째 행, columnspan=4로 4칸 차지)
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
        self.current_expression: List[str] = []  # 현재 수식을 저장할 리스트
        self.last_result: Union[float, str] = ""  # 마지막 계산 결과 저장
        
        # 계산기 버튼들 생성
        self.create_buttons()
        
    def create_buttons(self):
        # 버튼에 표시될 텍스트를 리스트로 정의
        button_texts = [
            '7', '8', '9', '/',    # 첫 번째 행
            '4', '5', '6', '*',    # 두 번째 행
            '1', '2', '3', '-',    # 세 번째 행
            '0', '.', '=', '+'     # 네 번째 행
        ]
        
        row = 1    # 시작 행 (display가 0행이므로 1부터 시작)
        col = 0    # 시작 열
        
        # 버튼 텍스트 리스트를 순회하며 버튼 생성
        for button_text in button_texts:
            # 버튼 위젯 생성
            # lambda를 사용하여 각 버튼별로 고유한 command 함수 생성
            button = tk.Button(
                self.root,
                text=button_text,
                width=5,
                height=2,
                command=lambda x=button_text: self.button_click(x)
            )
            # 버튼을 그리드에 배치
            button.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            # 4열까지 배치했으면 다음 행으로 이동
            if col > 3:
                col = 0
                row += 1
    
    def calculate(self, num1: float, num2: float, operator: str) -> Union[float, str]:
        """안전한 계산을 수행하는 메서드"""
        try:
            match operator:
                case '+':
                    return num1 + num2
                case '-':
                    return num1 - num2
                case '*':
                    return num1 * num2
                case '/':
                    if num2 == 0:
                        return "0으로 나눌 수 없습니다"
                    return num1 / num2
                case _:
                    return "잘못된 연산자입니다"
        except Exception as e:
            return f"계산 오류: {str(e)}"

    def evaluate_expression(self, expression: List[str]) -> Union[float, str]:
        """수식 리스트를 계산하는 메서드 (연산자 우선순위 적용)"""
        if not expression:
            return ""

        # 숫자와 연산자를 분리
        numbers = []
        operators = []
        
        # 첫 번째 숫자 처리
        try:
            numbers.append(float(expression[0]))
        except ValueError:
            return "잘못된 숫자 형식입니다"

        # 나머지 수식 처리
        i = 1
        while i < len(expression):
            if i + 1 >= len(expression):
                return "수식이 완성되지 않았습니다"
            
            operator = expression[i]
            try:
                next_num = float(expression[i + 1])
            except ValueError:
                return "잘못된 숫자 형식입니다"

            # 연산자 우선순위에 따라 처리
            if operator in ['*', '/']:
                # 이전 숫자와 현재 숫자로 계산
                prev_num = numbers.pop()
                calc_result = self.calculate(prev_num, next_num, operator)
                if isinstance(calc_result, str):
                    return calc_result
                numbers.append(calc_result)
            else:
                # +, - 연산자는 나중에 처리
                numbers.append(next_num)
                operators.append(operator)
            i += 2

        # 남은 +, - 연산 처리
        result = numbers[0]
        for i, operator in enumerate(operators):
            calc_result = self.calculate(result, numbers[i + 1], operator)
            if isinstance(calc_result, str):
                return calc_result
            result = calc_result

        return result

    def button_click(self, value: str):
        if value == '=':    # '=' 버튼 클릭 시
            if not self.current_expression:
                if isinstance(self.last_result, (int, float)):
                    self.display.delete(0, tk.END)
                    self.display.insert(0, str(self.last_result))
                return
            
            # 수식 계산
            result = self.evaluate_expression(self.current_expression)
            
            # 결과 표시 및 저장
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            if isinstance(result, (int, float)):
                self.last_result = result
            
            # 수식 초기화
            self.current_expression = []
            
        elif value in ['+', '-', '*', '/']:    # 연산자 버튼 클릭 시
            if not self.current_expression:    # 첫 입력이 연산자인 경우
                if isinstance(self.last_result, (int, float)):    # 이전 결과가 있으면
                    self.current_expression = [str(self.last_result), value]
                    self.display.delete(0, tk.END)
                    self.display.insert(0, ''.join(self.current_expression))
                return
            elif self.current_expression[-1] in ['+', '-', '*', '/']:    # 연속된 연산자 입력 방지
                self.current_expression[-1] = value
                self.display.delete(0, tk.END)
                self.display.insert(0, ''.join(self.current_expression))
            else:
                # 현재 수식이 있으면 계산 후 연산자 추가
                temp_result = self.evaluate_expression(self.current_expression)
                if isinstance(temp_result, (int, float)):
                    self.current_expression = [str(temp_result), value]
                    self.display.delete(0, tk.END)
                    self.display.insert(0, ''.join(self.current_expression))
                else:
                    return
            
        else:    # 숫자나 소수점 버튼 클릭 시
            if not self.current_expression:    # 첫 입력인 경우
                self.current_expression.append(value)
                self.last_result = ""    # 새로운 숫자 입력 시 이전 결과 초기화
            elif self.current_expression[-1] in ['+', '-', '*', '/']:    # 연산자 다음인 경우
                self.current_expression.append(value)
            else:    # 이전 숫자에 이어서 입력
                self.current_expression[-1] += value
            self.display.delete(0, tk.END)
            self.display.insert(0, ''.join(self.current_expression))
    
    def run(self):
        # 메인 이벤트 루프 실행
        self.root.mainloop()

# 프로그램 시작점
if __name__ == "__main__":
    calc = Calculator()    # Calculator 인스턴스 생성
    calc.run()            # 프로그램 실행