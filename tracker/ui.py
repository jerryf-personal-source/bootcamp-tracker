from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from .storage import load_data, save_data


class BootcampApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bootcamp Tracker")
        self.root.geometry("840x520")
        self.data = load_data()

        self.selected_day_index = 0

        self._build_layout()
        self._load_day(0)

    def _build_layout(self) -> None:
        # Top bar
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        self.title_var = tk.StringVar(value="Bootcamp Tracker")
        title = ttk.Label(top, textvariable=self.title_var, font=("Helvetica", 16, "bold"))
        title.pack(side="left")

        save_btn = ttk.Button(top, text="Save", command=self._save)
        save_btn.pack(side="right")

        # Main split
        main = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        main.pack(fill="both", expand=True)

        self.left = ttk.Frame(main)
        self.left.pack(side="left", fill="y")

        self.right = ttk.Frame(main)
        self.right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        # Day list
        ttk.Label(self.left, text="Days", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 6))
        self.day_list = tk.Listbox(self.left, height=10)
        self.day_list.pack(fill="y", expand=False)
        for d in self.data.get("days", []):
            self.day_list.insert("end", f"{d.get('date')} — {d.get('title')}")
        self.day_list.bind("<<ListboxSelect>>", self._on_day_select)

        # Right content
        self.day_header_var = tk.StringVar(value="")
        ttk.Label(self.right, textvariable=self.day_header_var, font=("Helvetica", 13, "bold")).pack(anchor="w")

        self.drills_frame = ttk.Frame(self.right, padding=(0, 10, 0, 0))
        self.drills_frame.pack(fill="x")

        ttk.Label(self.right, text="Reflection").pack(anchor="w", pady=(14, 4))
        self.reflection = tk.Text(self.right, height=8, wrap="word")
        self.reflection.pack(fill="both", expand=True)

        bottom = ttk.Frame(self.right, padding=(0, 10, 0, 0))
        bottom.pack(fill="x")
        ttk.Label(bottom, text="Confidence (1–10):").pack(side="left")
        self.confidence_var = tk.StringVar(value="")
        self.confidence_entry = ttk.Entry(bottom, width=4, textvariable=self.confidence_var)
        self.confidence_entry.pack(side="left", padx=(6, 0))

        refresh_btn = ttk.Button(bottom, text="Reload", command=self._reload)
        refresh_btn.pack(side="right")

    def _clear_drills(self) -> None:
        for child in self.drills_frame.winfo_children():
            child.destroy()

    def _load_day(self, idx: int) -> None:
        days = self.data.get("days", [])
        if not days:
            return
        idx = max(0, min(idx, len(days) - 1))
        self.selected_day_index = idx

        day = days[idx]
        self.day_header_var.set(day.get("title", ""))
        self.title_var.set(f"Bootcamp Tracker — {day.get('date', '')}")

        self._clear_drills()

        ttk.Label(self.drills_frame, text="Drills", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self._drill_vars = []  # list of (var, drill_id)
        for drill in day.get("drills", []):
            var = tk.BooleanVar(value=bool(drill.get("done")))
            cb = ttk.Checkbutton(self.drills_frame, text=drill.get("text", ""), variable=var)
            cb.pack(anchor="w", pady=2)
            self._drill_vars.append((var, drill.get("id")))

        self.reflection.delete("1.0", "end")
        self.reflection.insert("1.0", day.get("reflection", ""))

        conf = day.get("confidence")
        self.confidence_var.set("" if conf is None else str(conf))

        # Update listbox selection
        self.day_list.selection_clear(0, "end")
        self.day_list.selection_set(idx)
        self.day_list.activate(idx)

    def _on_day_select(self, _event=None) -> None:
        sel = self.day_list.curselection()
        if not sel:
            return
        self._load_day(int(sel[0]))

    def _save(self) -> None:
        # Pull UI state into data model
        day = self.data["days"][self.selected_day_index]
        drill_map = {d["id"]: d for d in day.get("drills", [])}
        for var, drill_id in getattr(self, "_drill_vars", []):
            if drill_id in drill_map:
                drill_map[drill_id]["done"] = bool(var.get())

        day["reflection"] = self.reflection.get("1.0", "end").rstrip("\n")

        conf_raw = self.confidence_var.get().strip()
        if conf_raw == "":
            day["confidence"] = None
        else:
            try:
                conf = int(conf_raw)
                if conf < 1 or conf > 10:
                    raise ValueError
                day["confidence"] = conf
            except ValueError:
                messagebox.showerror("Invalid confidence", "Confidence must be an integer 1–10 (or blank).")
                return

        save_data(self.data)
        messagebox.showinfo("Saved", "Progress saved to data.json")

    def _reload(self) -> None:
        self.data = load_data()
        self._load_day(self.selected_day_index)

    def run(self) -> None:
        self.root.mainloop()
