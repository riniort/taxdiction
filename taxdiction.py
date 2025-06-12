import tkinter as tk
from tkinter import ttk

# Constants
DEFAULT_VAT_RATES = {
    "7%": 0.07,
    "10%": 0.10,
    "Custom": None
}
DEFAULT_WHT_RATES = {
    "1%": 0.01,
    "2%": 0.02,
    "3%": 0.03,
    "5%": 0.05,
    "10%": 0.10,
    "Custom": None
}

def on_operation_change(event=None):
    op = operation.get()

    # Hide both VAT and WHT related fields first
    for widget in [label_vat, vat_dropdown, entry_custom_vat, label_wht, wht_dropdown, entry_custom_rate]:
        widget.grid_remove()

    if op in ["+VAT", "-VAT"]:
        label_vat.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        vat_dropdown.grid(row=2, column=1, padx=10)
        vat_dropdown.config(state="readonly")
        on_vat_rate_change()

    elif op in ["+WHT", "-WHT"]:
        label_wht.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        wht_dropdown.grid(row=2, column=1, padx=10)
        wht_dropdown.config(state="readonly")
        on_wht_rate_change()

def on_wht_rate_change(event=None):
    if wht_rate_var.get() == "Custom":
        entry_custom_rate.grid(row=3, column=1, padx=10)
    else:
        entry_custom_rate.grid_remove()

def on_vat_rate_change(event=None):
    if vat_rate_var.get() == "Custom":
        entry_custom_vat.grid(row=3, column=1, padx=10)
    else:
        entry_custom_vat.grid_remove()

def paste_clipboard():
    try:
        clipboard_value = root.clipboard_get()
        entry_amount.delete(0, tk.END)
        entry_amount.insert(0, clipboard_value)
    except tk.TclError:
        entry_amount.insert(0, "Clipboard empty")

def calculate():
    try:
        amount = float(entry_amount.get())
        op = operation.get()

        if op in ["+WHT", "-WHT"]:
            rate = float(entry_custom_rate.get()) / 100 if wht_rate_var.get() == "Custom" else DEFAULT_WHT_RATES.get(wht_rate_var.get(), 0)
        elif op in ["+VAT", "-VAT"]:
            rate = float(entry_custom_vat.get()) / 100 if vat_rate_var.get() == "Custom" else DEFAULT_VAT_RATES.get(vat_rate_var.get(), 0)
        else:
            rate = 0

        tax_amount = 0
        result = 0

        if op == '+VAT':
            tax_amount = amount * rate
            result = amount + tax_amount
            label_tax.config(text=f"VAT ({rate*100:.2f}%) Amount:")
        elif op == '-VAT':
            result = amount / (1 + rate)
            tax_amount = amount - result
            label_tax.config(text=f"VAT ({rate*100:.2f}%) Included:")
        elif op == '+WHT':
            result = amount / (1 - rate)
            tax_amount = result - amount
            label_tax.config(text=f"WHT ({rate*100:.2f}%) Added:")
        elif op == '-WHT':
            tax_amount = amount * rate
            result = amount - tax_amount
            label_tax.config(text=f"WHT ({rate*100:.2f}%) Deducted:")

        tax_var.set(f"{tax_amount:,.2f}")
        result_var.set(f"{result:,.2f}")
        copied_label_tax.grid_remove()
        copied_label_result.grid_remove()

    except ValueError:
        tax_var.set("Invalid input")
        result_var.set("Invalid input")

def clear_all():
    entry_amount.delete(0, tk.END)
    entry_custom_vat.delete(0, tk.END)
    entry_custom_rate.delete(0, tk.END)
    tax_var.set("")
    result_var.set("")
    copied_label_tax.grid_remove()
    copied_label_result.grid_remove()
    operation.current(0)
    on_operation_change()

def copy_to_clipboard(value, copied_label):
    root.clipboard_clear()
    root.clipboard_append(value)
    copied_label.grid()
    root.after(1500, copied_label.grid_remove)

# GUI Setup
root = tk.Tk()
root.title("Taxdiction - VAT & WHT Calculator")

# Row 0: Amount input + Paste
tk.Label(root, text="Amount (THB):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1, padx=10, sticky="w")
tk.Button(root, text="Paste", command=paste_clipboard).grid(row=0, column=2, padx=5)

# Row 1: Operation
tk.Label(root, text="Operation:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
operation = ttk.Combobox(root, values=["+VAT", "-VAT", "+WHT", "-WHT"], state="readonly")
operation.grid(row=1, column=1, padx=10)
operation.current(0)
operation.bind("<<ComboboxSelected>>", on_operation_change)

# Row 2: VAT and WHT dropdowns (toggle based on operation)
label_vat = tk.Label(root, text="VAT Rate:")
vat_rate_var = tk.StringVar(value="7%")
vat_dropdown = ttk.Combobox(root, textvariable=vat_rate_var, values=list(DEFAULT_VAT_RATES.keys()), state="readonly")
vat_dropdown.bind("<<ComboboxSelected>>", on_vat_rate_change)

label_wht = tk.Label(root, text="WHT Rate:")
wht_rate_var = tk.StringVar(value="3%")
wht_dropdown = ttk.Combobox(root, textvariable=wht_rate_var, values=list(DEFAULT_WHT_RATES.keys()), state="readonly")
wht_dropdown.bind("<<ComboboxSelected>>", on_wht_rate_change)

# Row 3: Custom rate entry fields (hidden by default)
entry_custom_vat = tk.Entry(root)
entry_custom_rate = tk.Entry(root)

# Row 4: Calculate + Clear button
tk.Button(root, text="Calculate", command=calculate).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="C", width=5, fg="red", command=clear_all).grid(row=4, column=2, padx=5)

# Row 5: Tax amount
label_tax = tk.Label(root, text="Tax Amount:")
label_tax.grid(row=5, column=0, padx=10, pady=5, sticky="e")
tax_var = tk.StringVar()
tax_label = tk.Label(root, textvariable=tax_var, font=('Arial', 12), fg="blue", cursor="hand2")
tax_label.grid(row=5, column=1, sticky="w")
copied_label_tax = tk.Label(root, text="Copied!", fg="green", font=("Arial", 10))
copied_label_tax.grid(row=5, column=2)
copied_label_tax.grid_remove()
tax_label.bind("<Button-1>", lambda e: copy_to_clipboard(tax_var.get(), copied_label_tax))

# Row 6: Final result
tk.Label(root, text="Final Result:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=('Arial', 14, 'bold'), fg="blue", cursor="hand2")
result_label.grid(row=6, column=1, sticky="w")
copied_label_result = tk.Label(root, text="Copied!", fg="green", font=("Arial", 10))
copied_label_result.grid(row=6, column=2)
copied_label_result.grid_remove()
result_label.bind("<Button-1>", lambda e: copy_to_clipboard(result_var.get(), copied_label_result))

# Initialize
on_operation_change()
root.mainloop()
