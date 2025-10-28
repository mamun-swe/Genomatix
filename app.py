import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class MLAlgorithmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ML Algorithms Platform")
        self.root.geometry("1000x700")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main container
        self.create_menu()
        self.create_layout()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Dataset", command=self.load_dataset)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_layout(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left sidebar - Algorithm selection
        self.create_sidebar(main_frame)
        
        # Right panel - Work area
        self.create_work_area(main_frame)
        
        # Bottom status bar
        self.create_status_bar(main_frame)
        
    def create_sidebar(self, parent):
        sidebar = ttk.Frame(parent, width=200, relief=tk.RIDGE, borderwidth=2)
        sidebar.grid(row=0, column=0, rowspan=2, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # Title
        title_label = ttk.Label(sidebar, text="ML Algorithms", font=('Arial', 12, 'bold'))
        title_label.pack(pady=10)
        
        # Algorithm categories
        categories = {
            "Supervised Learning": [
                "Linear Regression",
                "Logistic Regression",
                "Decision Trees",
                "Random Forest",
                "SVM",
                "KNN"
            ],
            "Unsupervised Learning": [
                "K-Means",
                "Hierarchical Clustering",
                "PCA",
                "DBSCAN"
            ],
            "Neural Networks": [
                "Perceptron",
                "MLP",
                "CNN",
                "RNN"
            ],
            "Ensemble Methods": [
                "AdaBoost",
                "Gradient Boosting",
                "XGBoost"
            ]
        }
        
        for category, algorithms in categories.items():
            # Category header
            cat_frame = ttk.LabelFrame(sidebar, text=category, padding=5)
            cat_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Algorithm buttons
            for algo in algorithms:
                btn = ttk.Button(
                    cat_frame, 
                    text=algo,
                    command=lambda a=algo: self.select_algorithm(a)
                )
                btn.pack(fill=tk.X, pady=2)
    
    def create_work_area(self, parent):
        work_frame = ttk.Frame(parent, relief=tk.RIDGE, borderwidth=2)
        work_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        work_frame.columnconfigure(0, weight=1)
        work_frame.rowconfigure(1, weight=1)
        
        # Header
        header = ttk.Label(
            work_frame, 
            text="Select an Algorithm to Begin",
            font=('Arial', 14, 'bold')
        )
        header.grid(row=0, column=0, pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(work_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        
        # Data tab
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data")
        self.create_data_tab()
        
        # Parameters tab
        self.params_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.params_frame, text="Parameters")
        self.create_params_tab()
        
        # Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        self.create_results_tab()
        
        # Visualization tab
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Visualization")
        self.create_viz_tab()
    
    def create_data_tab(self):
        # Data info
        info_label = ttk.Label(
            self.data_frame,
            text="Load your dataset to begin analysis",
            font=('Arial', 10)
        )
        info_label.pack(pady=20)
        
        # Load button
        load_btn = ttk.Button(
            self.data_frame,
            text="Load Dataset",
            command=self.load_dataset
        )
        load_btn.pack(pady=10)
        
        # Data preview area
        preview_frame = ttk.LabelFrame(self.data_frame, text="Data Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable text widget
        scroll_y = ttk.Scrollbar(preview_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.data_text = tk.Text(
            preview_frame,
            wrap=tk.NONE,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        scroll_y.config(command=self.data_text.yview)
        scroll_x.config(command=self.data_text.xview)
    
    def create_params_tab(self):
        # Parameters will be dynamically created based on selected algorithm
        self.params_container = ttk.Frame(self.params_frame, padding=20)
        self.params_container.pack(fill=tk.BOTH, expand=True)
        
        default_label = ttk.Label(
            self.params_container,
            text="Select an algorithm to configure parameters",
            font=('Arial', 10)
        )
        default_label.pack(pady=20)
        
        # Run button
        self.run_btn = ttk.Button(
            self.params_frame,
            text="Run Algorithm",
            command=self.run_algorithm,
            state=tk.DISABLED
        )
        self.run_btn.pack(pady=10)
    
    def create_results_tab(self):
        results_container = ttk.Frame(self.results_frame, padding=10)
        results_container.pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        scroll_y = ttk.Scrollbar(results_container)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(
            results_container,
            wrap=tk.WORD,
            yscrollcommand=scroll_y.set,
            height=20
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.results_text.yview)
        
        self.results_text.insert('1.0', "Results will appear here after running an algorithm")
    
    def create_viz_tab(self):
        viz_container = ttk.Frame(self.viz_frame, padding=10)
        viz_container.pack(fill=tk.BOTH, expand=True)
        
        viz_label = ttk.Label(
            viz_container,
            text="Visualization area\n(Will integrate with matplotlib/plotly)",
            font=('Arial', 10)
        )
        viz_label.pack(pady=20)
    
    def create_status_bar(self, parent):
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.time_label = ttk.Label(status_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.time_label.pack(side=tk.RIGHT)
    
    def select_algorithm(self, algo_name):
        self.current_algorithm = algo_name
        self.status_label.config(text=f"Selected: {algo_name}")
        
        # Clear and update parameters tab
        for widget in self.params_container.winfo_children():
            widget.destroy()
        
        title = ttk.Label(
            self.params_container,
            text=f"{algo_name} Parameters",
            font=('Arial', 12, 'bold')
        )
        title.pack(pady=10)
        
        # Add placeholder parameters (these will be algorithm-specific)
        param_frame = ttk.Frame(self.params_container)
        param_frame.pack(pady=10)
        
        ttk.Label(param_frame, text="Parameters will be added here").grid(row=0, column=0)
        
        self.run_btn.config(state=tk.NORMAL)
        
        # Switch to parameters tab
        self.notebook.select(self.params_frame)
    
    def load_dataset(self):
        filename = filedialog.askopenfilename(
            title="Select Dataset",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.status_label.config(text=f"Loaded: {os.path.basename(filename)}")
            self.data_text.delete('1.0', tk.END)
            self.data_text.insert('1.0', f"Dataset loaded from:\n{filename}\n\n")
            self.data_text.insert(tk.END, "Dataset preview will appear here...")
            messagebox.showinfo("Success", "Dataset loaded successfully!")
    
    def save_results(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(self.results_text.get('1.0', tk.END))
            messagebox.showinfo("Success", "Results saved successfully!")
    
    def run_algorithm(self):
        if hasattr(self, 'current_algorithm'):
            self.status_label.config(text=f"Running {self.current_algorithm}...")
            self.results_text.delete('1.0', tk.END)
            
            result = f"""
Algorithm: {self.current_algorithm}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Status: Ready for implementation
This is a placeholder for actual ML algorithm execution.

Next steps:
1. Integrate scikit-learn for ML algorithms
2. Add numpy/pandas for data processing
3. Implement matplotlib/plotly for visualization
4. Add model evaluation metrics
"""
            self.results_text.insert('1.0', result)
            self.notebook.select(self.results_frame)
            self.status_label.config(text=f"Completed: {self.current_algorithm}")
            messagebox.showinfo("Complete", f"{self.current_algorithm} executed successfully!")
    
    def show_about(self):
        about_text = """
ML Algorithms Platform
Version 1.0

A cross-platform desktop application for machine learning algorithms.

Built with Python and Tkinter
Compatible with Windows, macOS, and Linux
"""
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    app = MLAlgorithmsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()