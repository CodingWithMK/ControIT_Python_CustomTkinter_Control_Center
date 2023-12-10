import customtkinter
import keyboard

class KeyboardBlocker(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Keyboard Blocker")

        self.keyboard_block_var = customtkinter.BooleanVar()
        self.block_switch = customtkinter.CTkSwitch(self, text="Block Keyboard", variable=self.keyboard_block_var, command=self.disable_keyboard_input)
        self.block_switch.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")


    def disable_keyboard_input(self):
        for i in range(150):
            if self.keyboard_block_var.get():
                keyboard.block_key(i)
            else:
                keyboard.unhook(i)
            

if __name__ == "__main__":
    app = KeyboardBlocker()
    app.mainloop()