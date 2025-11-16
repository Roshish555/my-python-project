import tkinter as tk
from tkinter import messagebox
import random


class AlgebraPracticeITS:
    def __init__(self, root):
        self.root = root
        self.root.title("Algebra Practice ITS - Linear Equations Tutor")
        self.root.geometry("900x520")
        self.root.configure(bg="#1E1E2E")  # dark background so it looks modern

        # State
        self.current_x = None
        self.current_steps = []
        self.hint_index = 0
        self.correct = 0
        self.total = 0

        # ---------- TOP HEADER ----------
        header = tk.Frame(root, bg="#282A36", height=70)
        header.pack(side=tk.TOP, fill=tk.X)

        title = tk.Label(
            header,
            text="Algebra Practice Intelligent Tutoring System",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#282A36"
        )
        title.pack(pady=5)

        subtitle = tk.Label(
            header,
            text="Solving equations of the form  ax + b = c",
            font=("Segoe UI", 11),
            fg="#CFCFEA",
            bg="#282A36"
        )
        subtitle.pack()

        # ---------- MAIN AREA (LEFT + RIGHT) ----------
        main_area = tk.Frame(root, bg="#1E1E2E")
        main_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ----- LEFT PANEL: question, input, buttons, score -----
        left_panel = tk.Frame(main_area, bg="#232634", bd=2, relief="ridge")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        # Equation display
        self.eq_var = tk.StringVar()
        eq_title = tk.Label(
            left_panel,
            text="Current Equation",
            font=("Segoe UI", 12, "bold"),
            fg="#F8F8F2",
            bg="#232634"
        )
        eq_title.pack(pady=(10, 2))

        eq_label = tk.Label(
            left_panel,
            textvariable=self.eq_var,
            font=("Segoe UI", 12),
            fg="#BD93F9",
            bg="#232634"
        )
        eq_label.pack(pady=(0, 10))

        # Answer input
        answer_box = tk.Frame(left_panel, bg="#232634")
        answer_box.pack(pady=5)

        ans_label = tk.Label(
            answer_box,
            text="Your answer for  x  =",
            font=("Segoe UI", 11),
            fg="#F8F8F2",
            bg="#232634"
        )
        ans_label.pack(side=tk.LEFT)

        self.answer_var = tk.StringVar()
        ans_entry = tk.Entry(
            answer_box,
            textvariable=self.answer_var,
            width=8,
            font=("Segoe UI", 12)
        )
        ans_entry.pack(side=tk.LEFT, padx=5)

        # Buttons row 1
        btn_row1 = tk.Frame(left_panel, bg="#232634")
        btn_row1.pack(pady=(15, 5))

        new_btn = tk.Button(
            btn_row1,
            text="New Question",
            command=self.new_question,
            font=("Segoe UI", 10, "bold"),
            bg="#50FA7B",
            fg="#000000",
            width=14
        )
        new_btn.grid(row=0, column=0, padx=4, pady=2)

        check_btn = tk.Button(
            btn_row1,
            text="Check Answer",
            command=self.check_answer,
            font=("Segoe UI", 10, "bold"),
            bg="#6272A4",
            fg="#FFFFFF",
            width=14
        )
        check_btn.grid(row=0, column=1, padx=4, pady=2)

        # Buttons row 2
        btn_row2 = tk.Frame(left_panel, bg="#232634")
        btn_row2.pack(pady=(5, 10))

        hint_btn = tk.Button(
            btn_row2,
            text="Hint",
            command=self.show_hint,
            font=("Segoe UI", 10, "bold"),
            bg="#FFB86C",
            fg="#000000",
            width=14
        )
        hint_btn.grid(row=0, column=0, padx=4, pady=2)

        solution_btn = tk.Button(
            btn_row2,
            text="Show Full Solution",
            command=self.show_full_solution,
            font=("Segoe UI", 10, "bold"),
            bg="#BD93F9",
            fg="#000000",
            width=14
        )
        solution_btn.grid(row=0, column=1, padx=4, pady=2)

        # Score display
        self.score_var = tk.StringVar(value="Score: 0 / 0")
        score_label = tk.Label(
            left_panel,
            textvariable=self.score_var,
            font=("Segoe UI", 11, "bold"),
            fg="#8BE9FD",
            bg="#232634"
        )
        score_label.pack(pady=(10, 5))

        tip_label = tk.Label(
            left_panel,
            text="Try to solve first.\nUse hints only when stuck.",
            font=("Segoe UI", 9),
            fg="#F8F8F2",
            bg="#232634",
            justify="center"
        )
        tip_label.pack(pady=(0, 15))

        # ---------- RIGHT PANEL: explanation ----------
        right_panel = tk.Frame(main_area, bg="#232634", bd=2, relief="ridge")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        explain_title = tk.Label(
            right_panel,
            text="Tutor Feedback & Hints",
            font=("Segoe UI", 12, "bold"),
            fg="#F8F8F2",
            bg="#232634"
        )
        explain_title.pack(pady=(10, 2))

        self.explain_box = tk.Text(
            right_panel,
            height=15,
            width=60,
            state="disabled",
            wrap="word",
            font=("Segoe UI", 11),
            bg="#1E1E2E",
            fg="#F8F8F2",
            relief="flat"
        )
        self.explain_box.pack(padx=10, pady=8, fill=tk.BOTH, expand=True)

        # ---------- BOTTOM BAR WITH YOUR NAME ----------
        bottom_bar = tk.Frame(root, bg="#1E1E2E")
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5))

        credit_button = tk.Button(
            bottom_bar,
            text="Made by Roshish",
            font=("Segoe UI", 10, "bold"),
            bg="#44475A",
            fg="#F8F8F2",
            relief="groove",
            command=self.show_credit
        )
        credit_button.pack(pady=2)

        # Start with one question
        self.new_question()

    # ------------ Core tutoring logic ------------
    def generate_equation(self):
        """
        Random equation of the form ax + b = c with integer solution x.
        """
        x = random.randint(-10, 10)
        a = random.choice([i for i in range(-5, 6) if i not in (0,)])
        b = random.randint(-10, 10)
        c = a * x + b

        # Build left side string
        if a == 1:
            a_part = "x"
        elif a == -1:
            a_part = "-x"
        else:
            a_part = f"{a}x"

        if b > 0:
            left = f"{a_part} + {b}"
        elif b < 0:
            left = f"{a_part} - {abs(b)}"
        else:
            left = a_part

        equation_str = f"{left} = {c}"

        steps = []
        steps.append(f"Step 1: Start with the equation: {equation_str}")

        # Move b to the right side
        if b != 0:
            if b > 0:
                steps.append(f"Step 2: Subtract {b} from both sides to move the constant.")
                rhs_after = c - b
                steps.append(f"        {a_part} = {c} - {b} = {rhs_after}")
            else:  # b < 0
                steps.append(f"Step 2: Add {abs(b)} to both sides to move the constant.")
                rhs_after = c - b  # minus negative is plus
                steps.append(f"        {a_part} = {c} + {abs(b)} = {rhs_after}")
        else:
            rhs_after = c
            steps.append(f"Step 2: There is no constant term, so we already have {a_part} = {rhs_after}.")

        # Divide or multiply to isolate x
        if a not in (1, -1):
            steps.append(f"Step 3: Divide both sides by {a} to isolate x.")
            steps.append(f"        x = {rhs_after} / {a}")
        elif a == -1:
            steps.append("Step 3: Multiply both sides by -1 to change -x into x.")
            steps.append(f"        x = {rhs_after} × (-1)")

        steps.append(f"Step 4: The solution is x = {x}.")
        steps.append("Great work! This is how we solve ax + b = c step by step.")

        return equation_str, x, steps

    # ------------ Button actions ------------
    def new_question(self):
        self.explain_box.config(state="normal")
        self.explain_box.delete("1.0", tk.END)
        self.explain_box.insert(tk.END, "New question generated. Try to solve it yourself first.\n")
        self.explain_box.config(state="disabled")

        self.answer_var.set("")
        self.hint_index = 0

        eq_str, x, steps = self.generate_equation()
        self.eq_var.set(eq_str)
        self.current_x = x
        self.current_steps = steps

    def check_answer(self):
        if self.current_x is None:
            messagebox.showinfo("Info", "Click 'New Question' first.")
            return

        ans_text = self.answer_var.get().strip()
        if ans_text == "":
            messagebox.showwarning("Warning", "Please enter a value for x.")
            return

        try:
            user_x = float(ans_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric value for x.")
            return

        self.total += 1
        if abs(user_x - self.current_x) < 1e-6:
            self.correct += 1
            feedback = f"✅ Correct! x = {self.current_x}."
        else:
            feedback = f"❌ Not quite. Your answer: {user_x}, correct answer: {self.current_x}."

        self.score_var.set(f"Score: {self.correct} / {self.total}")

        self.explain_box.config(state="normal")
        self.explain_box.insert(tk.END, "\n" + feedback + "\n")
        self.explain_box.config(state="disabled")

    def show_hint(self):
        if not self.current_steps:
            messagebox.showinfo("Info", "No question loaded yet.")
            return

        if self.hint_index >= len(self.current_steps):
            messagebox.showinfo("Info", "No more hints. You can view the full solution.")
            return

        self.explain_box.config(state="normal")
        self.explain_box.insert(tk.END, "\n" + self.current_steps[self.hint_index] + "\n")
        self.explain_box.config(state="disabled")

        self.hint_index += 1

    def show_full_solution(self):
        if not self.current_steps:
            messagebox.showinfo("Info", "No question loaded yet.")
            return

        self.explain_box.config(state="normal")
        self.explain_box.insert(tk.END, "\nFull solution:\n")
        for step in self.current_steps:
            self.explain_box.insert(tk.END, step + "\n")
        self.explain_box.config(state="disabled")

    def show_credit(self):
        messagebox.showinfo(
            "About",
            "This Intelligent Tutoring System was designed and implemented by Roshish."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgebraPracticeITS(root)
    root.mainloop()

