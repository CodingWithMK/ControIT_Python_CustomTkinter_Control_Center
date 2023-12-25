import customtkinter
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

class DiskUsageVisualization(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Disk Usage Visualization')

        # Disk Labels
        self.disk_labels = []
        self.disk_textvars = []

        for i, disk in enumerate(psutil.disk_partitions()):
            text_var = customtkinter.StringVar()
            text_var.set(f'{disk.device}: {0.0}%')
            
            label = customtkinter.CTkLabel(self, textvariable=text_var)
            label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            self.disk_labels.append(label)
            self.disk_textvars.append(text_var)

        # Disk Usage Lineplot
        self.figure, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.lines = []
        for i in range(len(self.disk_labels)):
            line, = self.ax.plot([], [], label=f'Disk {i} Usage')
            self.lines.append(line)

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Disk Usage (%)')
        self.ax.legend(loc='upper left')

        # Setting the y-axis from 0 to 100
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=len(self.disk_labels), column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()

        self.update_disk_info()

    def update_disk_info(self):
        try:
            # Updating the informaion of each disk every second
            for i, (label, text_var) in enumerate(zip(self.disk_labels, self.disk_textvars)):
                device_path = text_var.get().split(':')[0]
                if not device_path.endswith(':\\'):
                    device_path += ':\\'

                disk_usage = psutil.disk_usage(device_path)

                text_var.set(f'{device_path}: {disk_usage.percent:.2f}%')

                # Updating Lineplot
                x_data = self.lines[i].get_xdata()
                y_data = self.lines[i].get_ydata()

                x_data = list(x_data) + [time.time() - self.start_time]
                y_data = list(y_data) + [disk_usage.percent]

                self.lines[i].set_xdata(x_data)
                self.lines[i].set_ydata(y_data)

                # Limitting data points to the last 10 seconds
                self.ax.set_xlim(max(0, time.time() - self.start_time - 10), time.time() - self.start_time)
                
            self.canvas.draw()

        except Exception as e:
            print(f'Error updating disk info: {e}')

        self.after(1000, self.update_disk_info)

if __name__ == '__main__':
    app = DiskUsageVisualization()
    app.mainloop()
