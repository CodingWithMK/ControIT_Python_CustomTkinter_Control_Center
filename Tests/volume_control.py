import customtkinter
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class VolumeControlsApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Volume Controller')

        # Volume Slider
        self.volume_label = customtkinter.CTkLabel(self, text='Volume:')
        self.volume_label.pack(pady=10)
        self.volume_slider = customtkinter.CTkSlider(self, from_=0, to=100, orientation='horizontal', command=self.set_volume)
        self.volume_slider.pack(pady=10)

        # Gettin default playback device for volume control
        devices = AudioUtilities.GetSpeakers()
        self.volume_control = cast(devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume)
        )

    def set_volume(self, value):
        volume = int(value)
        # Setting systme volume using pycaw
        self.volume_control.SetMasterVolumeLevelScalar(float(volume / 100), None)
        

if __name__ == '__main__':
    app = VolumeControlsApp()
    app.mainloop()