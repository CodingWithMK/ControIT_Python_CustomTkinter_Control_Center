import customtkinter
import tkinter
import tkinter.messagebox
import psutil
import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from screen_brightness_control import get_brightness, set_brightness

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')



class ControITApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ControIT")

        # Hardware Usage Monitoring Widgets
        self.cpu_label = customtkinter.CTkLabel(self, text='CPU:')
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.cpu_usage = customtkinter.CTkLabel(self, text='')
        self.cpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.memory_label = customtkinter.CTkLabel(self, text='RAM:')
        self.memory_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.memory_usage = customtkinter.CTkLabel(self, text='')
        self.memory_usage.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Keyboard Input Blocker Widgets
        self.keyboard_block_var = customtkinter.BooleanVar()
        self.blocker_switch = customtkinter.CTkSwitch(self, text='Keyboard Blocker', variable=self.keyboard_block_var, command=self.disable_keyboard_input)
        self.blocker_switch.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self.update_hardware_info()

        # Disk Labels
        self.disk_labels = []
        self.disk_textvars = []

        for i, disk in enumerate(psutil.disk_partitions()):
            text_var = tkinter.StringVar()
            text_var.set(f'{disk.device}: {0.0}%')
            label = customtkinter.CTkLabel(self, textvariable=text_var)
            label.grid(row=i + 3, column=0, padx=10, pady=5, sticky='w')
            self.disk_labels.append(label)
            self.disk_textvars.append(text_var)

        # Checking the consistency
        assert len(self.disk_labels) == len(self.disk_textvars)

        self.update_disk_info()

        # Volume Slider
        self.volume_label = customtkinter.CTkLabel(self, text='Volume:')
        self.volume_label.grid(row=5)
        self.volume_slider = customtkinter.CTkSlider(self, from_=0, to=100, orientation='horizontal', command=self.set_volume)
        self.volume_slider.grid(row=6)

        # Brightness Slider
        self.brightness_label = customtkinter.CTkLabel(self, text='Brightness')
        self.brightness_label.grid(row=7)
        self.brightness_slider = customtkinter.CTkSlider(self, from_=0, to=100, number_of_steps=10, orientation='horizontal', command=self.set_brightness)
        self.brightness_slider.grid(row=8)

        # Getting default playback device for volume control
        devices = AudioUtilities.GetSpeakers()
        self.volume_control = cast(devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume)
        )

        # Getting brightness control interface
        self.brightness_control = get_brightness(display=0)

    
    
    def update_hardware_info(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        self.cpu_usage.configure(text=f'{cpu_percent:.2f}%')
        self.memory_usage.configure(text=f'{memory_percent:.2f}%')

        self.after(1000, self.update_hardware_info)

    def update_disk_info(self):
        for i, (label, text_var) in enumerate(zip(self.disk_labels, self.disk_textvars)):
            device_path = text_var.get().split(':')[0]
            if not device_path.endswith(':\\'):
                device_path += ':\\'

            disk_usage = psutil.disk_usage(device_path)

            text_var.set(f'{device_path}: {disk_usage.percent:.2f}%')

        self.after(1000, self.update_disk_info)

    def disable_keyboard_input(self):
        for i in range(150):
            if self.keyboard_block_var.get():
                keyboard.block_key(i)
            else:
                keyboard.unhook(i)

    def set_volume(self, value):
        volume = int(value)
        # Setting systme volume using pycaw
        self.volume_control.SetMasterVolumeLevelScalar(float(volume / 100), None)

    def set_brightness(self, value):
        brightness = int(value)
        # Setting screen brightness using screen-brightness-control
        set_brightness(display=0, value=brightness)


if __name__ == '__main__':
    app = ControITApp()
    app.mainloop()


