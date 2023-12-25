import customtkinter
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

class MemoryUsageVisualization(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('RAM Usage Visualizaton')

        # RAM Usage Label
        self.memory_label = customtkinter.CTkLabel(self, text='RAM Usage:')
        self.memory_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.memory_usage = customtkinter.CTkLabel(self, text='')
        self.memory_usage.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # RAM Usage Lineplot
        self.figure, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.line, = self.ax.plot([], [], label='RAM Usage')
        self.ax.set_xlabel('Time (s)')

        # Setting y-axis percentage from 0 to 100
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()

        self.update_memory_info()

    def update_memory_info(self):
        try:
            memory_percent = psutil.virtual_memory().percent
            self.memory_usage.configure(text=f'{memory_percent:.2f}%')

            # Updating the Lineplot
            x_data = self.line.get_xdata()
            y_data = self.line.get_ydata()

            x_data = list(x_data) + [time.time() - self.start_time]
            y_data = list(y_data) + [memory_percent]

            self.line.set_xdata(x_data)
            self.line.set_ydata(y_data)

            # Limitting data points to the last 10 seconds
            self.ax.set_xlim(max(0, time.time() - self.start_time - 10), time.time() - self.start_time)

            self.canvas.draw()
        
        except Exception as e:
            print(f'Error updating RAM info: {e}')

        self.after(100, self.update_memory_info)

if __name__ == '__main__':
    app = MemoryUsageVisualization()
    app.mainloop()
