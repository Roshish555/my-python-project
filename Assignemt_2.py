# -*- coding: utf-8 -*-
import os
import random
import tkinter as tk
from tkinter import messagebox

from owlready2 import get_ontology


class AlgebraPracticeITS:
    def __init__(self, root):
        self.root = root
        self.root.title("Algebra Practice ITS - Linear Equations Tutor (Adaptive + Ontology)")
        self.root.geometry("900x520")
        self.root.configure(bg="#1E1E2E")

        # -------------------- State --------------------
        self.current_eq_str = None
        self.current_x = None
        self.current_steps = []
        self.hint_index = 0

        self.correct = 0
        self.total = 0

        # For semantic matching
        self.current_a = None
        self.current_b = None
        self.current_c = None
        self.current_rhs_after = None

        # Adaptive difficulty
        self.level = 1
        self.streak_correct = 0
        self.streak_wrong = 0

        # Ontology
        self.onto = None
        self.current_onto_equation = None

        self.rdf_path = os.path.join(os.path.dirname(__file__), "Assisgnment.rdf")

        # -------------------- UI --------------------
        header = tk.Frame(root, bg="#282A36", height=70)
        header.pack(side=tk.TOP, fill=tk.X)

        tk.Label(
            header,
            text="Algebra Practice Intelligent Tutoring System",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#282A36"
        ).pack(pady=5)

        tk.Label(
            header,
            text="Solving equations of the form  ax + b = c  (Adaptive + Ontology Hints)",
            font=("Segoe UI", 11),
            fg="#CFCFEA",
            bg="#282A36"
        ).pack()

        main_area = tk.Frame(root, bg="#1E1E2E")
        main_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # LEFT PANEL
        left_panel = tk.Frame(main_area, bg="#232634", bd=2, relief="ridge")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        tk.Label(
            left_panel, text="Current Equation",
            font=("Segoe UI", 12, "bold"),
            fg="#F8F8F2",
            bg="#232634"
        ).pack(pady=(10, 2))

        self.eq_var = tk.StringVar(value="(press New Question)")
        tk.Label(
            left_panel,
            textvariable=self.eq_var,
            font=("Segoe UI", 12),
            fg="#BD93F9",
            bg="#232634"
        ).pack(pady=(0, 10))

        self.level_var = tk.StringVar(value="Difficulty: Easy (Level 1)")
        tk.Label(
            left_panel,
            textvariable=self.level_var,
            font=("Segoe UI", 10, "bold"),
            fg="#50FA7B",
            bg="#232634"
        ).pack(pady=(0, 10))

        # Answer input
        answer_box = tk.Frame(left_panel, bg="#232634")
        answer_box.pack(pady=5)

        tk.Label(
            answer_box,
            text="Your answer for  x  =",
            font=("Segoe UI", 11),
            fg="#F8F8F2",
            bg="#232634"
        ).pack(side=tk.LEFT)

        self.answer_var = tk.StringVar()
        tk.Entry(
            answer_box,
            textvariable=self.answer_var,
            width=10,
            font=("Segoe UI", 12)
        ).pack(side=tk.LEFT, padx=5)

        # Buttons
        btn_row1 = tk.Frame(left_panel, bg="#232634")
        btn_row1.pack(pady=(15, 5))

        tk.Button(
            btn_row1,
            text="New Question",
            command=self.new_question,
            font=("Segoe UI", 10, "bold"),
            bg="#50FA7B",
            fg="#000000",
            width=14
        ).grid(row=0, column=0, padx=4, pady=2)

        tk.Button(
            btn_row1,
            text="Check Answer",
            command=self.check_answer,
            font=("Segoe UI", 10, "bold"),
            bg="#6272A4",
            fg="#FFFFFF",
            width=14
        ).grid(row=0, column=1, padx=4, pady=2)

        btn_row2 = tk.Frame(left_panel, bg="#232634")
        btn_row2.pack(pady=(5, 10))

        tk.Button(
            btn_row2,
            text="Hint",
            command=self.show_hint,
            font=("Segoe UI", 10, "bold"),
            bg="#FFB86C",
            fg="#000000",
            width=14
        ).grid(row=0, column=0, padx=4, pady=2)

        tk.Button(
            btn_row2,
            text="Show Full Solution",
            command=self.show_full_solution,
            font=("Segoe UI", 10, "bold"),
            bg="#BD93F9",
            fg="#000000",
            width=14
        ).grid(row=0, column=1, padx=4, pady=2)

        self.score_var = tk.StringVar(value="Score: 0 / 0")
        tk.Label(
            left_panel,
            textvariable=self.score_var,
            font=("Segoe UI", 11, "bold"),
            fg="#8BE9FD",
            bg="#232634"
        ).pack(pady=(10, 5))

        tk.Label(
            left_panel,
            text="Adaptive rules:\n- 3 correct in a row -> harder\n- 2 wrong in a row -> easier",
            font=("Segoe UI", 9),
            fg="#F8F8F2",
            bg="#232634",
            justify="center"
        ).pack(pady=(0, 15))

        # RIGHT PANEL
        right_panel = tk.Frame(main_area, bg="#232634", bd=2, relief="ridge")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            right_panel,
            text="Tutor Feedback & Hints",
            font=("Segoe UI", 12, "bold"),
            fg="#F8F8F2",
            bg="#232634"
        ).pack(pady=(10, 2))

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

        bottom_bar = tk.Frame(root, bg="#1E1E2E")
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5))

        tk.Button(
            bottom_bar,
            text="AI Assignment",
            font=("Segoe UI", 10, "bold"),
            bg="#44475A",
            fg="#F8F8F2",
            relief="groove",
            command=self.show_credit
        ).pack(pady=2)

        # -------------------- Load ontology and start --------------------
        self.load_ontology()
        self.new_question()

    # ==================== Output helper ====================
    def tutor_say(self, text: str):
        self.explain_box.config(state="normal")
        self.explain_box.insert(tk.END, text + "\n")
        self.explain_box.config(state="disabled")
        self.explain_box.see(tk.END)

    def _update_level_label(self):
        label = "Easy" if self.level == 1 else "Medium" if self.level == 2 else "Hard"
        self.level_var.set(f"Difficulty: {label} (Level {self.level})")

    # ==================== Ontology ====================
    def load_ontology(self):
        if not os.path.exists(self.rdf_path):
            self.onto = None
            self.tutor_say(f"Ontology file not found: {self.rdf_path}")
            self.tutor_say("Put Assisgnment.rdf in the SAME folder as this .py file.")
            return
        try:
            self.onto = get_ontology(self.rdf_path).load()
            self.tutor_say(f"Ontology loaded successfully ✅ ({self.rdf_path})")
        except Exception as e:
            self.onto = None
            self.tutor_say(f"Could not load ontology. Error: {e}")

    def find_equation_in_ontology(self, a, b, c):
        if not self.onto:
            return None

        try:
            eq_instances = self.onto.Equation.instances()
        except Exception:
            eq_instances = list(self.onto.individuals())

        for eq in eq_instances:
            try:
                if not (hasattr(eq, "hasA") and hasattr(eq, "hasB") and hasattr(eq, "hasC")):
                    continue
                if not (eq.hasA and eq.hasB and eq.hasC):
                    continue
                if int(eq.hasA[0]) == int(a) and int(eq.hasB[0]) == int(b) and int(eq.hasC[0]) == int(c):
                    return eq
            except Exception:
                continue
        return None

    def get_step_texts_from_ontology_equation(self, eq_individual):
        if eq_individual is None:
            return None
        if not hasattr(eq_individual, "hasSolution") or not eq_individual.hasSolution:
            return None
        sol = eq_individual.hasSolution[0]
        if not hasattr(sol, "hasStep") or not sol.hasStep:
            return None

        texts = []
        for s in sol.hasStep:
            if hasattr(s, "stepText") and s.stepText:
                texts.append(str(s.stepText[0]))
        return texts if texts else None

    def add_equation_to_ontology(self, a, b, c, eq_str, built_steps):
        """Auto-add and save to Assisgnment.rdf"""
        if not self.onto:
            return False

        # Avoid duplicates
        if self.find_equation_in_ontology(a, b, c):
            return True

        # Create new individuals
        safe = f"{a}_{b}_{c}".replace("-", "neg")

        eq = self.onto.Equation(f"Equation_{safe}")
        eq.hasA = [int(a)]
        eq.hasB = [int(b)]
        eq.hasC = [int(c)]
        if hasattr(eq, "equationString"):
            eq.equationString = [eq_str]

        sol = self.onto.Solution(f"Solution_{safe}")
        eq.hasSolution = [sol]

        step_objs = []
        for i, t in enumerate(built_steps, start=1):
            st = self.onto.Step(f"Step_{safe}_{i}")
            if hasattr(st, "stepText"):
                st.stepText = [str(t)]
            step_objs.append(st)

        if hasattr(sol, "hasStep"):
            sol.hasStep = step_objs

        try:
            self.onto.save(file=self.rdf_path, format="rdfxml")
            return True
        except Exception as e:
            self.tutor_say(f"Save failed: {e}")
            return False

    # ==================== Adaptive difficulty ====================
    def _difficulty_ranges(self):
        if self.level == 1:
            return (-3, 3, -6, 6, -5, 5)
        if self.level == 2:
            return (-5, 5, -10, 10, -10, 10)
        return (-9, 9, -15, 15, -12, 12)

    def adapt_difficulty(self, was_correct: bool):
        if was_correct:
            self.streak_correct += 1
            self.streak_wrong = 0
            if self.streak_correct >= 3 and self.level < 3:
                self.level += 1
                self.streak_correct = 0
                self.tutor_say(f"Adaptive update: Level increased to {self.level}.")
        else:
            self.streak_wrong += 1
            self.streak_correct = 0
            if self.streak_wrong >= 2 and self.level > 1:
                self.level -= 1
                self.streak_wrong = 0
                self.tutor_say(f"Adaptive update: Level decreased to {self.level}.")
        self._update_level_label()

    # ==================== Generate equation ====================
    def generate_equation(self):
        a_min, a_max, b_min, b_max, x_min, x_max = self._difficulty_ranges()

        x = random.randint(x_min, x_max)
        a_choices = [i for i in range(a_min, a_max + 1) if i != 0]
        a = random.choice(a_choices)
        b = random.randint(b_min, b_max)
        c = a * x + b

        # String
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

        eq_str = f"{left} = {c}"

        steps = [f"Step 1: Start with the equation: {eq_str}"]

        if b != 0:
            if b > 0:
                steps.append(f"Step 2: Subtract {b} from both sides.")
                rhs_after = c - b
                steps.append(f"        {a_part} = {rhs_after}")
            else:
                steps.append(f"Step 2: Add {abs(b)} to both sides.")
                rhs_after = c - b
                steps.append(f"        {a_part} = {rhs_after}")
        else:
            rhs_after = c
            steps.append(f"Step 2: No constant term, so {a_part} = {rhs_after}.")

        if a not in (1, -1):
            steps.append(f"Step 3: Divide both sides by {a}.")
            steps.append(f"        x = {rhs_after} / {a}")
        elif a == -1:
            steps.append("Step 3: Multiply both sides by -1.")
            steps.append(f"        x = {-rhs_after}")

        steps.append(f"Step 4: The solution is x = {x}.")
        steps.append("Great work! That is the method for ax + b = c.")

        return eq_str, x, steps, a, b, c, rhs_after

    # ==================== Actions ====================
    def new_question(self):
        self.explain_box.config(state="normal")
        self.explain_box.delete("1.0", tk.END)
        self.explain_box.config(state="disabled")

        self.answer_var.set("")
        self.hint_index = 0

        eq_str, x, built_steps, a, b, c, rhs_after = self.generate_equation()

        self.current_eq_str = eq_str
        self.current_x = x
        self.current_a, self.current_b, self.current_c = a, b, c
        self.current_rhs_after = rhs_after

        self.eq_var.set(eq_str)
        self._update_level_label()

        # 1) try match
        matched = self.find_equation_in_ontology(a, b, c)

        # 2) if not match -> add and save
        if not matched:
            added = self.add_equation_to_ontology(a, b, c, eq_str, built_steps)
            if added:
                self.tutor_say("New question generated. It was NOT in ontology, so it was ADDED & SAVED ✅")
                self.load_ontology()
                matched = self.find_equation_in_ontology(a, b, c)
            else:
                self.tutor_say("New question generated. Could not add to ontology; using built-in hints.")

        # 3) use ontology steps if present
        self.current_onto_equation = matched
        if matched:
            onto_steps = self.get_step_texts_from_ontology_equation(matched)
            if onto_steps:
                self.current_steps = ["Ontology Hint: " + s for s in onto_steps]
                self.tutor_say("Ontology match found ✅ Hints come from ontology.")
            else:
                self.current_steps = built_steps
                self.tutor_say("Ontology matched but no stepText found. Using built-in hints.")
        else:
            self.current_steps = built_steps
            self.tutor_say("No ontology match. Using built-in hints.")

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
            was_correct = True
            feedback = f"✅ Correct! x = {self.current_x}."
        else:
            was_correct = False
            feedback = f"❌ Not correct. Your: {user_x} | Correct: {self.current_x}."

            if abs(user_x + self.current_x) < 1e-6:
                feedback += " Diagnosis: sign mistake."

            if self.current_a not in (1, -1) and abs(user_x - self.current_rhs_after) < 1e-6:
                feedback += f" Diagnosis: forgot to divide by {self.current_a}."

        self.score_var.set(f"Score: {self.correct} / {self.total}")
        self.tutor_say(feedback)

        self.adapt_difficulty(was_correct)

    def show_hint(self):
        if not self.current_steps:
            messagebox.showinfo("Info", "No question loaded yet.")
            return
        if self.hint_index >= len(self.current_steps):
            messagebox.showinfo("Info", "No more hints. Use full solution.")
            return

        self.tutor_say(self.current_steps[self.hint_index])
        self.hint_index += 1

    def show_full_solution(self):
        if not self.current_steps:
            messagebox.showinfo("Info", "No question loaded yet.")
            return

        self.tutor_say("Full solution:")
        for s in self.current_steps:
            self.tutor_say(s)

    def show_credit(self):
        messagebox.showinfo("About", "AI Assignment.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgebraPracticeITS(root)
    root.mainloop()
