import psutil
# import GPUtil
import tkinter
import tkinter.messagebox
import customtkinter
import keyboard

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class ControITApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuring Window Attributes
        self.title("ControIT")
        self.geometry(f"{1280}x{720}")

# Hardware Usage Monitoring Widgets
        self.cpu_label = customtkinter.CTkLabel(self, text='CPU:')
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.cpu_usage = customtkinter.CTkLabel(self, text="")
        self.cpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.memory_label = customtkinter.CTkLabel(self, text='RAM:')
        self.memory_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.memory_usage = customtkinter.CTkLabel(self, text="")
        self.memory_usage.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Keyboard Input Blocker Widgets
        self.keyboard_block_var = customtkinter.BooleanVar()
        self.blocker_switch = customtkinter.CTkSwitch(self, text="Keyboard Blocker", variable=self.keyboard_block_var, command=self.disable_keyboard_input)
        self.blocker_switch.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.update_hardware_info()


    def update_hardware_info(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent

        self.cpu_usage.configure(text=f"{cpu_percent:.2f}%")
        self.memory_usage.configure(text=f"{ram_percent:.2f}%")

        self.after(1000, self.update_hardware_info)

    def disable_keyboard_input(self):
        for i in range(150):
            if self.keyboard_block_var.get():
                keyboard.block_key(i)
            else:
                keyboard.unhook(i)


if __name__ == "__main__":
    app = ControITApp()
    app.mainloop()