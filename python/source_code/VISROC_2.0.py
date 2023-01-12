#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
try:
    from tkmacosx import Button as Buttonette
except ImportError:
    pass
import tkinter.font as tkFont
from tkinter import filedialog

from PIL import ImageTk
from PIL import Image
#import _imaging

from math import *

import os
import sys

import numpy as np
import pandas as pd

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import backend_managers
from matplotlib import backend_bases
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure

import matplotlib.colors

from matplotlib.backends import (backend_ps, backend_pdf, backend_pgf, backend_svg)

import shutil

import webbrowser

from packaging import version

import time

import clipboard

np.seterr(divide='ignore', invalid='ignore')

def adapt_os(linx = None, mswin = None, macos = None, ibm = None):
    if sys.platform == "linux":
        return(linx)
    elif sys.platform == "win32" or sys.platform == "cygwin":
        return(mswin)
    elif sys.platform == "darwin":
        return(macos)
    else:
        return(ibm)

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath("__file__")))
    return os.path.join(base_path, relative_path)


def give_path():
    if not sys.argv[0].endswith('.py') and sys.platform == "darwin":
        return(os.path.sep.join(sys.argv[0].split(os.path.sep)[:-4]))
    else:
        return(os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1]))

def save_as_file_csv(df):
    file = filedialog.asksaveasfilename(defaultextension=adapt_os(linx=None, macos=None, mswin='.csv'),
                                        initialdir = give_path(),
                                        filetypes=[("CSV (Comma delimited) files (.csv)","*.csv"),
                                                   ("All files","*.*")],
                                        title='Save File',
                                        initialfile=str(df.name))
    if file:
        df.to_csv(file, index=False)
    else:
        return

def save_csv(df):
    df.to_csv(os.path.sep.join(filter(None,[give_path(),str(df.name)+".csv"])), index=False)

def save_as_plot(plt, defaultfilename):
    try:
        plt
    except NameError:
        plt = None
    if plt is None:
        popup("No plot to save")
    file = filedialog.asksaveasfilename(defaultextension=adapt_os(linx=None, macos=None, mswin='.png'),
                                        initialdir=give_path(),
                                        filetypes=[("Portable Graphics Format (.png)", "*.png"),
                                                   ("Encapsulated Postscript (.eps)", "*.eps"),
                                                   ("Joint Photographic Group (.jpeg)", "*.jpeg"),
                                                   ("Portable Document Format (.pdf)", "*.pdf"),
                                                   ("PGF code for LaTeX (.pgf)", "*.pgf"),
                                                   ("Postscript (.ps)", "*.ps"),
                                                   ("Raw RGBA bitmap (.raw)", "*.raw"),
                                                   ("Scalable Vector Graphics (.svg)", "*.svg"),
                                                   ("Tagged Image File Format (.tif)", "*.tif"),
                                                   ("All files", "*.*")],
                                        title='Save Plot',
                                        initialfile=defaultfilename)
    if file:
        plt.savefig(file)
    else:
        return

def save_plot(plt, defaultfilename):
    plt.savefig(os.path.sep.join(filter(None, [give_path(), defaultfilename+".png"])))

def save_zip():
    if fig1 is None:
        popup("No data to save")
    desired_zip_path = filedialog.asksaveasfilename(defaultextension='.zip',
                                        initialdir=give_path(),
                                        filetypes=[(".zip  files", "*.zip"),
                                                   ("All files", "*.*")],
                                        title='Zip Files',
                                        initialfile="VISROC_"+str(time.strftime("%Y%m%d%H%M%S")))
    if desired_zip_path:
        split_directory=os.path.split((desired_zip_path))
        initial_temp_directory=split_directory[0]
        zip_name=split_directory[1]
        zip_name_without_suffix=zip_name[:len(zip_name)-4]
        temp_directory = (os.path.join(initial_temp_directory, "."+zip_name_without_suffix))
        os.makedirs(temp_directory)
        fig1.savefig(os.path.join(temp_directory, "ROC_curve_P"+str(p)+"_Q"+str(q)+".png"))
        fig2.savefig(os.path.join(temp_directory, "Plot_"+(str(h1)+"_"+str(f1)).replace('.','')+".png"))
        out_field.to_csv(os.path.join(temp_directory, "out_field.csv"), index=False)
        out_CL.to_csv(os.path.join(temp_directory, "out_CL.csv"), index=False)
        out_p.to_csv(os.path.join(temp_directory, "out_p.csv"), index=False)
        out_F1H1.to_csv(os.path.join(temp_directory, "out_F1H1.csv"), index=False)
        out_k_F1H1.to_csv(os.path.join(temp_directory, "out_k_F1H1.csv"), index=False)
        shutil.make_archive(desired_zip_path[:len(desired_zip_path)-4], 'zip', temp_directory)
        shutil.rmtree(os.path.join(initial_temp_directory, "."+zip_name_without_suffix))
    else:
        return

def open_help():
    url = 'Help.html'
    if sys.platform=="darwin" : webbrowser.get("safari").open('file://'+resource_path(url), new=2)
    else: webbrowser.open(resource_path(url), new=2)

def toggle_view(view_style):
    global act_view_style, graph1, graph2, img_graph_interpr_label_1, img_graph_interpr_label_2, situation
    act_view_style = view_style
    if situation == 0:
        pass
    else:
        calc_n_plot()

def open_about():
    global about_window
    if about_window is not None:
        about_window.destroy()
    about_window = Toplevel()
    about_window.title("About")
    about_window.geometry( adapt_os(linx="440x300", macos="480x320", mswin="440x300"))
    about_window.resizable(False, False)
    Label(about_window, text="VISROC 2.0 application", font=myFont_about_title,
          fg="#053740", justify=CENTER).grid(row=0, column=0, pady=(15, 5), sticky="WE")
    Label(about_window, text=adapt_os(
          linx="This computer program and its documentation can be found in the Computer\n"
               "Physics Communications International Program Library under the Catalog\n"
               "Identifier AERY.",
          mswin="This computer program and its documentation can be found in the Computer\n"
               "Physics Communications International Program Library under the Catalog\n"
               "Identifier AERY.",
          macos="This computer program and its documentation can be found\n"
                "in the Computer Physics Communications International Program Library\n"
                "under the Catalog Identifier AERY."),
          font=myFont_about, justify=CENTER).grid(row=1, column=0, pady=5, padx=(10, 0), sticky="WE")
    logo_image = Button(about_window, image=myImg, command = lambda:webbrowser.open_new_tab("https://doi.org/"+linkaddress),
                        highlightthickness = 0, bd = 0, cursor="hand2")
    logo_image.grid(row=2, column=0, padx=(0, 0))
    ttk.Button(about_window, text="close window", command=about_window.destroy).grid(row=4, column=0, pady=10, padx=(3, 0))

    contacts_frame = Frame(about_window, width=adapt_os(linx=260, macos=260, mswin=250), height=adapt_os(linx=65, macos=75, mswin=65))
    contacts_frame.grid(row=3, column=0, pady=0, padx=0 , sticky="WE")
    contacts_frame.columnconfigure(0, weight=1)  
    contacts_frame.grid_propagate(False)

    contacts_text = Text(contacts_frame, height=5, borderwidth=2)
    contacts_text.insert(1.0, "Contact details:"
                              "\nac0966@coventry.ac.uk,"
                              "\nstrichr@phys.uoa.gr,"
                              "\ngeorgios.tsagiannis@parisnanterre.fr")
    contacts_text.tag_configure("center", justify='center')
    contacts_text.tag_add("center", 1.0, END)
    contacts_text.config(font=myFont_about)
    contacts_text.configure(state="disabled")
    contacts_text.configure(bg=contacts_frame.cget('bg'), relief="flat")
    contacts_text.configure(state="disabled")
    contacts_text.grid(sticky="we")

    about_window.bind("<Button-3>", prepare_popup)
    about_window.bind('<Return>', close_about_window)
    about_window.bind('<Escape>', close_about_window)

def cut_text(e):
    global copied, clickedWidget
    copied = clickedWidget.selection_get()
    clickedWidget.delete("sel.first", "sel.last")
    root.clipboard_append(selected)

def copy_text(e):
    global copied, clickedWidget
    copied = clickedWidget.selection_get()
    root.clipboard_append(copied)

def paste_text(e):
    global clickedWidget, copied
    position =clickedWidget.index(INSERT)
    try: clickedWidget.delete("sel.first", "sel.last")
    except TclError: pass
    clickedWidget.insert(position, copied)

def clear_text(e):
    clickedWidget.delete("sel.first", "sel.last")

def prepare_popup(event):
    global clickedWidget, copied, right_click_menu
    clickedWidget = event.widget 
    try:
        isinstance(clickedWidget.selection_get(), str)
        right_click_menu.entryconfig("Cut", state="normal")
        right_click_menu.entryconfig("Copy", state="normal")
        right_click_menu.entryconfig("Clear", state="normal")
    except TclError or _tkinter.TclError:
        right_click_menu.entryconfig("Cut", state="disabled")
        right_click_menu.entryconfig("Copy", state="disabled")
        right_click_menu.entryconfig("Clear", state="disabled")
    if copied:
        right_click_menu.entryconfig("Paste", state="normal")
    else: right_click_menu.entryconfig("Paste", state="disabled")
    do_popup(event)

def do_popup(event):
    try:
        right_click_menu.tk_popup(event.x_root, event.y_root)
    finally:
        right_click_menu.grab_release()

def popupFocusOut(self, event=None):
        right_click_menu.unpost()

def close_about_window(event):
    about_window.destroy()

def open_close_graph_interpretation():
    global graph_interpr_window
    if graph_interpr_window is not None:
        graph_interpr_window.destroy()
    graph_interpr_window = Toplevel()
    graph_interpr_window.title("Graph Interpretation")
    graph_interpr_window.geometry("697x746")
    graph_interpr_window.resizable(False, False)
    Label(graph_interpr_window, image=img_graph_interpr).place(x = 0, rely=0)
    ttk.Button(graph_interpr_window, text="close window", command=graph_interpr_window.destroy).place(relx=0.44, rely=0.95)

def popup(text):
    messagebox.showinfo("Help", text)

def import_csv_data():
    global v, file_entry, inFile, sv_infile, inFile_temp
    csv_file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("CSV (Comma delimited) files (.csv)", "*.csv"), ("All files", "*.*")))
    v.set(csv_file_path)
    file_entry.delete(0,END)
    file_entry.insert(0, v.get())
    inFile_temp=csv_file_path
    sv_infile.set(str(inFile_temp))

def import_csv_data_manualy(event):
    global inFile_temp, sv_infile
    inFile_temp=file_entry.get().strip()
    sv_infile.set(str(inFile_temp))

def delete_entered_file_fun():
    global entered_file, delete_entered_file
    entered_file.destroy()
    delete_entered_file.destroy()
    entered_file = Label(master=file_entered, text="",
                         font=adapt_os(linx="Arial 8", macos=(default_font_family, "14"), mswin="Arial 8"))
    delete_entered_file = Button(master=file_entered, text="x", relief=FLAT)

def callback():
    global Plot_button, p, q, N, f1, h1, uauc, ROCti
    global uauc_entry, N_entry, f1_entry, h1_entry, inFile, sv_infile, inFile_temp
    try:
        if ((float(sv_positives.get()) == p or p == None) and
        (float(sv_negatives.get()) == q or q == None) and
        (int(iv_slider.get()) == N_entry or N == None) and
        (float(sv_f1.get()) == f1_entry or f1 == None) and
        (float(sv_h1.get()) == h1_entry or h1 == None) and
        (float(sv_uauc.get()) == uauc_entry or uauc == None) and
        (sv_title.get().strip() == ROCti or ROCti == None) and
        (str(sv_infile.get().strip()) == str(inFile) or inFile == None or sv_infile.get().strip() == "")) :
            Plot_button.config(text="Plot", fg= "white")
        else:
            Plot_button.config(text="Update Plot", fg=adapt_os(linx="red", macos="pink", mswin="red"))
    except ValueError:
        pass

def assign(event):
    global entered_file, delete_entered_file, file_entry, v
    global p, q, N, uauc, f1, h1, ROCti, ROCti_print, inFile, raw_data
    global uauc_entry, f1_entry, h1_entry, N_entry, f1_crit_fault, h1_crit_fault
    global p_old, q_old, f1_old, h1_old, uauc_old, ROCti_old, N_old, raw_data_old
    global input_error_message, error_num, ifault

    try:
        del data
    except NameError:
        pass

    input_error_message = [[], []]
    error_num = 0
    ifault = 0

    p_entry = sv_positives.get()
    try:
        p = float(p_entry)
        if p % 1 != 0 or p < 1:
            Positives_entry['bg'] = "pink"
            input_error_message[0].append("P must be positive integer")
            ifault = 2
        else:
            Positives_entry['bg'] = "white"
        p = int(p)
    except ValueError or TypeError:
        Positives_entry['bg'] = "pink"
        input_error_message[0].append("P must be positive integer")
        ifault = 2

    q_entry = sv_negatives.get()
    try:
        q = float(q_entry)
        if q % 1 != 0 or q < 1:
            Negatives_entry['bg'] = "pink"
            input_error_message[0].append("Q must be positive integer")
            ifault = 2
        else:
            Negatives_entry['bg'] = "white"
        q = int(q)
    except ValueError or TypeError:
        Negatives_entry['bg'] = "pink"
        input_error_message[0].append("Q must be positive integer")
        ifault = 2

    N_entry = int(Resolution_Slider.get())
    if N_entry == 0:
        Resolution_Slider.configure(highlightbackground="crimson")
        input_error_message[0].append("Resolution must be greater than 0")
        ifault = 2
    else:
        N = N_entry
        Resolution_Slider.configure(highlightbackground=output_screen.cget("background"))

    uauc_entry = sv_uauc.get()
    try:
        uauc_entry = round(float(uauc_entry), 4)
        uauc = round(float(uauc_entry), 4)
        sv_uauc.set(uauc)
        if uauc <= 0:
            AUC_entry['bg'] = "pink"
            AUC_entry['fg'] = adapt_os(linx="black", macos=default_foreground_color, mswin="black")
            input_error_message[0].append(
                "User-defined AUC must have a numerical value in the closed interval [0.5, 1]")
            ifault = 2
        elif uauc < .5 and uauc > 0:
            AUC_entry['bg'] = "white"
            AUC_entry['fg'] = "crimson"
            input_error_message[1].append(
                "User-defined AUC must have a numerical value in the closed interval [0.5, 1] (else: use of default value)")
            ifault = max(ifault, 1)
            uauc = .51
        elif uauc > 1:
            AUC_entry['bg'] = "pink"
            AUC_entry['fg'] = adapt_os(linx="black", macos=default_foreground_color, mswin="black")
            input_error_message[0].append(
                "User-defined AUC must have a numerical value in the closed interval [0.5, 1]")
            ifault = 2
        else:
            AUC_entry['bg'] = "white"
            AUC_entry['fg'] = adapt_os(linx="black", macos=default_foreground_color, mswin="black")
    except ValueError or TypeError:
        AUC_entry['bg'] = "pink"
        input_error_message[0].append("User-defined AUC must have a numerical value in the closed interval [0.5, 1]")
        ifault = 2

    f1_entry = sv_f1.get()
    try:
        f1_entry = round(float(f1_entry), 4)
        f1 = round(float(f1_entry), 4)
        sv_f1.set(f1)
        if f1 < 0 or f1 > 1:
            f1_crit_fault = 1
            F1_entry['bg'] = "white"
            F1_entry['fg'] = "crimson"
            input_error_message[1].append(
                "F\u2081 must have a numerical value in the closed interval [0, 1] (else: use of default value)")
            f1 = 0.65
            ifault = max(ifault, 1)
        else:
            f1_crit_fault = 0
            F1_entry['bg'] = "white"
    except ValueError:
        F1_entry['bg'] = "pink"
        input_error_message[0].append("F\u2081 must have a numerical value in the closed interval [0, 1]")
        ifault = 2

    h1_entry = sv_h1.get()
    try:
        h1_entry = round(float(h1_entry), 4)
        h1 = round(float(h1_entry), 4)
        sv_h1.set(h1)
        if h1 < 0 or h1 > 1:
            h1_crit_fault = 1
            H1_entry['bg'] = "white"
            H1_entry['fg'] = "crimson"
            input_error_message[1].append(
                "H\u2081 must have a numerical value in the closed interval [0, 1] (else: use of default value)")
            h1 = 0.75
            ifault = max(ifault, 1)
        else:
            h1_crit_fault = 0
            H1_entry['bg'] = "white"
    except ValueError:
        H1_entry['bg'] = "pink"
        input_error_message[0].append("H\u2081 must have a numerical value in the closed interval [0, 1]")
        ifault = 2

    ROCti = sv_title.get().strip()
    ROCti_print = sv_title.get().strip() if ROCti != "" else " "

    try:
        if f1 > h1:
            mauc = h1
            h1 = f1
            F1_entry['fg'] = "crimson"
            H1_entry['fg'] = "crimson"
            f1 = mauc
            input_error_message[1].append("Value H1 must be greater than value F1 (else: input values inversion)")
            ifault = max(ifault, 1)
        else:
            if f1_crit_fault == 0:
                F1_entry['fg'] = adapt_os(linx="black", macos=default_foreground_color, mswin="black")
            else:
                F1_entry['fg'] = "crimson"
            if h1_crit_fault == 0:
                H1_entry['fg'] = adapt_os(linx="black", macos=default_foreground_color, mswin="black")
            else:
                H1_entry['fg'] = "crimson"
    except TypeError:
        ifault = 2

    if file_entry.get().strip() != "":
        entered_file.destroy()
        entered_file.update()
        delete_entered_file.destroy()
        entered_file = Label(master=file_entered, text=os.path.split(file_entry.get())[1],
                             font=adapt_os(linx="Arial 8", macos=(default_font_family, "14"), mswin="Arial 8"))
        entered_file.place(x=0)
        delete_entered_file = Button(master=file_entered, text="x", command=delete_entered_file_fun,
                                     font=adapt_os(linx="Arial 9 bold", macos=(default_font_family, "15", "bold"), mswin="Arial 9 bold"),
                                     fg='red', bd=adapt_os(linx=1, macos=0, mswin=1), relief=FLAT,
                                     activeforeground=adapt_os(linx='dark red', macos='dark red'),
                                     padx=1, pady=0)
        if sys.platform=="darwin":
            entered_file.place(x=0, y=-5)
            delete_entered_file.place(x=130, y=-7)
        else:
            entered_file.place(x=0)
            delete_entered_file.place(relx=0.94, y=-2)
        inFile = file_entry.get()
        file_entry.delete(0, END)
    else:
        try:
            if entered_file['text'] != "":
                pass
            else:
                entered_file.destroy()
                delete_entered_file.destroy()
                inFile = None
        except TclError:
            pass

    if inFile is None:
        file_entry['fg'] = adapt_os(linx="black", macos=default_foreground_color, mswin="black")
        raw_data = None
        pass
    else:
        try:
            with open(inFile) as f:
                first = f.read(1)
                header = 0 if first not in '.-0123456789' else None
                raw_data = pd.read_csv(inFile, sep='[,;\s]+', header=header, engine='python')
        except (FileNotFoundError, OSError):
            entered_file['fg'] = "red"
            input_error_message[1].append(
                "Filepath does not correspond to file (else: calculate and plot without user's ROC data input)")
            ifault = max(ifault, 1)
            raw_data = "ErrorData"
        except (UnicodeDecodeError, pd.errors.ParserError):
            entered_file['fg'] = "red"
            input_error_message[1].append(
                "File format is not supported (else: calculate and plot without user's ROC data input)")
            ifault = max(ifault, 1)
            raw_data = "ErrorData"
        try:
            raw_data.columns = ['x', 'y']
        except ValueError:
            entered_file['fg'] = "red"
            input_error_message[1].append(
                "Data dimensions are not correct (input data must have 2 cols, "
                "else: calculate and plot without user's ROC data input)")
            ifault = max(ifault, 1)
            raw_data = "ErrorData"
        except AttributeError:
            pass

    Plot_button.config(text="Plot", fg="white")

    input_validity_control()

    filemenu.entryconfig("Save as...", state="normal")
    filemenu.entryconfig("Save", state="normal")
    filemenu.entryconfig("Save all (.zip)", state="normal")
    Save_button.menu.entryconfig("Save as...", state="normal")
    Save_button.menu.entryconfig("Save", state="normal")
    Save_button.menu.entryconfig("Save all (.zip)", state="normal")

def input_validity_control():
    global p, q, N_entry, uauc, f1, h1, ROCti, raw_data
    global p_old, q_old, N_old, uauc_old, f1_old, h1_old, ROCti_old, raw_data_old
    global ifault, input_error_message, Error_Info_Button_border, text_error_message

    if len(input_error_message[0]) != 0:
        critical_errors_text = ""
        for i in input_error_message[0]:
            critical_errors_text += "\n - " + str(i)
        critical_errors_text = "Critical Errors (" + str(len(input_error_message[0])) + "x):" + critical_errors_text
    if len(input_error_message[1]) != 0:
        non_critical_errors_text = ""
        for i in input_error_message[1]:
            non_critical_errors_text += "\n - " + str(i)
        non_critical_errors_text = "Non Critical Errors (" + str(
            len(input_error_message[1])) + "x):" + non_critical_errors_text
    text_error_message = []
    if 'critical_errors_text' in locals():
        text_error_message.append(critical_errors_text)
    if 'non_critical_errors_text' in locals():
        text_error_message.append(non_critical_errors_text)
    text_error_message = '\n\n'.join(text_error_message)

    if ifault == 0:
        Error_Info_Button_border.destroy()
        Error_Info_Button_border = Frame(Results_pad, highlightthickness=1, bd=0, padx=0, pady=0)
        Error_Info_Button_border.place(rely=adapt_os(mswin=0.873, linx=0.883, macos=0.88), x=adapt_os(linx=-2, macos=-5, mswin=-2))
        Error_Info_Button = Button(Error_Info_Button_border, text="No fault", anchor="nw", relief=FLAT,
                                   height=2, width=adapt_os(linx=31, macos=27, mswin=31), bd=1,
                                   font=adapt_os(linx="Arial 12", macos=(default_font_family, "14"), mswin="Arial 12"), cursor="arrow", state=DISABLED,
                                   disabledforeground="#053740", padx=adapt_os(linx=0, macos=1, mswin=0))
    elif ifault == 1:
        Error_Info_Button_border.destroy()
        Error_Info_Button_border = Frame(Results_pad, highlightthickness=1, highlightbackground="crimson", bd=0, padx=0,
                                         pady=0)
        Error_Info_Button_border.place(rely=adapt_os(mswin=0.87, linx=0.88, macos=0.88), x=adapt_os(linx=-1, macos=-5, mswin=-1))
        Error_Info_Button = Button(Error_Info_Button_border,
                                   text=adapt_os(linx="fault 1:    Illegal input values. Altered values \n"
                                                      "     used, as described in the \"Help\" section",
                                                 macos="fault 1: Illegal input values. Altered values \n"
                                                       "used, as described in the \"Help\" section",
                                                 mswin="fault 1: Illegal input values. Altered values\n"
                                                       " used, as described in the \"Help\" section"), anchor="ne",
                                   foreground="crimson",
                                   height=2, width=adapt_os(linx=35, macos=27, mswin=31), bd=2,
                                   font=adapt_os(linx="Arial 11", macos=(default_font_family, "14"), mswin="Arial 12"), cursor="hand2", pady=0,
                                   disabledforeground="crimson", padx=adapt_os(linx=0, macos=1, mswin=0),
                                   activebackground=adapt_os(linx='grey90'),
                                   activeforeground=adapt_os(linx="crimson", macos="crimson"),
                                   command=lambda: messagebox.showerror("Input Error", text_error_message))
    else:
        messagebox.showerror("Input Error", text_error_message)
        Error_Info_Button_border.destroy()
        Error_Info_Button_border = Frame(Results_pad, highlightthickness=1, highlightbackground="crimson", bd=0,
                                         padx=0, pady=0)
        Error_Info_Button_border.place(rely=adapt_os(mswin=0.865, linx=0.88, macos=0.88), x=adapt_os(linx=-1, macos=-5, mswin=-1))
        Error_Info_Button = Button(Error_Info_Button_border,
                                   text=adapt_os(linx=" fault 2:       Illegal input values. Calculations \n"
                                                      "                         and plotting are not possible ",
                                                 macos="fault 2: Illegal input values.                        \n"
                                                       "Calculations and plotting are not possible",
                                                 mswin="fault 2:   Illegal input values. Calculations\n "
                                                       "                   and plotting are not possible"), anchor="ne",
                                   foreground="crimson",
                                   height=2, width=adapt_os(linx=35, macos=27, mswin=31), bd=2,
                                   font=adapt_os(linx="Arial 11", macos=(default_font_family, "14"), mswin="Arial 12"), cursor="hand2", pady=0,
                                   disabledforeground="crimson", padx=adapt_os(linx=0, macos=1, mswin=0),
                                   activebackground=adapt_os(linx='grey90'),
                                   activeforeground=adapt_os(linx="crimson", macos="crimson"),
                                   command=lambda: messagebox.showerror("Input Error", text_error_message))

    try:
        if [p, q, N_entry, uauc, f1, h1, ROCti, str(raw_data)] == [p_old, q_old, N_old, uauc_old, f1_old, h1_old,
                                                                   ROCti_old, str(raw_data_old)] or ifault==2:
            pass
        else:
            calc_n_plot()
    except NameError:
        calc_n_plot()

    Error_Info_Button.pack()

def calc_n_plot():
    global entered_file, delete_entered_file, file_entry, v
    global p, q, N, uauc, f1, h1, ROCti, ROCti_print, raw_data
    global graph_screen, graph1, graph2, fig1, fig2, canvas1, canvas2, ax1, ax2
    global p_old, q_old, f1_old, h1_old, uauc_old, ROCti_old, N_old, raw_data_old
    global out_field, out_CL, out_p, out_F1H1, out_k_F1H1
    global s, valy, valys, valy_file, PVAUC_file, area
    global ifault, text_error_message
    global situation, act_view_style

    freq = [1 for i in range(0, 900)]
    work = [1 for i in range(0, 900)]
    pdf = [0 for i in range(0, 900)]
    auc1 = [0 for i in range(0, 900)]
    cdf = [0 for i in range(0, 900)]
    auccr = [0 for i in range(0, 4)]
    val = [0 for i in range(0, 4)]
    kcr = [0 for i in range(0, 4)]

    case = 1 if (max(p, q) >= 30) & (p + q >= 40) else 0

    # Calculate the steps of the process so as to initialise progressbar
    steps_calc = 3 * (N + 1) * (N + 1) + 2002
    progress_bar = ttk.Progressbar(status, length=adapt_os(linx=1015, macos=1015, mswin=1013), mode="determinate",
                                   maximum=steps_calc, value=0)
    progress_bar.grid(row=0, column=0, padx=(3, 0), sticky="S")

    if (case == 0):
        # -----Use of AS62 to estimate the distribution of AUC"
        piqo = min(p, q)
        pq1 = p * q + 1
        paxo = max(p, q)
        q1 = paxo + 1
        for i in range(1, q1 + 1):
            freq[i] = 1
        q1 += 1
        for i in range(q1, pq1 + 1):
            freq[i] = 0
        work[1] = 0
        iq = paxo
        for i in range(2, piqo + 1):
            work[i] = 0
            iq += paxo
            q1 = iq + 2
            l = int(1 + iq / 2)
            w = i
            for j in range(1, l + 1):
                w += 1
                q1 -= 1
                sumAS62 = freq[j] + work[j]
                freq[j] = sumAS62
                work[w] = sumAS62 - freq[q1]
                freq[q1] = sumAS62
        sumAS62 = 0
        for i in range(1, p * q + 1 + 1):
            sumAS62 += freq[i]
            auc1[i] = 1.0 - (i - 1) / (p * q)
        cdf[1] = 1.0
        for i in range(1, p * q + 1 + 1):
            pdf[i] = freq[i] / sumAS62
            auc1[i] = 1.0 - (i - 1) / (p * q)
            cdf[i + 1] = cdf[i] - pdf[i]
            if cdf[i] >= 0.90: auccr[1] = auc1[i]
            if cdf[i] >= 0.95: auccr[2] = auc1[i]
            if cdf[i] >= 0.99: auccr[3] = auc1[i]

    if case == 1:
        # -----Use of Gaussian approximation
        s = sqrt(1.0 / q + 1.0 / p + 1.0 / (p * q)) / sqrt(12.0)
        auccr[1] = 0.50 + 1.2816 * s
        auccr[2] = 0.50 + 1.6449 * s
        auccr[3] = min(0.50 + 2.3264 * s, 0.99999999999999)

    # -----Calculate k-values for three AUC confidence levels
    for l in range(1, 3 + 1):
        y0 = auccr[l]
        know = 0.0
        flag1 = 0
        while flag1 == 0:
            k = know
            x1 = 0.5 + (p * q - k * sqrt(q * (k + q + p))) / (2.0 * q * (p + k))

            r = sqrt(k + 4 * q * (x1 - x1 * x1))
            r0 = sqrt(k)
            auc = 1 - x1 / 2 + (q / (q + k)) * (x1 - 1) * x1 / 2 + \
                  sqrt(k * (k + q + p) / p) / (2 * (k + q)) * \
                  ((k + q) * np.arctan(sqrt(q) * np.float64(2 * x1 - 1) / r) / (4 * sqrt(q)) +
                   (2 * x1 - 1) * r / 4 + (k + q) * np.arctan(np.float64(sqrt(q)) / r0) / (4 * sqrt(q)) + r0 / 4)
            kold = know
            x1old = x1
            aucold = auc
            k = kold + 0.001
            x1 = 0.5 + (p * q - k * sqrt(q * (k + q + p))) / (2.0 * q * (p + k))
            r = sqrt(k + 4 * q * (x1 - x1 * x1))
            r0 = sqrt(k)
            auc = 1 - x1 / 2 + (q / (q + k)) * (x1 - 1) * x1 / 2 + \
                  sqrt(k * (k + q + p) / p) / (2 * (k + q)) * \
                  ((k + q) * np.arctan(sqrt(q) * np.float64(2 * x1 - 1) / r) / (4 * sqrt(q)) +
                   (2 * x1 - 1) * r / 4 + (k + q) * np.arctan(np.float64(sqrt(q)) / r0) / (4 * sqrt(q)) + r0 / 4)
            dauc = (auc - aucold) / 0.001
            know = kold - (aucold - y0) / dauc
            if abs(know - kold) < 0.001 * kold: flag1 = 1
        kcr[l] = know

    out_CL = []
    for ix in range(0, 1000 + 1):
        x = ix / 1000.0
        for l in range(1, 3 + 1):
            k = kcr[l]
            valy = 0.5 + q / (q + k) * (x - 0.5) + 0.5 / (k + q) * sqrt(
                k * (k + q + p) * (k + 4.0 * q * (x - x * x)) / p)
            val[l] = valy
        out_CL.append(
            {
                'x1': x,
                'y1': val[1],
                'y2': val[2],
                'y3': val[3],
            }
        )
        progress_bar['value'] += 1
        root.update_idletasks()

    out_CL = pd.DataFrame(out_CL)
    out_CL.name = "out_CL"

    # -----Calculation of the p field on the ROC diagram"]
    x = 0
    y = 0
    out_field = []
    for ix in range(0, N + 1):
        for iy in range(0, N + 1):
            x = ix / N
            y = iy / N
            xv = x - 0.5
            yv = y - 0.5
            k = 2 * (p * yv ** 2 + q * xv ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * yv ** 2 + q * xv ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (xv - yv) ** 2)
            x1 = 0.5 + (p * q - k * sqrt(q * (k + q + p))) / (2.0 * q * (p + k))
            r = sqrt(k + 4 * q * (x1 - x1 * x1))
            r0 = sqrt(k)
            auc = 1 - x1 / 2 + (q / (q + k)) * (x1 - 1) * x1 / 2 + sqrt(k * (k + q + p) / p) / (2 * (k + q)) * (
                    (k + q) * np.arctan(sqrt(q) * np.float64(2 * x1 - 1) / r) / (4 * sqrt(q)) + (
                    2 * x1 - 1) * r / 4 + (k + q) * np.arctan(np.float64(sqrt(q)) / r0) / (
                            4 * sqrt(q)) + r0 / 4)
            if case == 1: valy = (erf(float((auc - 0.5) / sqrt(2) / s)) + 1) / 2
            if case == 0:
                valy = cdf[1]
                for i in range(2, p * q + 1 + 1):
                    if auc1[i] >= auc: valy = cdf[i]
            valys = 1 - valy
            out_field.append(
                {
                    'x': x,
                    'y': y,
                    'z': valys
                }
            )
        progress_bar['value'] += N + 1
        root.update_idletasks()

    out_field = pd.DataFrame(out_field)
    out_field.name = 'out_field'

    # -----Calculation of the p value for the user defined uauc"
    auc = uauc
    if case == 1:
        valy = (erf((auc - 0.5) / sqrt(2) / s) + 1) / 2
    if case == 0:
        valy = cdf[1]
        for i in range(2, p * q + 1 + 1):
            if auc1[i] >= auc: valy = cdf[i]
    valys = 1 - valy
    out_p = pd.DataFrame([[valys, uauc, p, q, ifault]], columns=['p_Value', 'UserDefAUC', 'p', 'q', 'ifault'])
    out_p.name = "out_p"

    # -----Calculations based on the k-ellipse passing through h1,f1
    x = f1
    y = h1
    xv = x - 0.5
    yv = y - 0.5
    k = 2 * (p * yv ** 2 + q * xv ** 2) - 0.5 * (p + q) + sqrt(
        (2 * (p * yv ** 2 + q * xv ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (xv - yv) ** 2)
    x1 = 0.5 + (p * q - k * sqrt(q * (k + q + p))) / (2.0 * q * (p + k))
    r = sqrt(k + 4 * q * (x1 - x1 * x1))
    r0 = sqrt(k)
    auc = 1 - x1 / 2 + (q / (q + k)) * (x1 - 1) * x1 / 2 + \
          sqrt(k * (k + q + p) / p) / (2 * (k + q)) * \
          ((k + q) * np.arctan(sqrt(q) * np.float64(2 * x1 - 1) / r) / (4 * sqrt(q)) + (2 * x1 - 1) * r / 4 +
           (k + q) * np.arctan(np.float64(sqrt(q)) / r0) / (4 * sqrt(q)) + r0 / 4)
    mauc = auc
    auc = mauc
    if case == 1: valy = (erf(float((auc - 0.5) / sqrt(2) / s)) + 1) / 2
    if case == 0:
        valy = cdf[1]
        for i in range(2, p * q + 1 + 1):
            if auc1[i] >= auc: valy = cdf[i]
    mval = valy
    mvals = 1.0 - mval

    out_F1H1 = pd.DataFrame([[mvals, f1, h1, ifault, p, q, mauc]],
                            columns=['p_Value', 'F1', 'H1', 'ifault', 'p', 'q', 'AUC'])
    out_F1H1.name = "out_F1H1"

    out_k_F1H1 = []
    for ix in range(1001):
        xk = ix / 1000
        valyF1H1 = 0.5 + q / (q + k) * (xk - 0.5) + 0.5 / (k + q) * sqrt(
            k * (k + q + p) * (k + 4.0 * q * (xk - xk * xk)) / p)
        out_k_F1H1.append(
            {
                'x': xk,
                'y': valyF1H1,
                'k': k
            }
        )
        progress_bar['value'] += 1
        root.update_idletasks()
    out_k_F1H1 = pd.DataFrame(out_k_F1H1)
    out_k_F1H1.name = "out_k_F1H1"

    if str(raw_data) != "None" and str(raw_data) != "ErrorData":
        zero0 = pd.DataFrame({'x': 0, 'y': 0}, index=[0])
        data = pd.concat([zero0, raw_data]).reset_index(drop=True)
        area = 0
        xold_area = 0
        yold_area = 0
        Area_input = data
        Area_input.loc[len(Area_input)] = [1, 1]
        nlines = len(Area_input)
        for line in range(nlines):
            x_area = Area_input.loc[line][0]
            y_area = Area_input.loc[line][1]
            area = area + (y_area + yold_area) * (x_area - xold_area) / 2
            xold_area = x_area
            yold_area = y_area

            auc_file = area
            if case == 1: valy_file = (erf((auc_file - 0.5) / sqrt(2) / s) + 1) / 2
            if case == 0:
                valy_file = cdf[0]
                for i in range(1, (p * q + 1)):
                    if auc1[i] >= auc_file:
                        valy_file = cdf[i]
        PVAUC_file = 1 - valy_file

    graph1.destroy()
    graph2.destroy()
    graph1 = Frame(graph_screen, width=696, height=712, relief=SUNKEN, bd=4)
    graph1.config(background='white')
    graph2 = Frame(graph_screen, width=696, height=712, relief=SUNKEN, bd=4)
    graph2.config(background='white')
    graph1.pack(fill="both", expand=1)
    graph2.pack(fill="both", expand=1)
    graph_screen.add(graph1, text="ROC curve")
    graph_screen.add(graph2, text="Plot (F\u2081, H\u2081)")

    fig1 = Figure(figsize=(6, 6), dpi=100, constrained_layout=True)

    ax1 = fig1.add_subplot(111)
    ax1.margins(x=0, y=0)
    ax1.set_ylim([0, 1])
    ax1.set_yticks(np.linspace(0, 1, 9), minor=True)
    ax1.set_yticks(np.linspace(0, 1, 5))
    ax1.set_xlim([0, 1])
    ax1.set_xticks(np.linspace(0, 1, 9), minor=True)
    ax1.set_xticks(np.linspace(0.25, 1, 4))
    ax1.grid(which='major', linestyle='-', color="grey", linewidth=0.5)
    ax1.grid(which='minor', linestyle='-', color="lightgrey", linewidth=0.5)
    ax1.spines['left'].set_linestyle('-')
    ax1.spines['left'].set_linewidth(0.2)
    ax1.spines['right'].set_linestyle('-')
    ax1.spines['right'].set_linewidth(0.4)
    ax1.spines['bottom'].set_linestyle('-')
    ax1.spines['bottom'].set_linewidth(0.4)
    ax1.spines['top'].set_linestyle('-')
    ax1.spines['top'].set_linewidth(0.2)
    ax1.set_title(ROCti_print, pad=15, fontsize=16)
    if act_view_style == "earth":
        ax1.set_ylabel('Hit Rate', fontsize=12, labelpad=10)
        ax1.set_xlabel('False Alarm Rate', fontsize=12, labelpad=15)
    elif act_view_style == "math":
        ax1.set_ylabel('True Positive Rate (TPR)', fontsize=12, labelpad=10)
        ax1.set_xlabel('False Positive Rate (FPR)', fontsize=12, labelpad=15)
    else:
        ax1.set_ylabel('Sensitivity', fontsize=12, labelpad=10)
        ax1.set_xlabel('1 - Specificity (False Positive Rate)', fontsize=12, labelpad=15)

    colors = ["white", "#00CC00", "#0080FF"]
    norm = matplotlib.colors.Normalize(vmin=0, vmax=.5)
    cmapu = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    ax1.scatter(out_field.x, out_field.y, c=out_field.z, vmin=0, vmax=.5, s=(356.5 / N) ** 2, marker="s", cmap=cmapu)
    cbaxes1 = fig1.add_axes([0.833, 0.465, 0.03, 0.3])
    clb1 = fig1.colorbar(matplotlib.cm.ScalarMappable(cmap=cmapu.reversed(), norm=norm), shrink=.35, aspect=10,
                         cax=cbaxes1)
    clb1.set_label('p-value', labelpad=10, y=1.15, rotation=0, fontsize=12)

    ax1.tick_params(colors='grey', direction="in", which="both")

    clb1.set_ticks(list())
    for index, label in enumerate(reversed(["- 0%", "- 10%", "- 20%", "- 30%", "- 40%", "- 50%"])):
        if version.parse(matplotlib.__version__) >= version.parse("3.5"):
            x = 1
            y = index / 10.55
        else:
            x = 0.5
            y = index / 10.45
        clb1.ax.text(x, y, label)

    ax1.plot(out_CL.x1, out_CL.y3, color="red", linewidth=.7, label='1%')
    ax1.plot(out_CL.x1, out_CL.y2, color="green", linewidth=.7, label='5%')
    ax1.plot(out_CL.x1, out_CL.y1, color="blue", linewidth=.7, label='10%        ')

    if str(raw_data) != "None" and str(raw_data) != "ErrorData":
        data.columns = ['x', 'y']
        if data.loc[0][0] != 0 or data.loc[0][1] != 0:
            zero0 = pd.DataFrame({'x': 0, 'y': 0}, index=[0])
            data = pd.concat([zero0, raw_data]).reset_index(drop=True)
        if data.loc[len(data) - 1][0] != 1 or data.loc[len(data) - 1][1] != 1:
            data.loc[len(data)] = [1, 1]
        ax1.plot(data.x, data.y, 'o', color="purple", linestyle="-", linewidth=1, markersize=4, label='Data')

    legend1 = ax1.legend(title='k-ellipses', bbox_to_anchor=(1.02, 0.41), loc='upper left', borderaxespad=0,
                         title_fontsize=12, labelspacing=1, markerscale=1.5, frameon=False)
    legend1._legend_box.align = "left"
    for line in legend1.get_lines():
        line.set_linewidth(2.0)

    fig2 = Figure(figsize=(6, 6), dpi=100, constrained_layout=True)

    ax2 = fig2.add_subplot(111)
    ax2.margins(x=0, y=0)
    ax2.set_ylim([0, 1])
    ax2.set_yticks(np.linspace(0, 1, 9), minor=True)
    ax2.set_yticks(np.linspace(0, 1, 5))
    ax2.set_xlim([0, 1])
    ax2.set_xticks(np.linspace(0, 1, 9), minor=True)
    ax2.set_xticks(np.linspace(0.25, 1, 4))
    ax2.grid(which='major', linestyle='-', color="grey", linewidth=0.5)
    ax2.grid(which='minor', linestyle='-', color="lightgrey", linewidth=0.5)
    ax2.spines['left'].set_linestyle('-')
    ax2.spines['left'].set_linewidth(0.2)
    ax2.spines['right'].set_linestyle('-')
    ax2.spines['right'].set_linewidth(0.4)
    ax2.spines['bottom'].set_linestyle('-')
    ax2.spines['bottom'].set_linewidth(0.4)
    ax2.spines['top'].set_linestyle('-')
    ax2.spines['top'].set_linewidth(0.2)
    ax2.set_title(ROCti_print, pad=15, fontsize=16)
    if act_view_style == "earth":
        ax2.set_ylabel('Hit Rate', fontsize=12, labelpad=10)
        ax2.set_xlabel('False Alarm Rate', fontsize=12, labelpad=15)
    elif act_view_style == "math":
        ax2.set_ylabel('True Positive Rate (TPR)', fontsize=12, labelpad=10)
        ax2.set_xlabel('False Positive Rate (FPR)', fontsize=12, labelpad=15)
    else:
        ax2.set_ylabel('Sensitivity', fontsize=12, labelpad=10)
        ax2.set_xlabel('1 - Specificity', fontsize=12, labelpad=15)

    colors = ["white", "#00CC00", "#0080FF"]
    norm = matplotlib.colors.Normalize(vmin=0, vmax=.5)
    cmapu = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    ax2.scatter(out_field.x, out_field.y, c=out_field.z, vmin=0, vmax=.5, s=(356.5 / N) ** 2, marker="s", cmap=cmapu)
    cbaxes2 = fig2.add_axes([0.833, 0.465, 0.03, 0.3])
    clb2 = fig2.colorbar(matplotlib.cm.ScalarMappable(cmap=cmapu.reversed(), norm=norm), shrink=.35, aspect=10,
                         cax=cbaxes2)
    clb2.set_label('p-value', labelpad=10, y=1.15, rotation=0, fontsize=12)

    ax2.tick_params(colors='grey', direction="in", which="both")

    clb2.set_ticks(list())
    for index, label in enumerate(reversed(["- 0%", "- 10%", "- 20%", "- 30%", "- 40%", "- 50%"])):
        if version.parse(matplotlib.__version__) >= version.parse("3.5"):
            x = 1
            y = index / 10.55
        else:
            x = 0.5
            y = index / 10.45
        clb2.ax.text(x, y, label)

    ax2.plot(out_CL.x1, out_CL.y3, color="red", linewidth=.7, label='1%')
    ax2.plot(out_CL.x1, out_CL.y2, color="green", linewidth=.7, label='5%')
    ax2.plot(out_CL.x1, out_CL.y1, color="blue", linewidth=.7, label='10%        ')

    ax2.plot(out_k_F1H1.x, out_k_F1H1.y, color="purple", linestyle="--", linewidth=.7, label='k-(F\u2081, H\u2081)')
    ax2.plot(f1, h1, 'o', color="purple", markersize=4, label='(F\u2081, H\u2081)')

    legend2 = ax2.legend(title='k-ellipses', bbox_to_anchor=(1.02, 0.41), loc='upper left', borderaxespad=0,
                         title_fontsize=12, labelspacing=1, markerscale=1.5, frameon=False)
    legend2._legend_box.align = "left"
    for line in legend2.get_lines():
        line.set_linewidth(2.0)

    canvas1 = FigureCanvasTkAgg(fig1, graph1)
    canvas1.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    canvas1.draw()
    for i in range(0, N + 1):
        progress_bar['value'] += N + 1
        root.update_idletasks()

    graph_screen.select(1)

    canvas2 = FigureCanvasTkAgg(fig2, graph2)
    canvas2.get_tk_widget().pack(side=TOP, fill=X, expand=1)
    canvas2.draw()
    progress_bar['value'] += (N + 1) * (N + 1)

    toolbar_items = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to  previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
    )

    backend_bases.NavigationToolbar2.toolitems = toolbar_items
    toolbar1 = NavigationToolbar2Tk(canvas1, graph1)
    toolbar1.winfo_children()[-1].config(font=adapt_os(linx=(default_font_family, "9")))
    toolbar1.update()
    canvas1.get_tk_widget().pack(side=TOP, fill=X, expand=1)

    toolbar2 = NavigationToolbar2Tk(canvas2, graph2)
    #toolbar2.config(background=adapt_os(linx='light grey'))
    #toolbar2._message_label.config(background=adapt_os(linx='light grey'))
    #for button in toolbar2.winfo_children():
    #    button.config(background=adapt_os(linx='light grey'))
    toolbar2.update()
    canvas2.get_tk_widget().pack(side=TOP, fill=X, expand=1)

    situation = 1

    table = pd.pivot_table(out_field, values='z', index=['x'], columns=['y'])
    bins = np.linspace(0, 1, N + 1)

    def calc_auc(x, y, p, q):
        result = 1 - (0.5 + (p * q - (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
            (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                        (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (
                    p + q) + sqrt((2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                    (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                    2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                            (x - .5) - (y - .5)) ** 2))))) / 2 + (q / (q + (
                    2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                            (x - .5) - (y - .5)) ** 2)))) * ((0.5 + (p * q - (
                    2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                            (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                    p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
            (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                        (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                    2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                            (x - .5) - (y - .5)) ** 2))))) - 1) * (0.5 + (p * q - (
                    2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                            (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                    p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
            (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                        (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                    2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                            (x - .5) - (y - .5)) ** 2))))) / 2 + \
                 sqrt((2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) * ((2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (
                             p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p) / p) / (2 * ((2 * (
                    p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
            (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                        (x - .5) - (y - .5)) ** 2)) + q)) * \
                 (((2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q) * np.arctan(sqrt(q) * np.float64(2 * (0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))) - 1) / (sqrt((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + 4 * q * ((0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))) - (0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))) * (0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))))))) / (4 * sqrt(q)) + (2 * (0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))) - 1) * (sqrt((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + 4 * q * ((0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))) - (0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2))))) * (0.5 + (p * q - (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)) * sqrt(q * ((2 * (
                             p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                     (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                 (x - .5) - (y - .5)) ** 2)) + q + p))) / (2.0 * q * (p + (
                             2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                         (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                     (x - .5) - (y - .5)) ** 2)))))))) / 4 +
                  ((2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                      (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                  (x - .5) - (y - .5)) ** 2)) + q) * np.arctan(np.float64(sqrt(q)) / (sqrt((2 * (
                                     p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                             (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                         (x - .5) - (y - .5)) ** 2))))) / (4 * sqrt(q)) + (sqrt((2 * (
                                     p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q) + sqrt(
                             (2 * (p * (y - .5) ** 2 + q * (x - .5) ** 2) - 0.5 * (p + q)) ** 2 + 4 * p * q * (
                                         (x - .5) - (y - .5)) ** 2)))) / 4)
        return result

    def format_coord(x, y):
        x_ = np.linspace(0, 1, N + 1)[np.digitize((x + 1 / 2 / N), np.linspace(0, 1, N + 1)) - 1]
        y_ = np.linspace(0, 1, N + 1)[np.digitize((y + 1 / 2 / N), np.linspace(0, 1, N + 1)) - 1]
        z_ = table.iloc[np.digitize(x, bins) - 1, np.digitize(y, bins) - 1]
        if act_view_style == "earth":
            return 'Hit Rate = %1.4f, False Alarm Rate=%1.4f, p-value=%1.6f, AUC = %1.6f' % (
            y_, x_, z_, calc_auc(x_, y_, p, q))
        elif act_view_style == "math":
            return 'TP Rate = %1.4f, FP Rate =%1.4f, p-value=%1.6f, AUC = %1.6f' % (y_, x_, z_, calc_auc(x_, y_, p, q))
        else:
            return 'Sensitivity = %1.4f, Specificity=%1.4f, p-value=%1.6f, AUC = %1.6f' % (
            y_, 1 - x_, z_, calc_auc(x_, y_, p, q))

    ax1.format_coord = ax2.format_coord = format_coord

    Results_pad.configure(state='normal')
    Results_pad.delete('1.0', END)
    Results_pad.insert(INSERT, "out_p:")
    Results_pad.insert(END, "\np-value of AUC = ")
    Results_pad.insert(END, str(round(valys, adapt_os(linx=16, macos=15, mswin=16))))
    Results_pad.insert(END, "\nUser defined AUC = " + str(uauc))
    Results_pad.insert(END, "\nP = " + str(p) + ", Q = " + str(q))
    Results_pad.insert(END, "\n\nout_F1H1:")
    Results_pad.insert(END, "\np-value of k-ellipse (F\u2081, H\u2081) =\n")
    Results_pad.insert(END, str(round(mvals, adapt_os(linx=16, macos=15, mswin=16))))
    Results_pad.insert(END, "\nAUC of k-ellipse (F\u2081, H\u2081) =\n")
    Results_pad.insert(END, str(round(mauc, adapt_os(linx=16, macos=15, mswin=16))))
    Results_pad.insert(END, "\nF\u2081= " + str(f1) + ", H\u2081= " + str(h1))
    if str(raw_data) != "None" and str(raw_data) != "ErrorData":
        Results_pad.insert(END, "\n\nFiles_data_ROC:")
        Results_pad.insert(END, "\np-value of user's ROC data AUC =\n")
        Results_pad.insert(END, str(round(PVAUC_file, adapt_os(linx=16, macos=15, mswin=16))))
        Results_pad.insert(END, "\nFile's ROC data AUC =\n")
        Results_pad.insert(END, str(round(area, adapt_os(linx=16, macos=15, mswin=16))))
        Results_pad.insert(END, "\nP = " + str(p) + ", Q = " + str(q))
    else:
        Results_pad.insert(END, "\n\nNo input file\n\n\n\n\n")

    Results_pad.tag_add("small black", "2.0", "2.16", "3.0", "3.18", "4.0", "4.3", "4.6", "4.12", "7.0", "7.end", "9.0",
                        "9.end", "11.0", "11.2",
                        "{}.{}".format(11, 2 + len(str(f1)) + 4), "{}.{}".format(11, 2 + len(str(f1)) + 6),
                        "14.0", "14.end", "16.0", "16.end", "18.0", "18.4", "{}.{}".format(18, 4 + len(str(p))),
                        "{}.{}".format(18, 9 + len(str(p))))
    Results_pad.tag_add("blue", "1.0", "1.end", "3.0", "3.16")
    Results_pad.tag_add("dark_violet", "6.0", "6.end", "7.22", "7.24", "7.26", "7.28", "9.18", "9.20", "9.22", "9.24",
                        "11.0", "11.2",
                        "{}.{}".format(11, 2 + len(str(f1)) + 4), "{}.{}".format(11, 2 + len(str(f1)) + 6))
    Results_pad.tag_add("dark_cyan_lime_green", "13.0", "13.end")
    Results_pad.tag_add("blue-green", "2.17", "2.end", "3.19", "3.end", "4.4", "{}.{}".format(4, 4 + len(str(p))),
                        "{}.{}".format(4, 4 + 6 + len(str(p))), "4.end",
                        "8.0", "8.end", "10.0", "10.end", "11.4", "{}.{}".format(11, 4 + len(str(f1))),
                        "{}.{}".format(11, 9 + len(str(f1))), "11.end", "15.0",
                        "15.end",
                        "17.0", "17.end", "18.4", "{}.{}".format(18, 4 + len(str(p))),
                        "{}.{}".format(18, 10 + len(str(p))), "18.end")

    Results_pad.configure(state=DISABLED)

    progress_bar['value'] += (N + 1) * (N + 1)
    status.update_idletasks()

    p_old, q_old, f1_old, h1_old, uauc_old, ROCti_old, N_old, raw_data_old = p, q, f1, h1, uauc, ROCti, N, raw_data

    graph_screen.select(0)

    progress_bar['value'] = 0

class F1_H1_messages():
    def __init__(self, test):
        if test == "earth":
            self.F1_button_help_msg = """Enter here the False Alarm Rate value, or F1 of the point (F\u2081, H\u2081) on the ROC diagram through which passes the k-ellipse for which you want to calculate the p-value\n
            Attention: F\u2081<H\u2081, False Alarm Rate must be less than Hit Rate"""
            self.H1_button_help_msg = """Enter here the Hit Rate value, or H1 of the point (F\u2081, H\u2081) on the ROC diagram through which passes the k-ellipse for which you want to calculate the p-value\n
            Attention:
            H\u2081>F\u2081, Hit Rate must be greater than False Alarm Rate"""
        else:
            self.F1_button_help_msg = """Enter here the (1-Specificity) value, or F1 of the point (F\u2081, H\u2081) on the ROC diagram through which passes the k-ellipse for which you want to calculate the p-value\n
            Attention: F\u2081<H\u2081, (1-Specificity) must be less than Sensitivity"""
            self.H1_button_help_msg = """Enter here the Sensitivity value, or H1 of the point (F\u2081, H\u2081) on the ROC diagram through which passes the k-ellipse for which you want to calculate the p-value\n
            Attention:
            H\u2081>F\u2081, Sensitivity must be greater than (1-Specificity)"""

root = Tk()

root.title("VISROC 2.0 application")


myImg = ImageTk.PhotoImage(Image.open(resource_path("LOGO_VISROC_75x75.png")))
root.iconphoto(True, myImg)
from tkinter import font
default_foreground_color = 'gray20'
root.option_add('*Foreground', default_foreground_color)
root.option_add('*Entry.selectBackground', '#008aa3')
root.option_add('*Entry.selectForeground', 'white')
root.option_add('*activeBackground', '#053740')
root.option_add('*activeForeground', 'white')


#define fonts
default_font_family = 'TkDefaultFont'
font_size = adapt_os(linx=11, macos=17, mswin=12)
myFont = tkFont.Font(size=font_size,
                     family=adapt_os(linx='Arial', macos=default_font_family, mswin='Arial'))
myFont_results_title = tkFont.Font(size=font_size+adapt_os(linx=3, macos=3, mswin=2), weight=adapt_os(linx=tkFont.BOLD, macos=tkFont.NORMAL, mswin=tkFont.NORMAL),
                                   family=adapt_os(linx='Arial', macos=default_font_family, mswin='Arial'))
myFont_about = tkFont.Font(size=adapt_os(linx=9, macos=14, mswin=9),
                           family=adapt_os(linx='Arial', macos=default_font_family, mswin='Arial'))
myFont_about_title = tkFont.Font(size=adapt_os(linx=15, macos=18, mswin=15), weight=tkFont.BOLD,
                                 family=adapt_os(linx='Arial', macos=default_font_family, mswin='Arial'))
root.option_add('*Dialog.msg.font', myFont_about)

w = 1024 # width for the Tk root
h = 860 # height for the Tk root
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#root.tk.call('tk', 'scaling', 4.0)
root.resizable(False, False)

situation = 0
act_view_style = "earth"
about_window=None

try:
    copied = root.clipboard_get()
except TclError:
    copied = None

right_click_menu = Menu(root, tearoff = 0)
right_click_menu.add_command(label ="Cut", state="disabled", command=lambda: cut_text(1))
right_click_menu.add_command(label ="Copy", state="disabled", command=lambda: copy_text(1))
right_click_menu.add_command(label ="Paste", state="disabled", command=lambda: paste_text(1))
right_click_menu.add_separator()
right_click_menu.add_command(label ="Clear", state="disabled", command=lambda: clear_text(1))
right_click_menu.bind("<Leave>",popupFocusOut)

root.bind("<Button-3>", prepare_popup)
    
# Create menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
submenu1 = Menu(filemenu, tearoff=0)
submenu2 = Menu(filemenu, tearoff=0)
submenu1.add_command(label="ROC plot", command=lambda :save_as_plot(fig1, "ROC_curve_P"+str(p)+"_Q"+str(q)))
submenu1.add_command(label="Plot (F\u2081, H\u2081)", command=lambda :save_as_plot(fig2, "Plot_"+(str(h1)+"_"+str(f1)).replace('.','')))
submenu1.add_separator()
submenu1.add_command(label="out_field", command=lambda : save_as_file_csv(out_field))
submenu1.add_command(label="out_CL", command=lambda : save_as_file_csv(out_CL))
submenu1.add_command(label="out_p", command=lambda : save_as_file_csv(out_p))
submenu1.add_command(label="out_F1H1", command=lambda : save_as_file_csv(out_F1H1))
submenu1.add_command(label="out_k_F1H1", command=lambda : save_as_file_csv(out_k_F1H1))
submenu2.add_command(label="Save ROC plot (.png)", command=lambda :save_as_plot(fig1, "ROC_curve_P"+str(p)+"_Q"+str(q)))
submenu2.add_command(label="Save Plot (F\u2081, H\u2081) (.png)", command=lambda :save_as_plot(fig2, "Plot_"+(str(h1)+"_"+str(f1)).replace('.','')))
submenu2.add_separator()
submenu2.add_command(label="out_field (.csv)", command=lambda : save_csv(out_field))
submenu2.add_command(label="out_CL (.csv)", command=lambda : save_csv(out_CL))
submenu2.add_command(label="out_p (.csv)", command=lambda : save_csv(out_p))
submenu2.add_command(label="out_F1H1 (.csv)", command=lambda : save_csv(out_F1H1))
submenu2.add_command(label="out_k_F1H1 (.csv)", command=lambda : save_csv(out_k_F1H1))
filemenu.add_cascade(label='Save as...', menu=submenu1, state="disabled")
filemenu.add_cascade(label='Save', menu=submenu2, state="disabled")
filemenu.add_command(label="Save all (.zip)", command=save_zip, state="disabled")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Hit Rate / False-Alarm Rate View", command=lambda : toggle_view("earth"))
viewmenu.add_command(label="Sensitivity / Specificity View", command=lambda : toggle_view("med"))
viewmenu.add_command(label="True Positive Rate / False Positive Rate", command=lambda : toggle_view("math"))
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=open_help)
helpmenu.add_command(label="About", command=open_about)
menubar.add_cascade(label="View", menu=viewmenu)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

graph_screen = ttk.Notebook(root, padding=0, width=703, height=755)
graph_screen.grid(row=0, column=0)
style_tabs = ttk.Style()
style_tabs.configure('TButton', background=adapt_os('grey75'))
style_tabs.configure('TNotebook.Tab',
                     font=adapt_os(linx=('Calibri', '12'), macos=(default_font_family, '17'), mswin=('Calibri', '12')),
                     foreground='#053740',
                     padding=adapt_os(linx=[130, 7], mswin=[136,5], macos=[125,7]))
graph1 = Frame(graph_screen, width=adapt_os(linx=696, macos=496, mswin=696), height=912, relief=SUNKEN, bd=4)
graph2 = Frame(graph_screen, width=adapt_os(linx=696, macos=496, mswin=696), height=912, relief=SUNKEN, bd=4)
graph1.pack(fill="both", expand=1)
graph2.pack(fill="both", expand=1)

graph_screen.add(graph1, text="ROC curve")
graph_screen.add(graph2, text="Plot (F\u2081, H\u2081)")

extra_margin = Frame(root, pady=0)
extra_margin.config(width=100, relief=GROOVE)
graph_screen.grid(row=0, column=0, padx=(4, 0))
extra_margin.grid(row=1, column=0, padx=(4,0), pady=(adapt_os(linx=0, macos=0, mswin=1), 0))

graph_interpr_window = None

try:
    info_interpretation_button = Buttonette(extra_margin, text='Graph Interpretation',
                                            fg=default_foreground_color, font=myFont,
                                            command=open_close_graph_interpretation)
except NameError:
    info_interpretation_button = ttk.Button(extra_margin, text='Graph Interpretation', command = open_close_graph_interpretation)
info_interpretation_button.grid(row=0, column=0, columnspan=1, sticky="se", padx=0, pady=adapt_os(linx=0, macos=1, mswin=0), ipady=adapt_os(linx=5, macos=5, mswin=7))
linkaddress = "10.1016/j.cpc.2013.12.009"
copyleft = Label(extra_margin, text = "DOI: "+linkaddress,
                 pady=adapt_os(linx=9,mswin=8,macos=5), relief=GROOVE,
                 width=adapt_os(linx=69,mswin=64,macos=52),
                 padx=adapt_os(linx=2, mswin=2,macos=0),
                 font=adapt_os(macos=(default_font_family, 15), linx="Arial 11 bold", mswin="Arial 11 bold"),
                 fg="#053740", cursor="hand2")
copyleft.bind("<Button-1>", lambda e:webbrowser.open_new_tab("https://doi.org/"+linkaddress))
copyleft.grid(row=0, column=1, columnspan=6, sticky=adapt_os(mswin="sw", linx="sw", macos="nw"),
              padx=adapt_os(mswin=(5, 0), linx=(4,2), macos=(2,0)),
              pady=(adapt_os(macos=5,linx=6,mswin=4), adapt_os(macos=0, linx=0, mswin=0)))###ti kanei telika to linx?



rightside_screen = Frame(root)
rightside_screen.grid(row=0, column=1, rowspan=2, padx=(2, 0), pady=(0, 0))

input_screen = Frame(rightside_screen)
input_screen.config(width=49, relief=GROOVE)
input_screen.grid(row=0, column=0, sticky="w")
central_buttons_screen = Frame(rightside_screen)
if not sys.platform=="darwin":
    central_buttons_screen.config(width=49, relief=FLAT)
else: central_buttons_screen.config(relief=FLAT, bd=1, bg='#d7dde4')
central_buttons_screen.grid(row=1, column=0,
                            padx=adapt_os(linx=(2, 0), macos=0, mswin=(2,0)),
                            pady=adapt_os(mswin=0, macos=4, linx=4),
                            sticky=adapt_os(mswin="w", macos="ew", linx="w"))
output_screen = LabelFrame(rightside_screen, text="Results", font=myFont_results_title, fg="#053740",
                           width=adapt_os(linx=100, mswin=100),
                           height=adapt_os(mswin=400, macos=400, linx=400))
output_screen.grid(row=2, column=0, padx=2, pady=0, sticky='nws')

p_old = None
p = None
q_old = None
q = None
N_old = None
N_entry = None
N = None
uauc_old = None
uauc_entry = None
uauc = None
f1_old = None
f1_entry = None
f1 = None
h1_old = None
h1_entry = None
h1 = None
ROCti_old = None
ROCti = None
inFile_temp = None
inFile = None
raw_data_old = None
raw_data = None
data = None

out_field = None
out_CL = None
out_p = None
out_F1H1 = None
out_k_F1H1 = None

try:
    Browse_button = Buttonette(input_screen, text='Browse...', command=import_csv_data, fg=default_foreground_color,
                               font=myFont, borderless=1, padx=adapt_os(macos=0), pady=3)
    Plot_button = Buttonette(central_buttons_screen, text='Plot',
                             font=adapt_os(macos=(default_font_family, "18"), mswin="Calibri 16"),
                             bg="#007AFF", fg="white",
                             activebackground="#012229", activeforeground="white",
                             bd=0, height=23, width=150,
                             borderless=1, padx=adapt_os(macos=0), pady=0)
    Positives_button = Label(input_screen,
                             text="P (Positives)", anchor="w", cursor="question_arrow",
                             relief=FLAT, borderwidth=0, font=myFont, fg="#053740")
    Positives_button.bind("<Button-1>", lambda event: popup("\nEnter the number of positive events 'P' here"))
    Negatives_button = Label(input_screen,
                             text="Q (Negatives)", anchor="w", cursor="question_arrow",
                             relief=FLAT, borderwidth=0, font=myFont, fg="#053740")
    Negatives_button.bind("<Button-1>", lambda event: popup("\nEnter the number of negative events 'Q' here"))

    Resolution_button = Label(input_screen,
                              text="Resolution", anchor="w", cursor="question_arrow",
                              relief=FLAT, borderwidth=0, font=myFont, fg="#053740")
    Resolution_button.bind("<Button-1>",
                           lambda event: popup("Slide to define the resolution, that is the number 'N' of segments"
                                               "in which the interval [0,1] is divided for the calculation of the p-values"
                                               "on a square lattice in the ROC diagram"
                                               "\n\n* To fine-tune the resolution by one (+1/-1), "
                                               "you can click correspondingly on the trough right/left of the slider"))
    AUC_button = Label(input_screen,
                       text="User defined AUC", anchor="w", cursor="question_arrow",
                       relief=FLAT, borderwidth=0, font=myFont, fg="#00008B")
    AUC_button.bind("<Button-1>",
                    lambda event: popup("Enter the value of the AUC (Area Under the Curve) of a ROC diagram,"
                                        "for which you would like to calculate the p-value"))
    F1_button = Label(input_screen,
                      text="F\u2081", anchor="w", cursor="question_arrow",
                      relief=FLAT, borderwidth=0, font=myFont, fg="#7030A0")
    F1_button.bind("<Button-1>", lambda event: popup(F1_H1_messages(act_view_style).F1_button_help_msg))
    H1_button = Label(input_screen,
                      text="H\u2081", anchor="w", cursor="question_arrow",
                      relief=FLAT, borderwidth=0, font=myFont, fg="#7030A0")
    H1_button.bind("<Button-1>", lambda event: popup(F1_H1_messages(act_view_style).H1_button_help_msg))
    Title_button = Label(input_screen,
                         text="Set title:", anchor="w", cursor="question_arrow",
                         relief=FLAT, borderwidth=0, font=myFont, fg="#053740")
    Title_button.bind("<Button-1>", lambda event: popup("\nHere you can enter the diagram title of your choice"))
    Data_button = Label(input_screen,
                        text="Load user's ROC data", anchor="w", cursor="question_arrow",
                        relief=FLAT, borderwidth=0, font=myFont, fg="#00B050")
    Data_button.bind("<Button-1>", lambda event: popup("\nChoose the data file you want to feed into the algorithm"))



except NameError:
    Browse_button = Button(input_screen, text='Browse...', command=import_csv_data, font=myFont,
                           bg=adapt_os(linx='grey75'),
                           activebackground=adapt_os(linx='grey85'),
                           activeforeground=adapt_os(linx=default_foreground_color), padx=adapt_os(linx=4))
    Plot_button = Menubutton(central_buttons_screen, text='Plot',
                             font=adapt_os(linx="Calibri 13", mswin="Calibri 16"),
                             bg="#053740", fg="white",
                             activebackground="#012229", activeforeground="white",
                             width=adapt_os(linx=12, mswin=12), bd=0)
    Positives_button = Button(input_screen,
                              command=lambda: popup("Enter the number of positive events 'P' here"),
                              text="P (Positives)", anchor="w",
                              cursor="question_arrow", relief=SUNKEN,
                              borderwidth=0, font=myFont, fg="#053740",
                              activeforeground=adapt_os(linx='#053740', mswin='#053740'),
                              activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')))
    Negatives_button = Button(input_screen,
                              command=lambda: popup("Enter the number of negative events 'Q' here"),
                              text="Q (Negatives)", anchor="w",
                              cursor="question_arrow", relief=SUNKEN,
                              borderwidth=0, font=myFont, fg="#053740",
                              activeforeground=adapt_os(linx='#053740', mswin='#053740'),
                              activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')))
    Resolution_button = Button(input_screen,
                               command=lambda: popup(
                                   "Slide to define the resolution, that is the number 'N' of segments"
                                   "in which the interval [0,1] is divided for the calculation of the p-values"
                                   "on a square lattice in the ROC diagram"
                                   "\n\n* To fine-tune the resolution by one (+1/-1), "
                                   "you can click correspondingly on the trough right/left of the slider"),
                               text="Resolution", anchor="w",
                               cursor="question_arrow", relief=SUNKEN,
                               borderwidth=0, font=myFont, fg="#053740",
                               activebackground=adapt_os(linx=root.cget('bg')),
                               activeforeground=adapt_os(linx='#053740'))
    AUC_button = Button(input_screen,
                        command=lambda: popup("Enter the value of the AUC (Area Under the Curve) of a ROC diagram,"
                                              "for which you would like to calculate the p-value"),
                        text="User defined AUC", anchor="w",
                        cursor="question_arrow", relief=SUNKEN,
                        borderwidth=0, font=myFont, fg="#00008B",
                        activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')),
                        activeforeground=adapt_os(linx='#00008B', mswin='#00008B'))
    F1_button = Button(input_screen,
                   command=lambda: popup(F1_H1_messages(act_view_style).F1_button_help_msg),
                   text="F\u2081", anchor="w",
                   cursor="question_arrow", relief=SUNKEN,
                   borderwidth=0, font=("Verdana", "12"), fg="#7030A0",
                   activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')),
                   activeforeground=adapt_os(linx='#053740', mswin='#053740'))
    H1_button = Button(input_screen,
                   command=lambda: popup(F1_H1_messages(act_view_style).H1_button_help_msg),
                   text="H\u2081", anchor="w", cursor="question_arrow", relief=SUNKEN,
                   borderwidth=0, font=("Verdana", "12"), fg="#7030A0",
                   activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')),
                   activeforeground=adapt_os(linx='#053740', mswin='#053740'))
    Title_button = Button(input_screen,
                      command=lambda: popup("Here you can enter the diagram title of your choice"),
                      text="Set title:", anchor="w", cursor="question_arrow", relief=SUNKEN,
                      borderwidth=0, font=myFont, fg="#053740",
                      activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')),
                      activeforeground=adapt_os(linx='#053740', mswin='#053740'))
    Data_button = Button(input_screen,
                     command=lambda: popup("Choose the data file you want to feed into the algorithm"),
                     text="Load user's ROC data", anchor="w", cursor="question_arrow",
                     relief=SUNKEN, borderwidth=0, font=myFont, fg="#00B050",
                     activebackground=adapt_os(linx=root.cget('bg'), mswin=root.cget('bg')),
                     activeforeground=adapt_os(linx='#00B050', mswin='#00B050'))

Positives_button.grid(row=0, column=0, sticky="w", padx=adapt_os(linx=0, macos=0, mswin=3), columnspan=7)

sv_positives = StringVar()
Positives_entry = Entry(input_screen, relief=GROOVE,
                        width=adapt_os(linx=17, macos=11, mswin=15),
                        font=myFont, textvariable=sv_positives, highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
Positives_entry.insert(0, 15)
Positives_entry.grid(row=1, column=0,
                     pady=(adapt_os(linx=0,macos=3,mswin=0), adapt_os(linx=0,macos=7,mswin=2)),
                     sticky="W", padx=adapt_os(linx=9, macos=0, mswin=5), columnspan=7)

Negatives_button.grid(row=0, column=adapt_os(linx=6,macos=7, mswin=6), sticky="w",
                      padx=adapt_os(linx=15, macos=0, mswin=22), columnspan=7)

sv_negatives = StringVar()
Negatives_entry = Entry(input_screen, relief=GROOVE,
                        width=adapt_os(linx=17, macos=11, mswin=15),
                        font=myFont, textvariable=sv_negatives, highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
Negatives_entry.insert(0, 35)
Negatives_entry.grid(row=1, column=7,
                     pady=(adapt_os(linx=0, macos=3, mswin=0), adapt_os(linx=0, macos=7, mswin=2)),
                     sticky="w", padx=adapt_os(linx=(1,0), macos=0, mswin=5), columnspan=7)


Resolution_button.grid(row=2, column=0, columnspan=14, sticky="sw",
                       padx=adapt_os(linx=0, macos=0, mswin=3))

iv_slider = IntVar()
Resolution_Slider = Scale(input_screen, from_=0, to=1000, orient=HORIZONTAL,
                          tickinterval=100, resolution=1, variable = iv_slider,
                          length=adapt_os(linx=294, macos=278, mswin=294),
                          font=(default_font_family, adapt_os(linx=7, macos=10, mswin=7)))
Resolution_Slider.set(100)
Resolution_Slider.grid(row=3, column=0, columnspan=14, sticky="NW",
                       padx=adapt_os(linx=6, macos=0, mswin=2))

AUC_button.grid(row=4, column=0, columnspan=14, sticky="w",
                padx=adapt_os(linx=0, macos=0, mswin=3))
sv_uauc = StringVar()
AUC_entry = Entry(input_screen, width=adapt_os(linx=36, macos=25, mswin=32),
                  relief=GROOVE, font=myFont, textvariable=sv_uauc, highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
AUC_entry.insert(0, 0.51)
AUC_entry.grid(row=5, column=0, columnspan=14,
               padx=adapt_os(linx=9, macos=0, mswin=5),
               sticky="NW", pady=adapt_os(macos=6, mswin=(0,2)))

F1_button.grid(row=6, column=0, sticky="w", padx=adapt_os(linx=0, macos=0, mswin=3), columnspan=7)
sv_f1 = StringVar()
F1_entry = Entry(input_screen, relief=GROOVE, width=adapt_os(linx=17, macos=11, mswin=15),
                 font=myFont, textvariable=sv_f1, highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
F1_entry.insert(0, 0.65)
F1_entry.grid(row=7, column=0, sticky="W", columnspan=7,
              pady=(adapt_os(linx=0, macos=3, mswin=0), adapt_os(linx=0, macos=6, mswin=2)),
              padx=adapt_os(linx=9, macos=0, mswin=5))

H1_button.grid(row=6, column=adapt_os(linx=6,mswin=6,macos=7),
               sticky="w", padx=adapt_os(mswin=22, macos=0, linx=15), columnspan=7)
sv_h1 = StringVar()
H1_entry = Entry(input_screen, relief=GROOVE, width=adapt_os(linx=17, macos=11, mswin=15),
                 font=myFont, textvariable=sv_h1, highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
H1_entry.insert(0, 0.75)
H1_entry.grid(row=7, column=7,
              pady=(adapt_os(linx=0, macos=3, mswin=0), adapt_os(linx=0, macos=6, mswin=2)),
              sticky="w", padx=adapt_os(linx=(1,0), macos=0, mswin=5), columnspan=7)

Title_button.grid(row=8, column=0, columnspan=14, sticky="w",
                  padx=adapt_os(linx=0, macos=0, mswin=3))
sv_title = StringVar()
Title_entry = Entry(input_screen, relief=GROOVE, width=adapt_os(linx=36, macos=25, mswin=32),
                    font=myFont, textvariable=sv_title, highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
Title_entry.insert(0, " ")
Title_entry.grid(row=9, column=0, columnspan=14,
                 pady=(adapt_os(linx=0, macos=3, mswin=0), adapt_os(linx=0, macos=6, mswin=0)),
                 padx=adapt_os(linx=9, macos=0, mswin=5), sticky="NW")

Data_button.grid(row=10, column=0, columnspan=14, sticky="w",
                 padx=adapt_os(linx=0, macos=0, mswin=3),
                 pady=(adapt_os(linx=0, mswin=0, macos=(1,0))))

Browse_button.grid(row=11, column=0, rowspan=2, columnspan=4, sticky="w",
                   padx=(adapt_os(linx=9, macos=0, mswin=6), adapt_os(linx=4, macos=9, mswin=0)), pady=0)

v = StringVar()
file_entry = Entry(input_screen, relief=GROOVE,
                   textvariable=v.get(),
                   width=adapt_os(linx=25, macos=17, mswin=34),
                   highlightthickness=adapt_os(macos=0, linx=1, mswin=0))
file_entry.grid(row=11, column=4, columnspan=10, sticky="nw",
                padx=adapt_os(linx=(7,6), macos=0, mswin=3),
                pady=(adapt_os(linx=0, mswin=0, macos=2),
                      adapt_os(linx=0, macos=0, mswin=1)))

file_entered = Frame(input_screen)
file_entered.config(width=adapt_os(linx=210, macos=160, mswin=210), height=18, bd=0)
file_entered.grid_propagate(0)
file_entered.grid(row=12, column=4, columnspan=10, sticky="w", padx=0, pady=0)

entered_file = Label(master=file_entered, text="", font=adapt_os(linx="Arial 8", macos=(default_font_family, "14"), mswin="Arial 8"))
entered_file.place(x=0, y=adapt_os(macos=-5))
delete_entered_file = Button(master=file_entered, text="x", relief=FLAT,
                             activeforeground=adapt_os(linx='dark red', macos="dark red"))

sv_infile = StringVar()

file_entry.bind('<KeyRelease>', import_csv_data_manualy)

sv_positives.trace_add("write", lambda name, index, mode: callback())
sv_negatives.trace_add("write", lambda name, index, mode: callback())
iv_slider.trace_add("write", lambda name, index, mode: callback())
sv_f1.trace_add("write", lambda name, index, mode: callback())
sv_h1.trace_add("write", lambda name, index, mode: callback())
sv_uauc.trace_add("write", lambda name, index, mode: callback())
sv_title.trace_add("write", lambda name, index, mode: callback())
sv_infile.trace_add("write", lambda name, index, mode: callback())

img_graph_interpr = Image.open(resource_path("graph_interpretation.png"))
img_graph_interpr = ImageTk.PhotoImage(img_graph_interpr)
img_graph_interpr_label_1 = ttk.Label(graph1, image=img_graph_interpr)
img_graph_interpr_label_1.pack(side=TOP)
img_graph_interpr_label_2 = ttk.Label(graph2, image=img_graph_interpr)
img_graph_interpr_label_2.pack(side=TOP)

Plot_button.grid(row=0, column=0, sticky="w", pady=adapt_os(linx=0, macos=12, mswin=6),
                 padx=adapt_os(linx=(7,0), macos=0, mswin=(6,3)))
Plot_button.bind("<Button-1>", assign)
root.bind('<Return>', assign)

Save_button = Menubutton(central_buttons_screen,
                         text=adapt_os(linx='Save', macos='      Save', mswin='Save'),
                         font=adapt_os(linx="Calibri 13", mswin="Calibri 16", macos=(default_font_family, "18")),
                         bg=adapt_os(linx="#053740", mswin="#053740"),
                         fg=adapt_os(linx="white", mswin="white", macos="#36587d"),
                         activebackground=adapt_os(mswin="#012229", linx="#012229"),
                         activeforeground=adapt_os(mswin="white", linx="white"),
                         relief=adapt_os(macos=FLAT),
                         width=adapt_os(linx=12, macos=8, mswin=12),
                         bd=0)
Save_button.grid(row=0, column=1, sticky="e", pady=adapt_os(linx=0, macos=12, mswin=6), padx=adapt_os(linx=9, macos=3, mswin=5))

Save_button.menu = Menu(Save_button, tearoff=0, bd=10, activebackground="#053740", activeborderwidth=0,
                        borderwidth=0, relief=FLAT)
submenu_save_as = Menu(Save_button, tearoff=0, bd=10, activebackground="#053740", relief=FLAT, activeborderwidth=0)
submenu_save = Menu(Save_button, tearoff=0, bd=10, activebackground="#053740", relief=FLAT, activeborderwidth=0)
Save_button["menu"] = Save_button.menu
Save_button.menu.add_cascade(label='Save as...', menu=submenu_save_as, state="disabled")
Save_button.menu.add_separator()
Save_button.menu.add_cascade(label='Save', menu=submenu_save, state="disabled")
Save_button.menu.add_separator()
Save_button.menu.add_command(label="Save all (.zip)", command=save_zip, state="disabled")

submenu_save_as.add_command(label="ROC plot", command=lambda: save_as_plot(fig1, "ROC_curve_P"+str(p)+"_Q"+str(q)))
submenu_save_as.add_command(label="Plot (F\u2081, H\u2081)", command=lambda: save_as_plot(fig2, "Plot_"+(str(h1)+"_"+str(f1)).replace('.','')))
submenu_save_as.add_separator()
submenu_save_as.add_command(label="out_field", command=lambda: save_as_file_csv(out_field))
submenu_save_as.add_command(label="out_CL", command=lambda: save_as_file_csv(out_CL))
submenu_save_as.add_command(label="out_p", command=lambda: save_as_file_csv(out_p))
submenu_save_as.add_command(label="out_F1H1", command=lambda: save_as_file_csv(out_F1H1))
submenu_save_as.add_command(label="out_k_F1H1", command=lambda: save_as_file_csv(out_k_F1H1))

submenu_save.add_command(label="ROC plot (.png)", command=lambda: save_plot(fig1, "ROC_curve_P"+str(p)+"_Q"+str(q)))
submenu_save.add_command(label="Plot (F\u2081, H\u2081) (.png)", command=lambda: save_plot(fig2, "Plot_"+(str(h1)+"_"+str(f1)).replace('.','')))
submenu_save.add_separator()
submenu_save.add_command(label="out_field (.csv)", command=lambda: save_csv(out_field))
submenu_save.add_command(label="out_CL (.csv)", command=lambda: save_csv(out_CL))
submenu_save.add_command(label="out_p (.csv)", command=lambda: save_csv(out_p))
submenu_save.add_command(label="out_F1H1 (.csv)", command=lambda: save_csv(out_F1H1))
submenu_save.add_command(label="out_k_F1H1 (.csv)", command=lambda: save_csv(out_k_F1H1))

Results_pad = Text(output_screen, width=adapt_os(mswin=32, linx=32, macos=27),
                   height=21, bg=output_screen.cget("background"), padx=4, pady=adapt_os(linx=0, macos=0, mswin=5), relief=FLAT)
Results_pad.config(font=adapt_os(mswin="Arial 13", macos=(default_font_family, "15"), linx= "Arial 12"))
Results_pad.insert(INSERT, "out_p:")
Results_pad.insert(END, "\n\n\n\n\nout_F1H1:")
Results_pad.insert(END, "\n\n\n\n\n\n\nFiles_data_ROC:")

Results_pad.tag_config("blue-green", foreground="#053740")
Results_pad.tag_config("small black", font=adapt_os(mswin="Calibri 12", linx="Calibri 11", macos=(default_font_family, "14")))
Results_pad.tag_config("blue", foreground="#00008B")
Results_pad.tag_config("dark_violet", foreground="#7030A0")
Results_pad.tag_config("dark_cyan_lime_green",  foreground="#00B050")
Results_pad.tag_config("red", foreground="red")

Results_pad.tag_add("blue", "1.0", "1.end")
Results_pad.tag_add("dark_violet", "6.0", "6.end")
Results_pad.tag_add("dark_cyan_lime_green", "13.0", "13.end")

Results_pad.configure(state=DISABLED)

separator1 = ttk.Separator(Results_pad, orient='horizontal')
separator1.place(relx=0, rely=0.21, relwidth=1, relheight=.005)
separator2 = ttk.Separator(Results_pad, orient='horizontal')
separator2.place(relx=0, rely=adapt_os(mswin=0.547, macos=0.545, linx=0.545), relwidth=1, relheight=.005)
separator3 = ttk.Separator(Results_pad, orient='horizontal')
separator3.place(relx=0, rely=adapt_os(mswin=0.87, macos=0.88, linx=0.88), relwidth=1, relheight=.005)

Error_Info_Button_border = Frame(Results_pad)

Results_pad.pack()

status = Label(root)
status.place(relwidth=1, height=10, x=0, y=adapt_os(mswin=842, macos=842, linx=844))

percent = 0
progress_bar = ttk.Progressbar(status, length=adapt_os(mswin=1013, macos=1015, linx=1015), mode="determinate", maximum=100, value=percent)
progress_bar.grid(row=0, column=0, padx=(3,0), sticky = "S")

root.mainloop()
