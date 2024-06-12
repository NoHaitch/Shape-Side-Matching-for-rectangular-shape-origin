import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import time
from dataset import Dataset
from shapeMatching import ShapeMatching


class ShapeMatchingGUI:
    """
    Class to create the GUI for the Shape Side Matching application
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Shape Side Matching")
        self.root.geometry("1200x600")

        # Title label
        self.title_label = tk.Label(root, text="Shape Side Matching", font=("Helvetica", 20))
        self.title_label.place(relx=0.5, rely=0.05, anchor="n")

        # Create widgets
        self.label = tk.Label(root, text="Select a shape (.png):", font=("Helvetica", 14))
        self.label.place(relx=0.5, rely=0.15, anchor="center")

        self.select_button = tk.Button(root, text="Select Shape", command=self.select_image, font=("Helvetica", 14))
        self.select_button.place(relx=0.5, rely=0.2, anchor="center")

        # Side selection dropdown
        self.side_var = tk.StringVar()
        self.side_var.set("right")
        self.side_combobox = ttk.Combobox(root, textvariable=self.side_var, values=["left", "right", "top", "bottom"],
                                          state="readonly", font=("Helvetica", 14))
        self.side_combobox.place(relx=0.5, rely=0.25, anchor="center")

        self.search_frame = tk.Frame(root)
        self.search_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.kmp_search_button = tk.Button(self.search_frame, text="KMP Search", command=self.kmp_search,
                                           font=("Helvetica", 14))
        self.kmp_search_button.grid(row=0, column=0, padx=5)

        self.bm_search_button = tk.Button(self.search_frame, text="BM Search", command=self.bm_search,
                                          font=("Helvetica", 14))
        self.bm_search_button.grid(row=0, column=1, padx=5)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.place(relx=0.5, rely=0.35, anchor="center")

        # Image labels
        self.original_image_label = tk.Label(root)
        self.original_image_label.place(relx=0.25, rely=0.6, anchor="center")

        self.result_image_label = tk.Label(root)
        self.result_image_label.place(relx=0.75, rely=0.6, anchor="center")

        # Time labels
        self.shape_matching_time_label = tk.Label(root, text="Shape Matching Time: N/A", font=("Helvetica", 14))
        self.shape_matching_time_label.place(relx=0.5, rely=0.85, anchor="center")

        # Variables to store times
        self.dataset_conversion_time = 0
        self.shape_matching_time = 0

        # Variable to store algorithm name
        self.algorithm_name = ""

    def select_image(self):
        """
        Open a file dialog to select an image
        """
        self.filename = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])

        # Display selected image
        self.image = Image.open(self.filename)
        self.image.thumbnail((300, 300))  # Resize image for display
        self.photo = ImageTk.PhotoImage(self.image)
        self.original_image_label.config(image=self.photo)

    def kmp_search(self):
        """
        Perform shape matching using the KMP algorithm
        """
        if hasattr(self, 'filename'):
            dataset_start_time = time.time()
            dataset_pattern = Dataset.get_folder_ascii_pattern("dataset", exclude_folder=self.filename)
            dataset_end_time = time.time()
            self.dataset_conversion_time = dataset_end_time - dataset_start_time

            shape_matching_start_time = time.time()
            result = ShapeMatching.shape_match_kmp(self.filename, self.side_var.get(), dataset_pattern)
            shape_matching_end_time = time.time()
            self.shape_matching_time = shape_matching_end_time - shape_matching_start_time

            self.algorithm_name = "KMP"

            # Display best match image
            best_matched_image_path = "dataset\\" + result.split('/')[0]
            best_match_image = Image.open(best_matched_image_path)
            best_match_image.thumbnail((300, 300))
            best_match_photo = ImageTk.PhotoImage(best_match_image)
            self.result_image_label.config(image=best_match_photo)
            self.result_image_label.image = best_match_photo  # Keep a reference to avoid garbage collection

            # Update result label
            self.result_label.config(text=f"Best match: {result.split('/')[0]}\nAlgorithm used: "
                                          f"{self.algorithm_name}\nSide used: {result.split('/')[1]}")

            # Update time labels
            self.shape_matching_time_label.config(text=f"Shape Matching Time: {self.shape_matching_time:.4f} seconds")
        else:
            self.result_label.config(text="Please select a shape first.")

    def bm_search(self):
        """
        Perform shape matching using the BM algorithm
        """
        if hasattr(self, 'filename'):
            dataset_start_time = time.time()
            dataset_pattern = Dataset.get_folder_ascii_pattern("dataset", exclude_folder=self.filename)
            dataset_end_time = time.time()
            self.dataset_conversion_time = dataset_end_time - dataset_start_time

            shape_matching_start_time = time.time()
            result = ShapeMatching.shape_match_bm(self.filename, self.side_var.get(), dataset_pattern)
            shape_matching_end_time = time.time()
            self.shape_matching_time = shape_matching_end_time - shape_matching_start_time

            self.algorithm_name = "BM"

            # Display best match image
            best_matched_image_path = "dataset\\" + result.split('/')[0]
            best_match_image = Image.open(best_matched_image_path)
            best_match_image.thumbnail((300, 300))
            best_match_photo = ImageTk.PhotoImage(best_match_image)
            self.result_image_label.config(image=best_match_photo)
            self.result_image_label.image = best_match_photo  # Keep a reference to avoid garbage collection

            # Update result label
            self.result_label.config(text=f"Best match: {result.split('/')[0]}\nAlgorithm used: "
                                          f"{self.algorithm_name}\nSide used: {result.split('/')[1]}")

            # Update time labels
            self.shape_matching_time_label.config(text=f"Shape Matching Time: {self.shape_matching_time:.4f} seconds")
        else:
            self.result_label.config(text="Please select a shape first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeMatchingGUI(root)
    root.mainloop()
