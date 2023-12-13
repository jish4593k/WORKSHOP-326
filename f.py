import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import tkinter as tk
from tkinter import filedialog, simpledialog

class PandasModel:
    # This class is used for displaying the DataFrame in a Tkinter Treeview widget
    def __init__(self, df):
        self.df = df

    def data(self, index):
        if index.isValid():
            return str(self.df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if orientation == 1 and role == 0:
            return str(self.df.columns[section])
        return None

    def rowCount(self, parent):
        return len(self.df)

    def columnCount(self, parent):
        return len(self.df.columns)

class CustomDataset(Dataset):
    # PyTorch Dataset class for potential further analysis
    def __init__(self, dataframe):
        self.data = dataframe

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data.iloc[idx].values
        return torch.tensor(sample, dtype=torch.float32)

class DataAnalyzerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Analyzer")
        self.df = None

    def load_data(self):
        # Load data using filedialog
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
        if not file_path:
            return
        file_type = file_path.split(".")[-1]
        if file_type == "csv":
            self.df = pd.read_csv(file_path)
        elif file_type == "json":
            self.df = pd.read_json(file_path)
        else:
            print("Invalid file type.")

    def display_info(self):
        if self.df is not None:
            # Display DataFrame information using PandasModel and Tkinter Treeview
            model = PandasModel(self.df)
            table = ttk.Treeview(self.root)
            table['columns'] = tuple(self.df.columns)
            table['show'] = 'headings'
            for column in self.df.columns:
                table.heading(column, text=column)
            for i in range(len(self.df)):
                table.insert("", "end", values=list(self.df.iloc[i]))
            table.pack()

    def replace_empty_cells(self):
        if self.df is not None:
            # Replace empty cells
            operation = simpledialog.askstring("Data Analysis", "Do you want to replace empty cells? (yes/no)")
            if operation.lower() == "yes":
                type_choice = simpledialog.askstring("Data Analysis", "1 Specific column, 2 All cells")
                if type_choice == "1":
                    column = simpledialog.askstring("Data Analysis", "Data column:")
                    value = simpledialog.askstring("Data Analysis", "Value for fill:")
                    self.df[str(column)].fillna(value, inplace=True)
                elif type_choice == "2":
                    value = simpledialog.askstring("Data Analysis", "Value for fill:")
                    self.df.fillna(value, inplace=True)
                else:
                    print("Not found")

    def plotting(self):
        if self.df is not None:
            # Plot data using Matplotlib
            plot_type = simpledialog.askstring("Data Analysis", "Plotting type 1 classic, 2 customized, 3 advanced")
            if plot_type == "1":
                self.plot_classic()
            elif plot_type == "2":
                self.plot_customized()
            elif plot_type == "3":
                self.plot_advanced()

    def plot_classic(self):
        if self.df is not None:
            # Plot classic using Matplotlib
            print("Plotting started:")
            self.df.plot()
            plt.grid()
            plt.show()

    def plot_customized(self):
        if self.df is not None:
            # Plot customized using Matplotlib
            x = simpledialog.askstring("Data Analysis", "X:")
            y = simpledialog.askstring("Data Analysis", "Y:")
            kind = simpledialog.askstring("Data Analysis", "Kind:")
            print("Plotting started:")
            self.df.plot(kind=str(kind), x=str(x), y=str(y))
            plt.grid()
            plt.show()

    def plot_advanced(self):
        if self.df is not None:
            # Plot advanced using Matplotlib
            kind = simpledialog.askstring("Data Analysis", "Kind:")
            items = simpledialog.askinteger("Data Analysis", "How many items:")
            array = []
            for _ in range(items):
                item = simpledialog.askstring("Data Analysis", "Item:")
                array.append(str(item))
            self.df[array].plot(kind=str(kind))
            plt.grid()
            plt.show()

    def run(self):
        # Set up the GUI and run the mainloop
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        analyze_menu = tk.Menu(menu)
        menu.add_cascade(label="Analyze", menu=analyze_menu)
        analyze_menu.add_command(label="Display Info", command=self.display_info)
        analyze_menu.add_command(label="Replace Empty Cells", command=self.replace_empty_cells)
        analyze_menu.add_command(label="Plot Data", command=self.plotting)

        self.root.mainloop()

if __name__ == "__main__":
    app = DataAnalyzerApp()
    app.run()
