
import tkinter as tk
from tkinter import ttk, StringVar

# Tax rates
DEFAULT_VAT_RATES = {"7%": 0.07, "10%": 0.10, "Custom": None}
DEFAULT_WHT_RATES = {"1%": 0.01, "2%": 0.02, "3%": 0.03, "5%": 0.05, "10%": 0.10, "Custom": None}

def on_operation_change(event=None):
    op = operation.get()
    for widget in [label_vat, vat_dropdown, entry_custom_vat, label_wht, wht_dropdown, entry_custom_rate]:
        widget.grid_remove()
    if op in ["+VAT", "-VAT"]:
        label_vat.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        vat_dropdown.grid(row=2, column=1, padx=10)
        on_vat_rate_change()
    elif op in ["+WHT", "-WHT"]:
        label_wht.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        wht_dropdown.grid(row=2, column=1, padx=10)
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
        if op == "+VAT":
            tax_amount = amount * rate
            result = amount + tax_amount
            label_tax.config(text=f"VAT ({rate*100:.2f}%) Amount:")
        elif op == "-VAT":
            result = amount / (1 + rate)
            tax_amount = amount - result
            label_tax.config(text=f"VAT ({rate*100:.2f}%) Included:")
        elif op == "+WHT":
            result = amount / (1 - rate)
            tax_amount = result - amount
            label_tax.config(text=f"WHT ({rate*100:.2f}%) Added:")
        elif op == "-WHT":
            tax_amount = amount * rate
            result = amount - tax_amount
            label_tax.config(text=f"WHT ({rate*100:.2f}%) Deducted:")
        tax_var.set(f"{tax_amount:,.2f}")
        result_var.set(f"{result:,.2f}")
        copied_label_tax.grid_remove()
        copied_label_result.grid_remove()
    except:
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

def copy_to_clipboard(value, label):
    root.clipboard_clear()
    root.clipboard_append(value)
    label.grid()
    root.after(1500, label.grid_remove)

# Main UI
root = tk.Tk()
root.title("Taxdiction")
root.configure(bg="black")

entry_amount = tk.Entry(root, font=("Helvetica", 28), bg="black", fg="white", justify="right", bd=0)
entry_amount.insert(0, "0")
entry_amount.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

operation = ttk.Combobox(root, values=["+VAT", "-VAT", "+WHT", "-WHT"], state="readonly", font=("Helvetica", 14))
operation.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
operation.current(0)
operation.bind("<<ComboboxSelected>>", on_operation_change)

tk.Button(root, text="Paste", font=("Helvetica", 14), bg="#a5a5a5", fg="black", command=paste_clipboard).grid(row=1, column=2)
tk.Button(root, text="C", font=("Helvetica", 14), bg="#a5a5a5", fg="black", command=clear_all).grid(row=1, column=3)

label_vat = tk.Label(root, text="VAT Rate:", bg="black", fg="white", font=("Helvetica", 12))
vat_rate_var = StringVar(value="7%")
vat_dropdown = ttk.Combobox(root, textvariable=vat_rate_var, values=list(DEFAULT_VAT_RATES.keys()), state="readonly", font=("Helvetica", 12))
vat_dropdown.bind("<<ComboboxSelected>>", on_vat_rate_change)

label_wht = tk.Label(root, text="WHT Rate:", bg="black", fg="white", font=("Helvetica", 12))
wht_rate_var = StringVar(value="3%")
wht_dropdown = ttk.Combobox(root, textvariable=wht_rate_var, values=list(DEFAULT_WHT_RATES.keys()), state="readonly", font=("Helvetica", 12))
wht_dropdown.bind("<<ComboboxSelected>>", on_wht_rate_change)

entry_custom_vat = tk.Entry(root, font=("Helvetica", 12))
entry_custom_rate = tk.Entry(root, font=("Helvetica", 12))

tk.Button(root, text="Calculate", font=("Helvetica", 16), bg="#ff9500", fg="white", command=calculate).grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")

label_tax = tk.Label(root, text="Tax Amount:", bg="black", fg="white", font=("Helvetica", 12))
label_tax.grid(row=5, column=0, padx=10, pady=5, sticky="e")
tax_var = StringVar()
tax_label = tk.Label(root, textvariable=tax_var, font=('Helvetica', 14), bg="black", fg="orange", cursor="hand2")
tax_label.grid(row=5, column=1, sticky="w")
copied_label_tax = tk.Label(root, text="Copied!", fg="green", bg="black", font=("Helvetica", 10))
copied_label_tax.grid(row=5, column=2)
copied_label_tax.grid_remove()
tax_label.bind("<Button-1>", lambda e: copy_to_clipboard(tax_var.get(), copied_label_tax))

tk.Label(root, text="Final Result:", bg="black", fg="white", font=("Helvetica", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
result_var = StringVar()
result_label = tk.Label(root, textvariable=result_var, font=('Helvetica', 16, 'bold'), bg="black", fg="orange", cursor="hand2")
result_label.grid(row=6, column=1, sticky="w")
copied_label_result = tk.Label(root, text="Copied!", fg="green", bg="black", font=("Helvetica", 10))
copied_label_result.grid(row=6, column=2)
copied_label_result.grid_remove()
result_label.bind("<Button-1>", lambda e: copy_to_clipboard(result_var.get(), copied_label_result))

on_operation_change()
root.mainloop()
