#!/usr/bin/env python3
# soundex_gui.py
# Version 1.0.0 vom 15.06.2025

"""
GUI-Tool für deutschen Soundex-Abgleich in CSV-Dateien

Beschreibung:
Dieses Programm bietet eine grafische Oberfläche zur Auswahl einer CSV-Datei und zur Auswahl von Spalten,
für die ein phonetischer Soundex-Code nach deutschen Aussprache-Regeln berechnet wird.
Die Verarbeitung erfolgt über die Funktion csv_soundex() aus der Datei csv_soundex.py.
Die neuen Spalten werden als <Spalte>_soundex in einer neuen Datei gespeichert.

Funktionen:
- Auswahl einer CSV-Datei per Dialog
- Anzeige des Dateipfads mit intelligentem Zeilenumbruch an Verzeichnis-Trennern
- Anzeige der Spaltenüberschriften mit Mehrfachauswahl (Checkboxen), gruppiert in Spalten zu je 10 Zeilen
- Buttons für INFO (Beschreibung), Bearbeiten (Soundex-Verarbeitung starten), Beenden (Programm schließen)
- Nach der Verarbeitung wird der Pfad der Ausgabedatei angezeigt
- Fenstergröße 600x400, horizontal veränderbar

Version: 1.0.0 vom 15.06.2025
Autor: Dieter Eckstein
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import importlib.util

# Dynamischer Import von csv_soundex.py
spec = importlib.util.spec_from_file_location("csv_soundex", os.path.join(os.path.dirname(__file__), "csv_soundex.py"))
csv_soundex_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csv_soundex_mod)

def smart_path_wrap(path, maxlen=60):
    """
    Gibt den Pfad mit Zeilenumbruch an Verzeichnis-Trennern zurück,
    sodass jede Zeile (außer der letzten) mit einem Trenner endet,
    wenn sie zu lang wird.
    """
    norm_path = path.replace("\\", "/")
    parts = norm_path.split("/")
    lines = []
    current_line = ""
    for i, part in enumerate(parts):
        # +1 für den "/" (außer am Anfang)
        if current_line and len(current_line) + len(part) + 1 > maxlen:
            lines.append(current_line + "/")
            current_line = part
        else:
            if current_line:
                current_line += "/" + part
            else:
                current_line = part
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


class SoundexGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Deutscher Soundex für CSV")
        self.geometry("600x400")
        self.resizable(True, False)

        self.csv_file = None
        self.headers = []
        self.check_vars = []
        self.checkbuttons = []
        self.check_frame = None

        self.file_label_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Datei-Auswahl
        file_frame = tk.Frame(self)
        file_frame.pack(pady=10)
        tk.Button(file_frame, text="📂 CSV-Datei auswählen", command=self.select_file).pack(side=tk.LEFT)
        tk.Label(file_frame, textvariable=self.file_label_var, wraplength=400, anchor="w", justify="left", fg="blue").pack(side=tk.LEFT, padx=10)

        # LabelFrame für die Überschriften mit Abstand zu den Seiten
        self.lf_headers = tk.LabelFrame(self, text=" [ Überschriften ] ")
        self.lf_headers.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.check_frame = tk.Frame(self.lf_headers)
        self.check_frame.pack(fill=tk.BOTH, expand=True)

        # Button-Leiste unten, gleichmäßig verteilt
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        info_btn = tk.Button(button_frame, text="ℹ️ INFO", width=12, command=self.show_info)
        info_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        edit_btn = tk.Button(button_frame, text="🛠️ Bearbeiten", width=12, command=self.process_csv)
        edit_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        quit_btn = tk.Button(button_frame, text="❌ Beenden", width=12, command=self.quit)
        quit_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def select_file(self):
        filetypes = [("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        filename = filedialog.askopenfilename(title="CSV-Datei auswählen", filetypes=filetypes)
        if filename:
            self.csv_file = filename
            self.file_label_var.set(smart_path_wrap(filename, maxlen=60))
            self.load_headers()
            self.show_checkboxes()
        else:
            self.file_label_var.set("")

    def load_headers(self):
        self.headers = []
        try:
            with open(self.csv_file, encoding="utf-8") as f:
                reader = csv.reader(f)
                self.headers = next(reader)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Lesen der CSV-Datei:\n{e}")
            self.headers = []

    def show_checkboxes(self):
        # Vorherige Checkboxen entfernen
        for widget in self.check_frame.winfo_children():
            widget.destroy()
        self.check_vars = []
        self.checkbuttons = []

        if not self.headers:
            return

        # Spalten zu je 10 Zeilen
        num_cols = (len(self.headers) + 9) // 10
        for col in range(num_cols):
            col_frame = tk.Frame(self.check_frame)
            col_frame.grid(row=0, column=col, padx=5, sticky="n")
            for i in range(10):
                idx = col * 10 + i
                if idx < len(self.headers):
                    var = tk.BooleanVar()
                    chk = tk.Checkbutton(col_frame, text=self.headers[idx], variable=var)
                    chk.pack(anchor="w")
                    self.check_vars.append(var)
                    self.checkbuttons.append(chk)

    def get_selected_columns(self):
        return [header for header, var in zip(self.headers, self.check_vars) if var.get()]

    def process_csv(self):
        if not self.csv_file:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie zuerst eine CSV-Datei aus.")
            return
        selected_columns = self.get_selected_columns()
        if not selected_columns:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie mindestens eine Spalte aus.")
            return
        try:
            output_file = csv_soundex_mod.csv_soundex(self.csv_file, selected_columns)
            if output_file is None:
                base, ext = os.path.splitext(self.csv_file)
                output_file = f"{base}_soundex{ext}"
            messagebox.showinfo("Fertig", f"Die Verarbeitung ist abgeschlossen.\nDie neue Datei wurde erstellt:\n{os.path.abspath(output_file)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Verarbeitung:\n{e}")

    def show_info(self):
        info_text = (
            "Deutscher Soundex für CSV-Dateien\n"
            "Version 1.0.0 (15.06.2025)\n\n"
            "Dieses Programm ermöglicht die Auswahl einer CSV-Datei und die Markierung von Spalten, "
            "für die ein phonetischer Soundex-Code nach deutschen Aussprache-Regeln berechnet wird. "
            "Die Verarbeitung erfolgt durch die Funktion csv_soundex() aus der Datei csv_soundex.py.\n\n"
            "Die neuen Spalten werden als <Spalte>_soundex in einer neuen Datei gespeichert."
        )
        messagebox.showinfo("INFO", info_text)

if __name__ == "__main__":
    app = SoundexGUI()
    app.mainloop()
