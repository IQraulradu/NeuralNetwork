import tkinter as tk
from tkinter import ttk
import math
import numpy as np
from ttkthemes import ThemedStyle

spinbox_values = []
data_results = []

def create_gui():
    root = tk.Tk()
    root.title("Neural Network")


    style = ThemedStyle(root)
    style.set_theme("arc")
    style.configure("TLabel", foreground="black")
    style.configure("TButton", foreground="black")

    teta_value = tk.DoubleVar()
    teta_value.set(0.0)
    num_decimals = tk.IntVar()
    num_decimals.set(2)
    gamma_value = tk.DoubleVar()
    gamma_value.set(1.0)

    def add_connection():
        a_spinbox = ttk.Spinbox(canvas_frame, from_=0, to=10, increment=0.01, width=10, style="Custom.TSpinbox")
        b_spinbox = ttk.Spinbox(canvas_frame, from_=0, to=10, increment=0.01, width=10, style="Custom.TSpinbox")
        a_spinbox.grid(row=len(spinbox_values), column=0, sticky="ew")
        b_spinbox.grid(row=len(spinbox_values), column=1, sticky="ew")
        a_spinbox.set(0.00)
        b_spinbox.set(0.00)
        a_spinbox["foreground"] = "black"
        b_spinbox["foreground"] = "black"
        spinbox_values.append((a_spinbox, b_spinbox))

    def remove_connection():
        if spinbox_values:
            a_spinbox, b_spinbox = spinbox_values.pop()
            a_spinbox.destroy()
            b_spinbox.destroy()

    def perform_dataResult():
        data_results.clear()
        for a_spinbox, b_spinbox in spinbox_values:
            a_value = float(a_spinbox.get())
            b_value = float(b_spinbox.get())
            result = round(a_value * b_value, num_decimals.get())
            data_results.append(result)

    def unit_step(operation):
        if operation < 0:
            return 0
        else:
            return 1

    def signum(operation):
        if operation < 0:
            return -1
        elif operation == 0:
            return 0
        else:
            return 1

    # def sigmoid(operation):
    #     return 1 / (1 + math.exp(-operation))
    #
    # def TangentHiperbolic(x):
    #     return np.tanh(x)

    def linear(operation):
        return operation

    def gamma_sigmoid(operation, gamma):
        return 1 / (1 + math.exp(-gamma * operation))

    def gamma_tangent(operation, gamma):
        return np.tanh(gamma * operation)

    def perform_operation(operation):
        if not spinbox_values:
            return

        perform_dataResult()
        teta = teta_value.get()
        gamma = gamma_value.get()
        threshold = -0.05

        if operation == "sum":
            result = round(sum(data_results), num_decimals.get())
        elif operation == "multiply":
            result = round(1, num_decimals.get())
            for value in data_results:
                result *= value
            result = round(result, num_decimals.get())
        elif operation == "min":
            result = round(min(data_results), num_decimals.get())
        elif operation == "max":
            result = round(max(data_results), num_decimals.get())
        elif operation == "unit_step":
            sum_of_values = sum(data_results) + teta
            result = unit_step(sum_of_values)
            result_label.config(text=f"Output (Unit Step): {result}")
            return
        elif operation == "signum":
            sum_of_values = sum(data_results) + teta
            result = signum(sum_of_values)
            result_label.config(text=f"Output (Signum): {result}")
            return
        elif operation == "sigmoid":
            sum_of_values = sum(data_results) + teta
            result = gamma_sigmoid(sum_of_values, gamma)
            result_label.config(text=f"Output (Sigmoid): {result}")
            return
        elif operation == "tangent":
            sum_of_values = sum(data_results) + teta
            result = gamma_tangent(sum_of_values, gamma)
            result_label.config(text=f"Output (Tangent): {result}")
            return
        elif operation == "linear":
            sum_of_values = sum(data_results) + teta
            result = linear(sum_of_values)
            result_label.config(text=f"Output (Linear): {result}")
            return
        elif operation == "binary":
            sum_of_values = sum(data_results) + teta
            binary_result = 1 if sum_of_values > threshold else 0
            result_label.config(text=f"Binary Output: {binary_result}")
            return
        else:
            result = 0

        result_label.config(text=f"Output ({operation}): {result}")

    data_input_frame = ttk.Frame(root)
    data_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    teta_entry = ttk.Entry(data_input_frame, textvariable=teta_value, style="Custom.TEntry")
    teta_label = ttk.Label(data_input_frame, text="Teta (ϴ):", style="Custom.TLabel")
    teta_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    teta_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    teta_label["foreground"] = "black"
    teta_entry["foreground"] = "black"

    gamma_label = ttk.Label(data_input_frame, text="Gamma (γ):", style="Custom.TLabel")
    gamma_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    gamma_entry = ttk.Entry(data_input_frame, textvariable=gamma_value, style="Custom.TEntry")
    gamma_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    gamma_label["foreground"] = "black"
    gamma_entry["foreground"] = "black"

    canvas = tk.Canvas(data_input_frame)
    canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    canvas_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    scrollbar = ttk.Scrollbar(data_input_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas_frame.bind("<Configure>", on_configure)

    add_button = ttk.Button(data_input_frame, text="Add (Increase ++)", command=add_connection, style="Custom.TButton")
    remove_button = ttk.Button(data_input_frame, text="Remove (Decrease --)", command=remove_connection, style="Custom.TButton")

    add_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    remove_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    operation_frame = ttk.Frame(root)
    operation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    num_decimals_label = ttk.Label(root, text="Number of Decimals:")
    num_decimals_entry = ttk.Entry(root, textvariable=num_decimals)
    num_decimals_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    num_decimals_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    sum_button = ttk.Button(operation_frame, text="Sum", command=lambda: perform_operation("sum"), style="Custom.TButton")
    multiply_button = ttk.Button(operation_frame, text="Multiply", command=lambda: perform_operation("multiply"), style="Custom.TButton")
    min_button = ttk.Button(operation_frame, text="Minimum", command=lambda: perform_operation("min"), style="Custom.TButton")
    max_button = ttk.Button(operation_frame, text="Maximum", command=lambda: perform_operation("max"), style="Custom.TButton")
    unit_step_button = ttk.Button(operation_frame, text="Unit Step", command=lambda: perform_operation("unit_step"), style="Custom.TButton")
    signum_button = ttk.Button(operation_frame, text="Signum", command=lambda: perform_operation("signum"), style="Custom.TButton")
    sigmoid_button = ttk.Button(operation_frame, text="Sigmoid", command=lambda: perform_operation("sigmoid"), style="Custom.TButton")
    tangent_button = ttk.Button(operation_frame, text="Tangent", command=lambda: perform_operation("tangent"), style="Custom.TButton")
    linear_button = ttk.Button(operation_frame, text="Linear", command=lambda: perform_operation("linear"), style="Custom.TButton")
    binary_output_button = ttk.Button(operation_frame, text="Binary", command=lambda: perform_operation("binary"), style="Custom.TButton")

    binary_output_button.grid(row=2, column=0, padx=10, pady=5)
    sum_button.grid(row=0, column=0, padx=10, pady=5)
    multiply_button.grid(row=0, column=1, padx=10, pady=5)
    min_button.grid(row=0, column=2, padx=10, pady=5)
    max_button.grid(row=0, column=3, padx=10, pady=5)
    unit_step_button.grid(row=1, column=4, padx=10, pady=5)
    signum_button.grid(row=1, column=0, padx=10, pady=5)
    sigmoid_button.grid(row=1, column=1, padx=10, pady=5)
    tangent_button.grid(row=1, column=2, padx=10, pady=5)
    linear_button.grid(row=1, column=3, padx=10, pady=5)

    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    result_label = tk.Label(result_frame, text="Final result: ", font=("Helvetica", 14))
    result_label.grid(row=0, column=0, padx=10, pady=5)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    return root

if __name__ == "__main__":
    app = create_gui()
    app.geometry("750x650")
    app.mainloop()