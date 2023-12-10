import customtkinter
import psutil

class HardwareMonitorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Hardware Monitor")

        # Hardware Monitor Widgets
        self.cpu_label = customtkinter.CTkLabel(self, text='CPU:')
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.ram_label = customtkinter.CTkLabel(self, text='RAM:')
        self.ram_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.update_hardware_info()

    def update_hardware_info(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent

        # Updating CPU Percentage Display
        self.cpu_label.configure(text=f"CPU: {cpu_percent:.2f}%")
        # Updating RAM Percentage Display
        self.ram_label.configure(text=f"RAM: {ram_percent:.2f}%")

        self.after(1000, self.update_hardware_info)

if __name__ == "__main__":
    app = HardwareMonitorApp()
    app.mainloop()

