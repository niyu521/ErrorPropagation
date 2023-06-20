import sympy as sp
import re
import math

# ----------------------------------------------------------------------------------------------
# 数式を指定
expression = 'x/(y*z)'

# 変数名、最確値、公算誤差の二次元配列
variables = [
    ["x", 0.872, 0.003],  
    ["y", 499.90, 0.03],  
    ["z", 74.095, 0.003]  
]

# ----------------------------------------------------------------------------------------------

# 式から変数を抜き出す関数
def extract_variables(expression):
    pattern = r'[a-zA-Z_]\w*'  # 変数名として許容されるパターン
    variables = re.findall(pattern, expression)
    unique_variables = set(variables)
    return unique_variables

# 指定した式を指定した変数で偏微分する関数
def partial_derivative(expression, variable):
    x = sp.Symbol(variable)
    derivative = sp.diff(expression, x)
    return derivative

# 数式に変数の値を代入して計算する関数
def evaluate_expression(expression, variable_values):
    sorted_array = sorted(variable_values.items(), key=lambda x: len(x[0]), reverse=True)
    sorted_dict = dict(sorted_array)

    for variable, value in sorted_dict.items():
        expression = expression.replace(variable, str(value))
    result = eval(expression)
    return result

# main関数
def main():

    # 式に含まれている変数を抽出
    result = extract_variables(expression)
    if len(result) != len(variables):
        print("入力された変数の数が式の変数の数と一致しません")
    else:
        tols = "" #計算する公算誤差の二乗の値の式
        for v in variables:
            variable   = v[0] # どの変数で偏微分するか
            best_value = v[1] # この変数の最確値
            tol        = v[2] # この変数の公算誤差
            result = partial_derivative(expression, variable) # 偏微分を計算
            print(f'{variable}で偏微分する : {result}')

            eq = f'(({result})*r{variable})**2'

            tols += f'{eq}+'
            

        # 代入する値の連想配列を作成
        associative_array = {}  # 空の連想配列を作成
        for v in variables:
            # この変数の最確値
            key1 = v[0]
            value = v[1]
            associative_array[key1] = value

            # この変数の公算誤差
            key2 = f'r{v[0]}' 
            value = v[2]
            associative_array[key2] = value

        print(associative_array)
        

        tols = tols[:-1] # 最後についてる + を削除
        tols_double = evaluate_expression(tols, associative_array)
        print(tols)

        print(f'r = {math.sqrt(tols_double)}')


if __name__ == "__main__":
    main()
    





