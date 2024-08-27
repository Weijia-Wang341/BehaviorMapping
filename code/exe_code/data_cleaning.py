import os
import re
import pandas as pd
from tkinter import *
from tkinter import filedialog



root = Tk()
root.title('Data Cleaning')
root.geometry("700x200")

selected_folder = StringVar(root, value="No folder selected")
selected_save_path = StringVar(root, value="No save path selected")

def process_pdfs(folder_path, csv_file_path):
    if not folder_path or not csv_file_path:
        print("Input folder or output file pathis not set.")
        return 
    
    df = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_file = os.path.join(folder_path, filename)

            project_id = os.path.splitext(pdf_file)[0].split('-')[1]
            time = os.path.splitext(pdf_file)[0].split('-')[2]
            time = f"{time[:2]}:{time[2:]}"

            subj_pattern = re.compile(r'/Subj\((.*?)\)')
            rect_pattern = re.compile(r'/Rect\[(.*?)\]')
            contents_pattern = re.compile(r'<p>([\s\S]*?)<\/p>')
            color_pattern = re.compile(r'/C\[(.*?)\]')
            rt_pattern = re.compile(r'/RT/(.*?)/')

            with open(pdf_file, mode='rb') as f1:
                for line in f1:
                    line_str = line.decode('UTF-8', errors='ignore')
                    if 'PolyLine' in line_str or "Ellipse" in line_str:
                        subj_match = subj_pattern.search(line_str)
                        rect_coords = list(map(float, rect_pattern.search(line_str).group(1).split()))
                        contents_match = contents_pattern.search(line_str)
                        cleaned_contents = re.sub(r'<[^>]+>', '', contents_match.group(1)) if contents_match else ''
                        color_match = list(map(float, color_pattern.search(line_str).group(1).split()))
                        rt_match = rt_pattern.search(line_str)
                        if rect_coords:  # center coordinates
                            x_coor = round((rect_coords[0] + rect_coords[2]) / 2, 4)
                            y_coor = round((rect_coords[1] + rect_coords[3]) / 2, 4)
                        
                        df.append([
                            subj_match.group(1) if subj_match else '',
                            rect_coords,
                            cleaned_contents,
                            color_match,
                            rt_match.group(1) if rt_match else '',
                            x_coor,
                            y_coor,
                            project_id,
                            time
                            ])


    columns = ['Subj', 'Rect', 'Contents', 'Color', 'RT', 'x_coor', 'y_coor', 'project_id', 'time']
    df = pd.DataFrame(df, columns=columns)
    df = df[~((df['Subj'].str.contains('PolyLine')) & (df['RT'] == 'Group'))]  # Removing duplicates for Walking in Groups
    
    with open(csv_file_path, 'w', newline='') as file:
        df.to_csv(file, index=False)
    print("Data saved to: ", csv_file_path)
    lb.config(text='Process complete and data saved.')

# csv_file_path = input("Please enter the desired file path and file name for saving the CSV file (e.g., C:/path/to/output.csv): ")
# df.to_csv(csv_file_path, index=False)
# print("Data saved to:", csv_file_path)


###### open BB folder #####
def FileOpen():
   folder_path = filedialog.askdirectory(title="Please select a folder")
   if folder_path:
       selected_folder.set(folder_path)


# save CSV file
def FileSave():
   file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
   if file_path:
       selected_save_path.set(file_path)

def RunProcess():
    folder_path = selected_folder.get()
    csv_file_path = selected_save_path.get()
    if folder_path and csv_file_path:
        process_pdfs(folder_path, csv_file_path)
    else:
        lb.config(text="Please select both a folder and a save path.")



lb = Label(root, text='Please select a folder and then save path for the CSV.', font=('Arial', 18))
lb.pack()

frame = Frame(root)
frame.pack(expand=True, padx=20, pady=20)

# bottomframe = Frame(root)
# bottomframe.pack(side=BOTTOM)

# button_open = Button(frame, text='Select a folder', command=FileOpen, fg='black', bg='white')
# button_open.pack(side=LEFT)

# button_save = Button(frame, text='File Save', command=FileSave, fg='black', bg='white')
# button_save.pack(side=LEFT)

# button_run = Button(bottomframe, text='Run', command=RunProcess, fg='white', bg='blue')
# button_run.pack(side=BOTTOM)

Button(frame, text='Open Folder', command=FileOpen, fg='black', bg='white').grid(row=0, column=0, sticky='ew', padx=(0, 10))
Label(frame, textvariable=selected_folder, bg='white').grid(row=0, column=1, sticky='ew')
Button(frame, text='Save File', command=FileSave, fg='black', bg='white').grid(row=1, column=0, sticky='ew', padx=(0, 10))
Label(frame, textvariable=selected_save_path, bg='white').grid(row=1, column=1, sticky='ew')

hex_color='#ffd100'
Button(root, text='Run', command=RunProcess,  fg='white', bg=hex_color).pack(side='bottom', fill='x', padx=20, pady=(0, 20))
frame.columnconfigure(1, weight=1)
root.mainloop()





