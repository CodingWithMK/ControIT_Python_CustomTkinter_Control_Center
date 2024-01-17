import customtkinter
from screen_brightness_control import get_brightness, set_brightness

class BrightnessControlApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Brightness Control')

        # Brightness Slider
        self.brightness_label = customtkinter.CTkLabel(self, text='Brightness')
        self.brightness_label.pack(pady=10)
        self.brightness_slider = customtkinter.CTkSlider(self, from_=0, to=100, number_of_steps=10, orientation='horizontal', command=self.set_brightness)
        self.brightness_slider.pack(pady=10)

        # Getting brightness control interface
        self.brightness_control = get_brightness(display=0)

    def set_brightness(self, value):
        brightness = int(value)
        # Setting screen brightness using screen-brightness-control
        set_brightness(display=0, value=brightness)

if __name__ == "__main__":
    app = BrightnessControlApp()
    app.mainloop()