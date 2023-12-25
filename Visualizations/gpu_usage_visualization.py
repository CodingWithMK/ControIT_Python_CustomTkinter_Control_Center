import customtkinter
import GPUtil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

class GPUusageVisualization(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('GPU Usage Visualization')

        # GPU Usage Label
        self.gpu_label = customtkinter.CTkLabel(self, text='GPU Usage:')
        self.gpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.gpu_usage = customtkinter.CTkLabel(self, text='')
        self.gpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # GPU Usage Lineplot

        self.figure, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.line, = self.ax.plot([], [], label='GPU Usage')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('GPU Usage (%)')
        self.ax.legend(loc='upper left')

        # Setting limit of y-axis from 0 to 100
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()

        self.update_gpu_info()

    def update_gpu_info(self):
        try:
            gpu_percent = GPUtil.getGPUs()[0].load * 100
            self.gpu_usage.configure(text=f'{gpu_percent:.2f}%')

            # Updating the Lineplot
            x_data = self.line.get_xdata()
            y_data = self.line.get_ydata()

            x_data = list(x_data) + [time.time() - self.start_time]
            y_data = list(y_data) + [gpu_percent]

            self.line.set_xdata(x_data)
            self.line.set_ydata(y_data)

            # Limitting data points to the last 10 seconds
            self.ax.set_xlim(max(0, time.time() - self.start_time - 10, time.time() - self.start_time()))

            self.canvas.draw()

        except Exception as e:
            print(f'Error updating GPU info: {e}')

        self.after(1000, self.update_gpu_info)

if __name__ == '__main__':
    app = GPUusageVisualization()
    app.mainloop()