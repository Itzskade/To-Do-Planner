import tkinter as tk
import atexit
from planner import MinimalistPlanner

@atexit.register
def goodbye_message():
    print("\033[0;34m[INFO]\033[0m To Do Planner was closed!")

if __name__ == '__main__':
    root = tk.Tk()
    app = MinimalistPlanner(root)
    try:
        app.run()
    except KeyboardInterrupt:
        print(goodbye_message())