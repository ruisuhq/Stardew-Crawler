from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, ttk
from App import load_crops, filter_crops, calculate_costs_and_profits
from stardew_saves import get_saves_data
from StardewWikiCrawler import StardewCrawler
import requests
from PIL import Image
from io import BytesIO

# Function to select a game save
def select_game(save_data, selection_window):
    try:
        # Close the game selection window
        selection_window.destroy()
        # Start the main window
        start_main_window(save_data)
    except Exception as e:
        # Handle errors
        messagebox.showerror("Error", f"Unable to process the game save.\nDetails: {e}")
    
def Gamesave_window():
    # Retrieve game saves data
    saves_data = get_saves_data()
    if not saves_data:
        messagebox.showerror("Error", "No saved games found.")
        return

    # Create the main selection window
    selection_window = tk.Tk()
    selection_window.title("Stardew Crawler: Load Game")
    selection_window.geometry("720x250")
    selection_window.resizable(False, False)  # Disable resizing
    selection_window.configure(bg="#f0d29a")

    # Load the Stardew Valley font
    try:
        stardew_font = "StardewValley"
    except:
        messagebox.showwarning(
            "Warning",
            "Stardew Valley font not found. A default font will be used."
        )
        stardew_font = "Arial"

    # Title label
    title_label = tk.Label(
        selection_window,
        text="LOAD GAME SAVE",
        font=(stardew_font, 25),
        bg="#f0d29a",
        fg="#8b4513",
    )
    title_label.pack(pady=5)

    # Scrollable container
    scroll_frame = ttk.Frame(selection_window)
    scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(scroll_frame, bg="#f5deb3", relief="solid")
    scroll_y = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    # Create buttons for each save in a grid
    columns = 3  # Number of columns in the grid
    for index, save in enumerate(saves_data):
        row = index // columns
        col = index % columns
        save_button = tk.Button(
            scrollable_frame,
            text=f"{save['name']}\nFarm: {save['farm']}\nDate: {save['day_month']} of {save['current_season']}, Year {save['year']}",
            font=(stardew_font, 15),
            bg="#d6b86a",
            fg="#8b4513",
            activebackground="#caa259",
            activeforeground="#f0d29a",
            command=lambda s=save: select_game(s, selection_window),
            wraplength=250,  # For long text
        )
        save_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
    # Configure columns to equalize width
    for col in range(columns):
        scrollable_frame.grid_columnconfigure(col, weight=1)

    selection_window.mainloop()

def start_main_window(save_data):
    # Load initial data
    try:
        crops = load_crops("cultivos.json")
    except Exception as e:
        messagebox.showinfo(
            "Error",
            f"{e}\nStarting web crawler for the first time."
        )
        StardewCrawler()
        messagebox.showinfo("Update", "Data updated successfully.")

    # Calculate remaining days in the season
    remaining_days = 28 - int(save_data["day_month"])

    # Validate crops
    valid_crops = []
    for crop in crops:
        try:
            valid_crops.append(crop)
        except Exception as e:
            print(f"Invalid crop ignored: {crop}, error: {e}")

    # Filter available crops
    available_crops = filter_crops(crops, save_data["current_season"], remaining_days)
    selected_crop = None

    # Initialize the main window
    main_window = tk.Tk()
    main_window.title("Stardew Crawler: Calculator")
    main_window.geometry("900x500")
    main_window.resizable(False, False)  # Disable resizing

    # Load the Stardew Valley font
    try:
        stardew_font = "StardewValley"
    except:
        messagebox.showwarning(
            "Warning",
            "Stardew Valley font not found. A default font will be used."
        )
        stardew_font = "Arial"

    # Header section
    header_frame = tk.Frame(main_window, bg="#cd853f", height=50, relief="raised", bd=4)
    header_frame.pack(fill=tk.X)
    title_label = tk.Label(
        header_frame,
        text=f"STARDEW CRAWLER - {save_data['name']} ({save_data['farm']})",
        font=(stardew_font, 25),
        bg="#cd853f",
        fg="#8b4513",
    )
    title_label.pack(pady=10)

    # Load and display background image
    response = requests.get("https://wallpapers.com/images/hd/2d-stardew-valley-mountains-and-sky-bxdaa0lic9b5coki.jpg")
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        background_image = Image.open(image_data)
        bg_image = ImageTk.PhotoImage(background_image.resize((900, 500)))
    bg_image = ImageTk.PhotoImage(background_image.resize((900, 500)))

    background_canvas = tk.Canvas(main_window, width=900, height=500)
    background_canvas.pack(fill="both", expand=True)
    background_canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # Main container
    main_frame = ttk.Frame(background_canvas, style="Card.TFrame", padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=400)

    # Layout configuration
    selection_frame = ttk.Frame(main_frame)
    actions_frame = ttk.Frame(main_frame)
    results_frame = ttk.Frame(main_frame)

    selection_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    actions_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    results_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    main_frame.grid_columnconfigure(0, weight=2)
    main_frame.grid_columnconfigure(1, weight=1)

    # --- "Select Crop" Section ---
    selection_label = tk.Label(
        selection_frame,
        text="Select Crop",
        font=(stardew_font, 20),
        bg="#d6b86a",
        fg="#8b4513",
        relief="solid",
        bd=2,
    )
    selection_label.pack(fill=tk.X, pady=5)

    # Scrollable container for crop buttons
    canvas = tk.Canvas(
        selection_frame,
        bg="#f5deb3",
        bd=2,
        width=400,  # Width in pixels
        height=200,  # Height in pixels
        relief="solid"
    )
    scroll_y = ttk.Scrollbar(selection_frame, orient="vertical", command=canvas.yview)
    crop_frame = ttk.Frame(canvas)

    crop_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=crop_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    selected_button = None  # To keep track of the currently selected button

    def select_crop(crop, button):
        nonlocal selected_crop, selected_button

        # Reset the style of the previously selected button
        if selected_button:
            selected_button.config(
                font=(stardew_font, 15),
                bg="#d6b86a",
                fg="#8b4513",
            )

        # Update the style of the newly selected button
        button.config(
            font=(stardew_font, 15),
            bg="#b56426",
            fg="#f5deb3",
        )

        # Update references
        selected_crop = crop
        selected_button = button

    # Helper function to create buttons
    def create_crop_button(crop, row, col):
        button = tk.Button(
            crop_frame,
            text=f"{crop['name']}\n{crop['sell_price']} - {crop['growth_time']}",
            font=(stardew_font, 15),
            bg="#d6b86a",
            fg="#8b4513",
            relief="solid",
            command=lambda: select_crop(crop, button),  # Pass the button itself
            wraplength=150,
        )
        button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        return button

    # Create crop buttons
    columns = 4  # Number of columns in the grid
    for index, crop in enumerate(available_crops):
        row = index // columns  # Current row
        col = index % columns  # Current column
        create_crop_button(crop, row, col)


    for col in range(columns):
        crop_frame.grid_columnconfigure(col, weight=1)

        # --- "Actions" Section ---
    actions_label = tk.Label(
        actions_frame,
        text="Actions",
        font=(stardew_font, 20),
        bg="#d6b86a",
        fg="#8b4513",
        relief="solid",
        bd=2,
    )
    actions_label.pack(fill=tk.X, pady=5)

    # Function to calculate results
    def calculate_results():
        if not selected_crop:
            messagebox.showwarning("Warning", "Please select a crop first.")
            return

        # Create a custom popup window
        popup_window = tk.Toplevel()
        popup_window.title("Calculate")
        popup_window.geometry("400x300")
        popup_window.configure(bg="#d6b86a")
        popup_window.resizable(False, False)

        # Header for the popup
        header_frame = tk.Frame(popup_window, bg="#cd853f", height=50, relief="raised", bd=4)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(
            header_frame,
            text="Calculate",
            font=(stardew_font, 20),
            bg="#cd853f",
            fg="#8b4513",
        )
        header_label.pack(pady=10)

        # Description
        description_label = tk.Label(
            popup_window,
            text=f"Enter the number of {selected_crop['name']} crops you want to plant.",
            font=(stardew_font, 15),
            bg="#f5deb3",
            fg="#8b4513",
            wraplength=350,
        )
        description_label.pack(pady=10)

        # Input field for crop quantity
        quantity_entry = tk.Entry(
            popup_window,
            font=(stardew_font, 20),
            justify="center",
            bg="white",
            fg="#8b4513",
            relief="solid",
            bd=2,
            
        )
        quantity_entry.pack(pady=10)

        # Confirm button
        def confirm():
            try:
                tiles = int(quantity_entry.get())
                if tiles <= 0:
                    raise ValueError("The number must be greater than zero.")

                # Calculate results
                total_cost, total_profit, net_profit = calculate_costs_and_profits(
                    selected_crop, tiles, remaining_days
                )
                results_label.config(
                    text=f"Results for: {selected_crop['name']}\n"
                         f"Total Costs: {total_cost}g\n"
                         f"Total Profits: {total_profit}g\n"
                         f"Net Profits: {net_profit}g"
                )
                popup_window.destroy()
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Please enter a valid number of crops.",
                )

        confirm_button = tk.Button(
            popup_window,
            text="Confirm",
            font=(stardew_font, 20),
            bg="#f5deb3",
            fg="#8b4513",
            relief="raised",
            command=confirm,
        )
        confirm_button.pack(pady=10)

        popup_window.transient()  # Keep the popup on top
        popup_window.grab_set()  # Disable interaction with the main window
        popup_window.mainloop()

    # Button to trigger calculation
    calculate_button = tk.Button(
        actions_frame,
        text="Calculate",
        font=(stardew_font, 15),
        bg="#f5deb3",
        fg="#8b4513",
        relief="raised",
        command=calculate_results,
    )
    calculate_button.pack(fill=tk.X, pady=10)

        # Function to run the web crawler
    def run_crawler():
        StardewCrawler()
        messagebox.showinfo("Update", "Data updated successfully.")
        
        nonlocal available_crops, selected_button, selected_crop

        # Clear selection references as buttons will be recreated
        selected_button = None
        selected_crop = None

        # Update available crops
        available_crops = filter_crops(crops, save_data["current_season"], remaining_days)

        # Refresh crop selection buttons
        for widget in crop_frame.winfo_children():
            widget.destroy()

        # Create new buttons
        for index, crop in enumerate(available_crops):
            row = index // columns  # Current row
            col = index % columns  # Current column
            create_crop_button(crop, row, col)

        # Reconfigure grid columns
        for col in range(columns):
            crop_frame.grid_columnconfigure(col, weight=1)


    # Button to execute the web crawler
    crawler_button = tk.Button(
        actions_frame,
        text="Run WebCrawler",
        font=(stardew_font, 15),
        bg="#f5deb3",
        fg="#8b4513",
        relief="raised",
        command=run_crawler,
    )
    crawler_button.pack(fill=tk.X, pady=10)

    # # Button to execute the web crawler
    # Change_save = tk.Button(
    #     actions_frame,
    #     text="Change Game Save",
    #     font=(stardew_font, 15),
    #     bg="#f5deb3",
    #     fg="#8b4513",
    #     relief="raised",
    #     command=change_save(main_window),
    # )
    # Change_save.pack(fill=tk.X, pady=10)

        # --- "Results" Section ---
    results_label = tk.Label(
        results_frame,
        text=f"Results:\n"
             f"Total Costs: 0g\n"
             f"Total Profits: 0g\n"
             f"Net Profits: 0g",
        font=(stardew_font, 20),
        bg="#d6b86a",
        fg="#8b4513",
        relief="solid",
        bd=2,
    )
    results_label.pack(fill=tk.X, pady=5)

    main_window.mainloop()