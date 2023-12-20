import customtkinter
import GPUtil


class GPUMonitorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GPU Usage Monitor")

        # GPU Usage Widgets
        self.gpu_label = customtkinter.CTkLabel(self, text='GPU Usage:')
        self.gpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.gpu_usage = customtkinter.CTkLabel(self, text='')
        self.gpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.update_gpu_info()

    def update_gpu_info(self):
        try:
            gpu_info = GPUtil.getGPUs()[0]  # If first index does return the exception try with next index.
            gpu_percent = gpu_info.load * 100
            self.gpu_usage.configure(text=f'{gpu_percent:.2f}%')
        except Exception as e:
            print(f'Error updating GPU info: {e}')

        self.after(1000, self.update_gpu_info)

if __name__ == '__main__':
    app = GPUMonitorApp()
    app.mainloop()