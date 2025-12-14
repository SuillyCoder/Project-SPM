import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ============================================================================
# IMPORT FUNCTIONS FROM YOUR EXISTING FILES
# ============================================================================
try:
    from DataProcessing import read_csv_columns
    from ExtrapolationAndError import lagrange_interpolation, relative_error
except ImportError:
    print("Warning: Could not import from DataProcessing.py or ExtrapolationAndError.py")
    print("Make sure these files are in the same directory as this script.")
    
    # Fallback functions if import fails
    def read_csv_columns(filename):
        col1 = []
        col2 = []
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            first_row = next(reader)
            try:
                float(first_row[0])
                col1.append(float(first_row[0]))
                col2.append(float(first_row[1]))
            except ValueError:
                pass
            for row in reader:
                if len(row) >= 2:
                    col1.append(float(row[0]))
                    col2.append(float(row[1]))
        return col1, col2
    
    def lagrange_interpolation(x_points, y_points, x):
        n = len(x_points)
        total = 0.0
        for i in range(n):
            Li = 1.0
            for j in range(n):
                if i != j:
                    Li *= (x - x_points[j]) / (x_points[i] - x_points[j])
            total += y_points[i] * Li
        return total
    
    def relative_error(true_value, approx_value):
        return abs(true_value - approx_value) / abs(true_value)

def get_rating(accuracy):
    """Determine rating based on accuracy percentage"""
    if accuracy >= 90:
        return "OUTSTANDING"
    elif accuracy >= 75:
        return "GREAT"
    elif accuracy >= 50:
        return "AVERAGE"
    elif accuracy >= 30:
        return "NEEDS IMPROVEMENT"
    else:
        return "POOR"

# ============================================================================
# CSV VALIDATION
# ============================================================================

def validate_csv(file_path):
    """Validate CSV file before processing"""
    # Check if file exists
    if not os.path.isfile(file_path):
        return False, "File does not exist"
    
    # Check file extension
    if not file_path.lower().endswith('.csv'):
        return False, "Invalid File Type"
    
    # Check if file is empty or has insufficient rows
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if len(rows) == 0 or all(all(cell.strip() == ' ' for cell in row) for row in rows):
                return False, "Empty CSV File. Cannot be used!"
            
            # Check if first row is header
            data_rows = rows
            try:
                float(rows[0][0])
            except (ValueError, IndexError):
                data_rows = rows[1:]  # Skip header
            
            if len(data_rows) < 5:
                return False, "Insufficient Rows. Invalid CSV"
            
            # Check if rows have at least 2 columns
            for row in data_rows:
                if len(row) < 2:
                    return False, "CSV must have at least 2 columns"
        
        return True, "Valid CSV"
    
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

# ============================================================================
# RESULTS WINDOW
# ============================================================================

def show_results_window(file_path, filename):
    """Display comprehensive results window"""
    
    # Read CSV data
    rounds, distances = read_csv_columns(file_path)
    n = len(rounds)
    
    # State variable for number of data points to use
    num_data_points = [min(3, n)]  # Default to 3 (or less if not enough data)
    
    TRUE_VALUE = 5.0
    
    def calculate_predictions(num_points):
        """Calculate predictions based on selected number of data points"""
        # Use the last N data points
        use_n = min(num_points, n)
        x_points = list(range(1, use_n + 1))
        y_points = distances[-use_n:]
        
        predictions = []
        for j in range(3):
            x_test = use_n + j + 1
            approx = lagrange_interpolation(x_points, y_points, x_test)
            
            # Manipulate if over 5
            if approx > 5:
                approx = 10 - approx
            
            rel_err = relative_error(TRUE_VALUE, approx)
            pred_accuracy = (1 - rel_err) * 100
            
            predictions.append({
                'round': int(rounds[-1]) + j + 1,
                'distance': approx,
                'accuracy': pred_accuracy
            })
        
        return predictions
    
    # Calculate initial predictions
    predictions = [calculate_predictions(num_data_points[0])]
    
    # Calculate accuracy for each round (using all data)
    x_points = list(range(1, n + 1))
    y_points = distances
    
    accuracies = []
    errors = []
    
    for i in range(n):
        x_test = i + 1
        approx = lagrange_interpolation(x_points, y_points, x_test)
        rel_err = relative_error(TRUE_VALUE, approx)
        accuracy = (1 - rel_err) * 100
        
        accuracies.append(accuracy)
        errors.append(rel_err)
    
    # Calculate average accuracy
    avg_accuracy = sum(accuracies) / len(accuracies)
    rating = get_rating(avg_accuracy)
    
    # Create results window
    results_window = tk.Toplevel()
    results_window.title("Project S.P.M - Results Dashboard")
    results_window.geometry("1200x750")
    results_window.configure(bg='#f0f0f0')
    
    # UPPER PART - CSV Filename
    header_frame = tk.Frame(results_window, bg='#2c3e50', height=60)
    header_frame.pack(fill='x', padx=10, pady=10)
    
    tk.Label(header_frame, text=filename, 
             font=('Arial', 20, 'bold'), 
             fg='white', bg='#2c3e50').pack(pady=10)
    
    # MAIN CONTENT FRAME
    content_frame = tk.Frame(results_window, bg='#f0f0f0')
    content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # ========================================================================
    # LEFT PART - ACCURACY READINGS
    # ========================================================================
    left_frame = tk.Frame(content_frame, bg='white', relief='raised', borderwidth=2)
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
    
    tk.Label(left_frame, text="ACCURACY READINGS", 
             font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
    
    # Scrollable frame for accuracy data
    scroll_container = tk.Frame(left_frame, bg='white')
    scroll_container.pack(fill='both', expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(scroll_container, bg='#e8f4f8', highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#e8f4f8')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Add data rows
    for i in range(n):
        row_frame = tk.Frame(scrollable_frame, bg='#e8f4f8', pady=5)
        row_frame.pack(fill='x', padx=10)
        
        tk.Label(row_frame, text=f"Round {int(rounds[i])}: {accuracies[i]:.1f}%", 
                 font=('Arial', 12, 'bold'), 
                 bg='#e8f4f8', anchor='w', width=25).pack(side='left', padx=5)
        
        tk.Label(row_frame, text=f"Error: {errors[i]:.3f}", 
                 font=('Arial', 10), 
                 bg='#e8f4f8', fg='gray').pack(side='left', padx=5)
    
    # Summary section
    summary_frame = tk.Frame(left_frame, bg='white', pady=20)
    summary_frame.pack(fill='x', padx=20, pady=10)
    
    tk.Label(summary_frame, text=f"Average Accuracy: {avg_accuracy:.1f}%", 
             font=('Arial', 16, 'bold'), bg='white').pack(pady=5)
    
    # Rating with color
    rating_colors = {
        "OUTSTANDING": "#27ae60",
        "GREAT": "#2ecc71",
        "AVERAGE": "#f39c12",
        "NEEDS IMPROVEMENT": "#e67e22",
        "POOR": "#e74c3c"
    }
    
    rating_frame = tk.Frame(summary_frame, bg='white')
    rating_frame.pack(pady=5)
    
    tk.Label(rating_frame, text="Rating: ", 
             font=('Arial', 14), bg='white').pack(side='left')
    tk.Label(rating_frame, text=rating, 
             font=('Arial', 14, 'bold'), 
             fg=rating_colors.get(rating, 'black'), 
             bg='white').pack(side='left')
    
    # ========================================================================
    # RIGHT PART - PERFORMANCE PREDICTIONS
    # ========================================================================
    right_frame = tk.Frame(content_frame, bg='white', relief='raised', borderwidth=2)
    right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
    
    tk.Label(right_frame, text="PERFORMANCE PREDICTIONS", 
             font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
    
    # Graph
    fig = Figure(figsize=(6, 4), dpi=80)
    ax = fig.add_subplot(111)
    
    ax.plot(rounds, distances, marker='o', linestyle='-', 
            color='#3498db', linewidth=2, markersize=6, label='Actual Data')
    
    ax.set_xlabel('Round Number', fontsize=12)
    ax.set_ylabel('Mark Distance', fontsize=12)
    ax.set_title('Shot Performance Over Time', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    canvas_widget = FigureCanvasTkAgg(fig, right_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(padx=10, pady=10)
    
    # Prediction navigation
    prediction_frame = tk.Frame(right_frame, bg='white')
    prediction_frame.pack(pady=20)
    
    current_pred_idx = [0]  # Use list to allow modification in nested function
    
    def update_prediction_display():
        idx = current_pred_idx[0]
        pred = predictions[0][idx]  # predictions[0] because it's recalculated
        
        pred_label.config(text=f"Round {pred['round']} Prediction:")
        distance_label.config(text=f"{pred['distance']:.2f}")
        accuracy_label.config(text=f"{pred['accuracy']:.0f}%")
        
        # Update button states
        prev_btn.config(state='normal' if idx > 0 else 'disabled')
        next_btn.config(state='normal' if idx < len(predictions[0]) - 1 else 'disabled')
    
    def prev_prediction():
        if current_pred_idx[0] > 0:
            current_pred_idx[0] -= 1
            update_prediction_display()
    
    def next_prediction():
        if current_pred_idx[0] < len(predictions[0]) - 1:
            current_pred_idx[0] += 1
            update_prediction_display()
    
    def update_data_points(change):
        """Update number of data points and recalculate predictions"""
        new_value = num_data_points[0] + change
        if 2 <= new_value <= min(5, n):
            num_data_points[0] = new_value
            data_points_label.config(text=str(num_data_points[0]))
            
            # Recalculate predictions
            predictions[0] = calculate_predictions(num_data_points[0])
            
            # Reset to first prediction and update display
            current_pred_idx[0] = 0
            update_prediction_display()
        
        # Update button states
        decrease_btn.config(state='normal' if num_data_points[0] > 2 else 'disabled')
        increase_btn.config(state='normal' if num_data_points[0] < min(5, n) else 'disabled')
    
    # Navigation buttons
    nav_frame = tk.Frame(prediction_frame, bg='white')
    nav_frame.pack()
    
    prev_btn = tk.Button(nav_frame, text="◀", command=prev_prediction, 
                         font=('Arial', 16), width=3, state='disabled')
    prev_btn.pack(side='left', padx=5)
    
    pred_label = tk.Label(nav_frame, text="", font=('Arial', 14, 'bold'), bg='white')
    pred_label.pack(side='left', padx=20)
    
    next_btn = tk.Button(nav_frame, text="▶", command=next_prediction, 
                         font=('Arial', 16), width=3)
    next_btn.pack(side='left', padx=5)
    
    # Prediction details
    details_frame = tk.Frame(prediction_frame, bg='white', pady=10)
    details_frame.pack()
    
    tk.Label(details_frame, text="Mark Distance:", 
             font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='e', padx=5)
    distance_label = tk.Label(details_frame, text="", 
                              font=('Arial', 12, 'bold'), fg='#e74c3c', bg='white')
    distance_label.grid(row=0, column=1, sticky='w', padx=5)
    
    tk.Label(details_frame, text="Accuracy:", 
             font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='e', padx=5)
    accuracy_label = tk.Label(details_frame, text="", 
                              font=('Arial', 12, 'bold'), fg='#e74c3c', bg='white')
    accuracy_label.grid(row=1, column=1, sticky='w', padx=5)
    
    # Data Points Selector
    data_points_frame = tk.Frame(prediction_frame, bg='white', pady=15)
    data_points_frame.pack()
    
    tk.Label(data_points_frame, text="Data Points for Prediction:", 
             font=('Arial', 11), bg='white').pack()
    
    selector_frame = tk.Frame(data_points_frame, bg='white')
    selector_frame.pack(pady=10)
    
    decrease_btn = tk.Button(selector_frame, text="◀", 
                            command=lambda: update_data_points(-1),
                            font=('Arial', 14), width=3)
    decrease_btn.pack(side='left', padx=5)
    
    data_points_label = tk.Label(selector_frame, text=str(num_data_points[0]),
                                 font=('Arial', 16, 'bold'), bg='white', width=3)
    data_points_label.pack(side='left', padx=10)
    
    increase_btn = tk.Button(selector_frame, text="▶",
                            command=lambda: update_data_points(1),
                            font=('Arial', 14), width=3)
    increase_btn.pack(side='left', padx=5)
    
    tk.Label(data_points_frame, text="(2-5 data points)", 
             font=('Arial', 9, 'italic'), fg='gray', bg='white').pack()
    
    # Initialize button states
    update_data_points(0)
    
    # Initialize display
    update_prediction_display()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def upload_csv():
    """Handle CSV file upload with validation"""
    file_path = filedialog.askopenfilename(
        title="Select Sniper Data CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if file_path:
        filename = os.path.basename(file_path)
        
        # Validate CSV
        is_valid, message = validate_csv(file_path)
        
        if not is_valid:
            messagebox.showerror("Invalid CSV", message)
            return
        
        # Show results window
        show_results_window(file_path, filename)
    else:
        messagebox.showinfo("No File Selected", "No CSV file was selected.")

# Create main window
root = tk.Tk()
root.geometry("800x500")
root.title("Project S.P.M - Sniper Performance Metrics")
root.configure(bg='#ecf0f1')

# Title
title_frame = tk.Frame(root, bg='#34495e', height=100)
title_frame.pack(fill='x', pady=20, padx=20)

tk.Label(title_frame, text="PROJECT S.P.M.", 
         font=('Times New Roman', 36, 'bold'),
         fg='white', bg='#34495e').pack(pady=20)

# Subtitle
tk.Label(root, text="Sniper Performance Metrics", 
         font=('Arial', 16, 'italic'),
         fg='#7f8c8d', bg='#ecf0f1').pack(pady=10)

# Description
desc_frame = tk.Frame(root, bg='white', relief='solid', borderwidth=1)
desc_frame.pack(pady=20, padx=50, fill='x')

desc_text = """
Upload your sniper training CSV file to analyze:
• Shot accuracy and performance metrics
• Round-by-round performance trends
• Predictive analysis for future rounds
"""

tk.Label(desc_frame, text=desc_text, 
         font=('Arial', 11), justify='left',
         bg='white', fg='#2c3e50').pack(pady=15, padx=20)

# Upload Button
upload_button = tk.Button(root, 
                         text="📁 UPLOAD CSV FILE",
                         command=upload_csv,
                         font=('Arial', 14, 'bold'),
                         bg='#27ae60',
                         fg='white',
                         activebackground='#229954',
                         width=25,
                         height=2,
                         cursor='hand2')
upload_button.pack(pady=30)

# Footer
tk.Label(root, text="Developed by Basuil, Esler & Quiel | CPE 3108", 
         font=('Arial', 9, 'italic'),
         fg='#95a5a6', bg='#ecf0f1').pack(side='bottom', pady=10)

root.mainloop()