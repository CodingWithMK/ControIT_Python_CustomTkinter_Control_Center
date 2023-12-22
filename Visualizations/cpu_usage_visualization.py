import customtkinter
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUusageVisualization(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CPU Usage Visualization")

        # CPU Usage Label
        self.cpu_label = customtkinter.CTkLabel(self, text='CPU Usage:')
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.cpu_usage = customtkinter.CTkLabel(self, text='')
        self.cpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # CPU Usage Lineplot
        self.figure, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.line, = self.ax.plot([], [], label='CPU Usage')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('CPU Usage (%)')
        self.ax.legend(loc='upper left')

        # Setting y-axis percentage from 0 to 100
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()
        
        self.update_cpu_info()

    def update_cpu_info(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.configure(text=f'{cpu_percent:.2f}%')

            # Updating Lineplot Data
            x_data = self.line.get_xdata()
            y_data = self.line.get_ydata()

            x_data = list(x_data) + [time.time() - self.start_time]
            y_data = list(y_data) +[cpu_percent]

            self.line.set_xdata(x_data)
            self.line.set_ydata(y_data)

            # Limiting data points to the last 10 seconds
            self.ax.set_xlim(max(0, time.time() - self.start_time - 10), time.time() - self.start_time)

            self.canvas.draw()

        except Exception as e:
            print(f'Error updating CPU info: {e}')

        self.after(1000, self.update_cpu_info)

if __name__ == '__main__':
    app = CPUusageVisualization()
    app.mainloop()