import tkinter as tk

class Window:
    def __init__(self, title):
        self.gesture = ""

        self.root = tk.Tk()
        self.root.title(title)

        # Create text entry box
        self.text_entry = tk.Text(self.root, width=50, height=20)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create Button 1
        self.button1 = tk.Button(self.root, text="Button 1", command=self.button1_clicked)
        self.button1.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ne")

        # Create Button 2
        self.button2 = tk.Button(self.root, text="Button 2", command=self.button2_clicked)
        self.button2.grid(row=0, column=1, padx=(0, 10), pady=40, sticky="ne")

        # Create "Run" button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_callback)
        self.run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Configure grid row and column weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        print("the GUI is up and running")

    def run_callback(self):
        command = self.text_entry.get("1.0", "end-1c")
        #print("command", command)
        if self.gestures != "":
            command += ". The user clicked on " + self.gestures
        r = self.agent_executor.invoke(
            {
                "input": command,
            }
        )
        self.gestures = ""
        print(r)

    def button1_clicked(self):
        self.gestures = "button 1"
        print("Button 1 clicked")

    def button2_clicked(self):
        self.gestures = "button 2"
        print("Button 2 clicked")

    def set_agent_executor(self, agent_executor):
        self.agent_executor = agent_executor

    def run(self):
        self.root.mainloop()