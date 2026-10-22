"""
================================================================================
SMART AI CHATBOT - DESKTOP GUI APPLICATION
================================================================================
Description: A modern desktop Graphical User Interface (GUI) for the Smart AI
             Chatbot built using Python's built-in `tkinter` library.
             Provides a sleek dark-themed chat window with quick action buttons,
             scrollable chat log, and real-time status tracking.

Author:      B.Tech AI Student
Language:    Python 3.8+ (Standard Library Tkinter)
================================================================================
"""

import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from chatbot import ChatState, process_response, match_exit, get_help_menu, get_current_date, get_current_time


class ChatbotGUI:
    """
    Tkinter Graphical User Interface application for Smart AI Chatbot.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart AI Chatbot - B.Tech AI Minor Project")
        self.root.geometry("750x700")
        self.root.minsize(650, 550)

        # Initialize Chatbot state
        self.state = ChatState()

        # Apply dark modern color scheme
        self.bg_dark = "#181825"       # Window background
        self.card_bg = "#1e1e2e"       # Header / frames
        self.chat_bg = "#11111b"       # Chat area
        self.user_color = "#89b4fa"    # User message highlight (Blue)
        self.bot_color = "#a6e3a1"     # Bot message highlight (Green)
        self.system_color = "#cba6f7"  # System highlight (Purple)
        self.text_color = "#cdd6f4"    # Default text color
        self.entry_bg = "#313244"      # Input box background
        self.btn_bg = "#45475a"        # Button background
        self.btn_hover = "#585b70"     # Button hover

        self.root.configure(bg=self.bg_dark)

        # Build UI Components
        self.create_header()
        self.create_name_bar()
        self.create_chat_area()
        self.create_quick_buttons()
        self.create_input_area()
        self.create_status_bar()

        # Display initial welcome message
        self.display_system_message("🤖 Welcome to Smart AI Chatbot! Enter your name above and start chatting.")

    def create_header(self):
        """Creates top banner header."""
        header_frame = tk.Frame(self.root, bg=self.card_bg, pady=10)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="🤖 SMART AI CHATBOT",
            font=("Helvetica", 16, "bold"),
            fg=self.system_color,
            bg=self.card_bg
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="B.Tech AI Minor Project • Rule-Based Natural Language Processing",
            font=("Helvetica", 9, "italic"),
            fg="#a6adc8",
            bg=self.card_bg
        )
        subtitle_label.pack()

    def create_name_bar(self):
        """Creates user name registration bar."""
        name_frame = tk.Frame(self.root, bg=self.card_bg, padx=15, pady=5)
        name_frame.pack(fill=tk.X, side=tk.TOP, pady=2)

        lbl = tk.Label(name_frame, text="Your Name:", font=("Helvetica", 10, "bold"), fg=self.text_color, bg=self.card_bg)
        lbl.pack(side=tk.LEFT, padx=(0, 10))

        self.name_entry = tk.Entry(name_frame, font=("Helvetica", 10), bg=self.entry_bg, fg=self.text_color, insertbackground="white", width=20)
        self.name_entry.insert(0, self.state.user_name)
        self.name_entry.pack(side=tk.LEFT, padx=(0, 10))

        btn_save = tk.Button(
            name_frame, text="Set Name", font=("Helvetica", 9, "bold"),
            bg="#89b4fa", fg="#11111b", activebackground="#74c7ec",
            relief=tk.FLAT, padx=10, command=self.save_user_name
        )
        btn_save.pack(side=tk.LEFT)

    def save_user_name(self):
        """Saves user name from entry field."""
        new_name = self.name_entry.get().strip()
        if new_name:
            self.state.set_user_name(new_name)
            self.display_system_message(f"✅ Name updated to: {self.state.user_name}")
            self.update_status()

    def create_chat_area(self):
        """Creates scrollable text area for conversation logs."""
        chat_frame = tk.Frame(self.root, bg=self.bg_dark, padx=10, pady=5)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(chat_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_display = tk.Text(
            chat_frame,
            wrap=tk.WORD,
            bg=self.chat_bg,
            fg=self.text_color,
            font=("Consolas", 10),
            padx=12,
            pady=12,
            yscrollcommand=self.scrollbar.set,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.chat_display.yview)

        # Configure tags for custom colors
        self.chat_display.tag_config("user", foreground=self.user_color, font=("Consolas", 10, "bold"))
        self.chat_display.tag_config("bot", foreground=self.bot_color, font=("Consolas", 10))
        self.chat_display.tag_config("system", foreground=self.system_color, font=("Consolas", 9, "italic"))

    def create_quick_buttons(self):
        """Creates toolbar of quick prompt buttons."""
        quick_frame = tk.Frame(self.root, bg=self.card_bg, padx=10, pady=6)
        quick_frame.pack(fill=tk.X, side=tk.TOP)

        btn_specs = [
            ("❓ Help", "help"),
            ("📅 Date", "what is the date?"),
            ("🕒 Time", "what time is it?"),
            ("😄 Joke", "tell me a joke"),
            ("💡 AI Fact", "share an AI fact"),
            ("🧹 Clear", "__CLEAR__")
        ]

        for text, cmd in btn_specs:
            if cmd == "__CLEAR__":
                btn = tk.Button(
                    quick_frame, text=text, font=("Helvetica", 8, "bold"),
                    bg="#f38ba8", fg="#11111b", relief=tk.FLAT, padx=8, pady=2,
                    command=self.clear_chat
                )
            else:
                btn = tk.Button(
                    quick_frame, text=text, font=("Helvetica", 8),
                    bg=self.btn_bg, fg=self.text_color, activebackground=self.btn_hover,
                    relief=tk.FLAT, padx=8, pady=2,
                    command=lambda c=cmd: self.send_quick_command(c)
                )
            btn.pack(side=tk.LEFT, padx=3)

    def create_input_area(self):
        """Creates message entry box and send button."""
        input_frame = tk.Frame(self.root, bg=self.card_bg, padx=10, pady=10)
        input_frame.pack(fill=tk.X, side=tk.TOP)

        self.user_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 11),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground="white",
            relief=tk.FLAT
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=5)
        self.user_entry.bind("<Return>", lambda event: self.handle_send())
        self.user_entry.focus_set()

        self.btn_send = tk.Button(
            input_frame,
            text="Send ➔",
            font=("Helvetica", 10, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            relief=tk.FLAT,
            padx=15,
            ipady=3,
            command=self.handle_send
        )
        self.btn_send.pack(side=tk.RIGHT)

    def create_status_bar(self):
        """Creates bottom status bar."""
        self.status_frame = tk.Frame(self.root, bg="#11111b", padx=10, pady=3)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(
            self.status_frame,
            text="Status: Active • Turns: 0",
            font=("Helvetica", 8),
            fg="#a6adc8",
            bg="#11111b"
        )
        self.status_label.pack(side=tk.LEFT)

        time_label = tk.Label(
            self.status_frame,
            text=f"Session Date: {get_current_date()}",
            font=("Helvetica", 8),
            fg="#a6adc8",
            bg="#11111b"
        )
        time_label.pack(side=tk.RIGHT)

    def display_message(self, sender: str, message: str, tag: str):
        """Appends formatted message to chat area."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def display_system_message(self, message: str):
        """Appends system notification message."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[System] {message}\n", "system")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_quick_command(self, command_text: str):
        """Executes predefined command from quick bar."""
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, command_text)
        self.handle_send()

    def clear_chat(self):
        """Clears chat display history."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.display_system_message("Chat window cleared.")

    def update_status(self):
        """Updates turn count in status bar."""
        self.status_label.config(text=f"User: {self.state.user_name} • Turns: {self.state.conversation_count}")

    def handle_send(self):
        """Processes user message input from entry box."""
        user_text = self.user_entry.get().strip()
        if not user_text:
            return

        self.user_entry.delete(0, tk.END)
        self.display_message(self.state.user_name, user_text, "user")
        self.state.increment_conversation()
        self.update_status()

        # Check for exit command
        if match_exit(user_text):
            farewell = f"Goodbye {self.state.user_name}! Have a great day! 👋 🤖"
            self.display_message("Bot", farewell, "bot")
            messagebox.showinfo("Session Ended", farewell)
            self.root.destroy()
            return

        # Process response via core rule engine
        bot_response = process_response(user_text, self.state)
        self.display_message("Bot", bot_response, "bot")


def launch_gui():
    """Launches Desktop GUI Application."""
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
