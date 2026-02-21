import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from temperature_scraper import TemperatureScraper
import pandas as pd
from datetime import datetime

class TemperatureDashboard:
    """GUI Dashboard for temperature data"""

    def __init__(self, root):
        self.root = root
        self.root.title("Indian Cities Temperature Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        self.scraper = TemperatureScraper()
        self.data_df = None

        self._create_widgets()
        self._apply_styles()

    def _apply_styles(self):
        """Apply custom styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10), background="#f0f0f0")
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), background="#f0f0f0")
        style.configure('Treeview', font=('Courier', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))

    def _create_widgets(self):
        """Create dashboard widgets"""

        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(header_frame, text="🌡️ Indian Cities Temperature Dashboard", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)

        # Control Panel
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.fetch_button = ttk.Button(control_frame, text="Fetch Temperature Data", command=self._fetch_data_thread)
        self.fetch_button.pack(side=tk.LEFT, padx=5)

        self.export_csv_button = ttk.Button(control_frame, text="Export to CSV", command=self._export_csv, state=tk.DISABLED)
        self.export_csv_button.pack(side=tk.LEFT, padx=5)

        self.export_json_button = ttk.Button(control_frame, text="Export to JSON", command=self._export_json, state=tk.DISABLED)
        self.export_json_button.pack(side=tk.LEFT, padx=5)

        self.refresh_label = ttk.Label(control_frame, text="")
        self.refresh_label.pack(side=tk.RIGHT, padx=5)

        # Status Label
        self.status_label = ttk.Label(self.root, text="Ready to fetch data", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: Data Table
        self.table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="Temperature Data")
        self._create_table_tab()

        # Tab 2: Summary
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Summary")
        self._create_summary_tab()

        # Tab 3: Logs
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Logs")
        self._create_log_tab()

    def _create_table_tab(self):
        """Create data table tab"""
        # Treeview for data display
        columns = ('City', 'Min Temp', 'Max Temp', 'Condition', 'Humidity', 'Wind Speed')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, height=20, show='headings')

        # Define column headings and widths
        self.tree.column('City', width=120)
        self.tree.column('Min Temp', width=100)
        self.tree.column('Max Temp', width=100)
        self.tree.column('Condition', width=150)
        self.tree.column('Humidity', width=100)
        self.tree.column('Wind Speed', width=100)

        for col in columns:
            self.tree.heading(col, text=col)

        # Scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def _create_summary_tab(self):
        """Create summary statistics tab"""
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame, wrap=tk.WORD, font=('Courier', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.summary_text.config(state=tk.DISABLED)

    def _create_log_tab(self):
        """Create logs tab"""
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, font=('Courier', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

    def _log_message(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _fetch_data_thread(self):
        """Fetch data in a separate thread to prevent UI freeze"""
        self.fetch_button.config(state=tk.DISABLED)
        self.status_label.config(text="Fetching data...")
        self.root.update()

        thread = threading.Thread(target=self._fetch_data)
        thread.daemon = True
        thread.start()

    def _fetch_data(self):
        """Fetch temperature data"""
        try:
            self._log_message("Starting data fetch...")

            # Scrape data
            self.scraper.scrape_weather_data()
            self.data_df = pd.DataFrame(self.scraper.temperature_data)

            self._log_message(f"Successfully fetched data for {len(self.data_df)} cities")

            # Update table
            self._update_table()

            # Update summary
            self._update_summary()

            # Enable export buttons
            self.export_csv_button.config(state=tk.NORMAL)
            self.export_json_button.config(state=tk.NORMAL)

            self.status_label.config(text=f"✓ Data fetched successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._log_message("Data fetch completed successfully")

            self.refresh_label.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            self._log_message(f"Error: {str(e)}")
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to fetch data:\n{str(e)}")

        finally:
            self.fetch_button.config(state=tk.NORMAL)

    def _update_table(self):
        """Update treeview with data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.data_df is None:
            return

        # Sort by max temperature
        df = self.data_df.sort_values('Max Temp (°C)', ascending=False)

        # Add items
        for idx, row in df.iterrows():
            values = (
                row['City'],
                f"{row['Min Temp (°C)']}°C",
                f"{row['Max Temp (°C)']}°C",
                row['Current Condition'],
                f"{row['Humidity (%)']}%",
                f"{row['Wind Speed (km/h)']} km/h"
            )
            self.tree.insert('', tk.END, values=values)

    def _update_summary(self):
        """Update summary statistics"""
        if self.data_df is None:
            return

        df = self.data_df

        summary_text = f"""
{'='*60}
TEMPERATURE SUMMARY STATISTICS
{'='*60}

Total Cities: {len(df)}
Average Max Temperature: {df['Max Temp (°C)'].mean():.1f}°C
Average Min Temperature: {df['Min Temp (°C)'].mean():.1f}°C

Hottest City: {df.loc[df['Max Temp (°C)'].idxmax(), 'City']} ({df['Max Temp (°C)'].max()}°C)
Coldest City: {df.loc[df['Min Temp (°C)'].idxmin(), 'City']} ({df['Min Temp (°C)'].min()}°C)

Temperature Range: {df['Min Temp (°C)'].min()}°C to {df['Max Temp (°C)'].max()}°C

{'='*60}
TOP 5 HOTTEST CITIES:
{'='*60}
"""

        top_hot = df.nlargest(5, 'Max Temp (°C)')
        for idx, (_, row) in enumerate(top_hot.iterrows(), 1):
            summary_text += f"\n{idx}. {row['City']:<20} Max: {row['Max Temp (°C)']:>6.1f}°C | Min: {row['Min Temp (°C)']:>6.1f}°C"

        summary_text += f"\n\n{'='*60}\nTOP 5 COLDEST CITIES:\n{'='*60}\n"

        top_cold = df.nsmallest(5, 'Min Temp (°C)')
        for idx, (_, row) in enumerate(top_cold.iterrows(), 1):
            summary_text += f"\n{idx}. {row['City']:<20} Min: {row['Min Temp (°C)']:>6.1f}°C | Max: {row['Max Temp (°C)']:>6.1f}°C"

        summary_text += f"\n\n{'='*60}\nAVERAGE HUMIDITY BY CONDITION:\n{'='*60}\n"
        avg_humidity = df.groupby('Current Condition')['Humidity (%)'].mean().sort_values(ascending=False)
        for condition, humidity in avg_humidity.items():
            summary_text += f"\n{condition:<30} {humidity:>6.1f}%"

        summary_text += f"\n\n{'='*60}"

        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert('1.0', summary_text)
        self.summary_text.config(state=tk.DISABLED)

    def _export_csv(self):
        """Export data to CSV"""
        if self.data_df is None:
            messagebox.showwarning("Warning", "No data to export. Please fetch data first.")
            return

        try:
            self.scraper.save_to_csv()
            self._log_message("Data exported to CSV successfully")
            messagebox.showinfo("Success", "Data exported to CSV successfully")
        except Exception as e:
            self._log_message(f"Error exporting to CSV: {str(e)}")
            messagebox.showerror("Error", f"Failed to export to CSV:\n{str(e)}")

    def _export_json(self):
        """Export data to JSON"""
        if self.data_df is None:
            messagebox.showwarning("Warning", "No data to export. Please fetch data first.")
            return

        try:
            self.scraper.save_to_json()
            self._log_message("Data exported to JSON successfully")
            messagebox.showinfo("Success", "Data exported to JSON successfully")
        except Exception as e:
            self._log_message(f"Error exporting to JSON: {str(e)}")
            messagebox.showerror("Error", f"Failed to export to JSON:\n{str(e)}")


def main():
    """Main function to run the dashboard"""
    root = tk.Tk()
    dashboard = TemperatureDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()

