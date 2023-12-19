import psutil
import tkinter
import customtkinter

class DiskMonitorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Disk Monitor")

        # Disk Labels
        self.disk_labels = []
        self.disk_textvars = []

        for i, disk in enumerate(psutil.disk_partitions()):
            text_var = tkinter.StringVar()
            text_var.set(f'{disk.device}: {0.0}%')
            label = customtkinter.CTkLabel(self, textvariable=text_var)
            label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            self.disk_labels.append(label)
            self.disk_textvars.append(text_var)

        # Checking the consistency
        assert len(self.disk_labels) == len(self.disk_textvars)
        
        self.update_disk_info()

    def update_disk_info(self):
        # Updating the information of each disk every second
        for i, (label, text_var) in enumerate(zip(self.disk_labels, self.disk_textvars)):
            device_path = text_var.get().split(':')[0]
            if not device_path.endswith(':\\'):
                device_path += ':\\'
            
            disk_usage = psutil.disk_usage(device_path)
            
            text_var.set(f'{device_path}: {disk_usage.percent:.2f}%')

        self.after(1000, self.update_disk_info)

if __name__ == "__main__":
    app = DiskMonitorApp()
    app.mainloop()