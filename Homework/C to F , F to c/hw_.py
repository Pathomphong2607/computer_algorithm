import customtkinter as ctk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def convert_temp():
    temp = entry.get()

    try:
        value = float(temp[:-1])
        unit = temp[-1].upper()

        if unit == "C":
            result = (value * 9/5) + 32
            output_label.configure(text=f"{value}°C = {result:.2f}°F")

        elif unit == "F":
            result = (value - 32) * 5/9
            output_label.configure(text=f"{value}°F = {result:.2f}°C")

        else:
            output_label.configure(text="รูปแบบข้อมูลไม่ถูกต้อง")

    except:
        output_label.configure(text="กรุณาใส่ เช่น 30C หรือ 86F")



app = ctk.CTk()
app.title("Temperature Converter")
app.geometry("400x250")


title = ctk.CTkLabel(app, text="Celsius ↔ Fahrenheit", font=("Arial", 22))
title.pack(pady=20)


entry = ctk.CTkEntry(app, width=200, placeholder_text="เช่น 30C หรือ 86F")
entry.pack(pady=10)


button = ctk.CTkButton(app, text="Convert", command=convert_temp)
button.pack(pady=10)


output_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
output_label.pack(pady=10)


credit = ctk.CTkLabel(
    app,
    text="นายปฐมพงศ์ พึ่งประโคน 684245008\n"
         "นายพัศณพล คานภู่ 684245010\n"
         "นายกฤตพิภัช ศรีนิล 684245002",
    font=("Arial", 10)
)
credit.pack(side="bottom", pady=10)

app.mainloop()