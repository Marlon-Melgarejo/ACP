import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import messagebox
from groq import Groq
import os
import requests
import folium
from tkinter import Tk, Label, Button, Frame
from tkhtmlview import HTMLLabel
from tkinterweb import HtmlFrame
from geopy.geocoders import Nominatim
import geopy
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import webbrowser
import webview
from tkinter import Frame
from PyQt5 import sip


# Global variable to store chat history
chat_history = []

# Setup the Groq client
client = Groq(api_key="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")

# Function to handle the AI chat response
def get_ai_response(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": user_input,
            }],
            model="llama-3.1-70b-versatile",  # Use your preferred model
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle user submitting the chat message
def send_message(event=None):
    global chat_history
    user_message = user_input.get()
    if user_message:
        # Add the user's message to the chat window
        chat_display.insert(tk.END, f"User(YOU): {user_message}\n")
        chat_history.append(f"User: {user_message}")
        
        # Get AI response
        ai_message = get_ai_response(user_message)
        
        # Add AI's response to the chat window
        chat_display.insert(tk.END, f"B.E.R.M.S.: {ai_message}\n")
        chat_history.append(f"AI: {ai_message}")

        # Scroll to the bottom of the chat
        chat_display.yview(tk.END)

        # Clear the input field
        user_input.delete(0, tk.END)

users_db = {}
def get_barangay_list():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (empty for default)
            database="berms"  # Your database name
        )

        cursor = conn.cursor()

        # Query to fetch barangay names
        cursor.execute("SELECT * FROM barangay")  # Fetch all columns for debugging
        rows = cursor.fetchall()

        # Debug: print the rows to check the data structure
        print("Rows fetched from barangay table:", rows)

        # Assuming the name column is the first one (adjust if necessary)
        barangay_list = [row[1] for row in rows]  # Adjust if the column index is different

        # Close the connection
        conn.close()

        return barangay_list
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    
# Initialize the root window
root = tk.Tk()
root.title("B.E.R.M.S")
root.geometry("510x510")

# Global lists to store frames for animations
bg_frames = []
login_frames = []


# Function to load and animate background GIF
def set_background(gif_path, width, height):
    global bg_frames

    try:
        # Open the GIF file and extract its frames
        bg_image = Image.open(gif_path)
        bg_frames.clear()

        for frame in range(bg_image.n_frames):
            bg_image.seek(frame)
            # Resize each frame
            resized_frame = bg_image.copy().resize((width, height), Image.Resampling.LANCZOS)
            frame_image = ImageTk.PhotoImage(resized_frame)
            bg_frames.append(frame_image)

        # Create a label for the background
        bg_label = tk.Label(root)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Function to animate the background
        def animate_bg(count):
            if bg_frames:  # Ensure frames are available
                bg_label.configure(image=bg_frames[count])
                root.after(40, animate_bg, (count + 1) % len(bg_frames))

        animate_bg(0)

    except Exception as e:
        print(f"Error loading background GIF: {e}")


# Function to show the main menu
def show_main_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Set animated background
    set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif",500,500)

    # Show SIM number and password fields
    tk.Label(root, text="SIM Number (11 digits):", font=("Helvetica", 9),bg="orange").pack(pady=15)
    sim_number_entry = tk.Entry(root)
    sim_number_entry.pack(pady=1)

    tk.Label(root, text="Password (8 characters):", font=("Helvetica", 9),bg="orange").pack(pady=15)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=1)

    # Login button
    def login():
        sim_number = sim_number_entry.get()
        password = password_entry.get()

        if sim_number in users_db and users_db[sim_number]['password'] == password:
            show_login_animation()
        else:
            error_label.config(text="Invalid SIM number or password.", fg="red",)

    # Error label for login
    error_label = tk.Label(root, text="Login or Sign-up",bg="yellow", fg="black")
    error_label.pack(pady=5)

    tk.Button(root, text="LOGIN", command=login,font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(pady=10)

    # Sign Up button
    def go_to_sign_up():
        show_sign_up()

    tk.Button(root, text="SIGN UP", command=go_to_sign_up,font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(pady=10)

    # Exit button
    def exit_program():
        root.quit()

    tk.Button(root, text="EXIT", command=exit_program,font=("Helvetica", 10), bg="red", fg="white").pack(pady=10)

# Function to show sign up form
def show_sign_up():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Set the background GIF (example path) 
    set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif",500,500)  # Ensure you provide the correct path to the GIF file

    # Show the sign-up fields
    tk.Label(root, text="SIM Number (11 digits):", font=("Helvetica", 10), bg="orange").pack(pady=8)
    sim_number_entry = tk.Entry(root)
    sim_number_entry.pack(pady=5)

    tk.Label(root, text="Username:", font=("Helvetica", 10), bg="orange").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Address:", font=("Helvetica", 10), bg="orange").pack(pady=5)

     # Fetch barangay list from the database
    barangay_list = get_barangay_list()

    # Create a Combobox for the Barangay selection
    barangay_combobox = ttk.Combobox(root, values=barangay_list)
    barangay_combobox.pack(pady=5)

    tk.Label(root, text="Hotline (Optional):", font=("Helvetica", 10), bg="orange").pack(pady=5)
    hotline_entry = tk.Entry(root)
    hotline_entry.pack(pady=5)

    tk.Label(root, text="Password (8 characters):", font=("Helvetica", 10), bg="orange").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Label(root, text="Confirm Password:", font=("Helvetica", 10), bg="orange").pack(pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=5)

    # Sign Up button
    def save_user():
        global current_user

        sim_number = sim_number_entry.get()
        username = username_entry.get()
        address = barangay_combobox.get()
        hotline = hotline_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Validate SIM number
        if len(sim_number) != 11 or not sim_number.isdigit():
            error_label.config(text="SIM number must be 11 digits.", bg="yellow", fg="red")
            return

        # Check if password is 8 characters
        if len(password) < 8:
            error_label.config(text="Password must be at least 8 characters.",bg="yellow", fg="red")
            return

        # Check if passwords match
        if password != confirm_password:
            error_label.config(text="Passwords do not match.", bg="yellow",fg="red")
            return

        # Save user to the database
        users_db[sim_number] = {
            'username': username,
            'address': address,
            'hotline': hotline,
            'password': password
        }
        current_user = sim_number

        # Change the window to display login options
        def go_back_to_menu_or_login():
            # Clear the window and show login choices
            for widget in root.winfo_children():
                widget.destroy()
                set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif",500,500)

            tk.Label(root, text="Sign-Up \nSuccessful!", font=("Times New Roman 24 Bold", 40),bg="orange", fg="green").pack(pady=90)
            response = tk.Label(root, text="Do you want to log in now?",bg="orange", fg="white")
            response.pack(pady=15)

            def login_now():
                show_login_animation()
                

            def back_to_menu():
                show_main_menu()

            login_button = tk.Button(root, text="Login Now", command=login_now,font=("Helvetica", 12), bg="#4CAF50", fg="white")
            login_button.pack(pady=5)
            
            back_button = tk.Button(root, text="Back to Menu", command=back_to_menu,font=("Helvetica", 12), bg="#f44336", fg="white")
            back_button.pack(pady=5)

        go_back_to_menu_or_login()

    tk.Button(root, text="Sign Up", command=save_user).pack(pady=5)

    # Back button
    def back_to_main_menu():
        show_main_menu()

    tk.Button(root, text="Back", command=back_to_main_menu).pack(pady=5)

    # Error label for sign-up
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=5)

    # Success label for sign-up
    success_label = tk.Label(root, text="", fg="green")
    success_label.pack(pady=5)

# Function to show "Logging in..." animation with rotating circle
# Global list to store frames and image reference
frames = []

def show_post_login_menu():
    for widget in root.winfo_children():  # Clear the window
        widget.destroy()

    # Set a background
    set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif", 500, 500)

    # Welcome message
    tk.Label(root, text="Welcome to B.E.R.M.S", font=("Helvetica", 16, "bold"), bg="orange").pack(pady=20)

    # Buttons for Emergency Chat, Profile, and Logout
    button_style = {"font": ("Helvetica", 14), "width": 20, "height": 2, "bg": "#4CAF50", "fg": "white"}

    tk.Button(root, text="Emergency Chat", command=show_emergency_chat, **button_style).pack(pady=10)
    tk.Button(root, text="Profile", command=show_profile, **button_style).pack(pady=10)
    tk.Button(root, text="Logout", command=show_logout_animation, **button_style).pack(pady=10)


# Emergency Chat Placeholder
def show_emergency_chat():
    global chat_history
    for widget in root.winfo_children():
        widget.destroy()

        # Set the background GIF (example path)
    set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif",500,500)
    
    tk.Label(root, text="Emergency Chat", font=("Helvetica", 16, "bold"),fg="white",bg="orange").pack(pady=20)
    
    # Create chat display area
    global chat_display
    chat_display = tk.Text(root, height=15, width=80)
    chat_display.pack(padx=10, pady=10)
    chat_display.insert(tk.END, "Welcome! Ask your emergency-related questions...\n")

    for message in chat_history:
        chat_display.insert(tk.END, message + "\n")
    chat_display.yview(tk.END)  # Scroll to the bottom
    
    # Create user input field
    global user_input
    user_input = tk.Entry(root, width=40)
    user_input.pack(padx=10, pady=10)
    
    # Bind the Enter key to send the message
    user_input.bind("<Return>", send_message)  # <Return> is the Enter key

    # Send button
    send_button = tk.Button(root, text="Send", command=send_message,font=("Helvetica", 12), bg="#4CAF50", fg="white")
    send_button.pack(pady=10)
    
    # Back button
    back_button = tk.Button(root, text="Back", command=show_post_login_menu, font=("Helvetica", 12), bg="#f44336", fg="white")
    back_button.pack(pady=10)

# Function to create and save the map
def create_map(latitude, longitude, address):
    map_object = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude], popup=f"You are here: {address}").add_to(map_object)
    map_file = os.path.join(os.getcwd(), "user_map.html")
    map_object.save(map_file)
    return map_file

# Function to create and save the map
def create_map(latitude, longitude, address):
    map_object = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude], popup=f"You are here: {address}").add_to(map_object)
    map_file = os.path.join(os.getcwd(), "user_map.html")
    map_object.save(map_file)
    return map_file

# Function to display map in a separate window using PyQt5
class MapWindow(QMainWindow):
    def __init__(self, map_file):
        super().__init__()
        self.setWindowTitle("Map Location")
        self.setGeometry(100, 100, 800, 600)

        # Create a QWebEngineView widget to display the map
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile(map_file))

        # Set layout for the window
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.web_view)
        self.setCentralWidget(central_widget)

# Global variable to store the QApplication instance
app = None

# Function to show the map window
def show_map_window(map_file):
    global app

    # Check if QApplication instance already exists
    if app is None:
        app = QApplication(sys.argv)  # Create a new QApplication if none exists

    # Create and show the map window
    map_window = MapWindow(map_file)
    map_window.show()

    # Start the PyQt5 event loop for this window only
    app.exec_()

# Profile Placeholder
def show_profile():
    for widget in root.winfo_children():
        widget.destroy()
    
    # Set the background GIF (example path)
    set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif", 500, 500)

    if current_user is not None:
        # Fetch user data from users_db
        user_data = users_db[current_user]
        address = user_data['address']

        # Display user profile details
        tk.Label(root, text="Your Profile", font=("Helvetica", 16, "bold"),fg="white", bg="orange").pack(pady=20)
        tk.Label(root, text=f"SIM Number: {current_user}", font=("Helvetica", 12),fg="white",bg="orange").pack(pady=5)
        tk.Label(root, text=f"Username: {user_data['username']}", font=("Helvetica", 12), fg="white",bg="orange").pack(pady=5)
        tk.Label(root, text=f"Address: {address}", font=("Helvetica", 12),fg="white", bg="orange").pack(pady=5)
        tk.Label(root, text=f"Hotline: {user_data['hotline'] if user_data['hotline'] else 'N/A'}", 
                 font=("Helvetica", 12),fg="white", bg="orange").pack(pady=5)

        # Buttons
        tk.Button(root, text="Edit Profile", command=show_edit_profile_window, 
                  font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(root, text="Back", command=show_post_login_menu, 
                  font=("Helvetica", 12), bg="#f44336", fg="white").pack(pady=10)

        # Generate the map and show it in a new window
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode(address)
        if location:
            latitude, longitude = location.latitude, location.longitude
        else:
            latitude, longitude = 13.7600, 121.1500  # Default location if address not found

        map_file = create_map(latitude, longitude, address)
        
        # Ensure the map is shown when the button is clicked
        tk.Button(root, text="Show Map", command=lambda: show_map_window(map_file), 
                  font=("Helvetica", 12), bg="#2196F3", fg="white").pack(pady=10)
    else:
        # Handle case where no user is logged in
        tk.Label(root, text="No user is currently logged in.", font=("Helvetica", 12), 
                 fg="red", bg="white").pack(pady=20)

def show_edit_profile_window(): 
    for widget in root.winfo_children():
        widget.destroy()
        set_background("C:/Users/mjjme/Desktop/New folder (2)/bgwall.gif",500,500)
    global current_user  # Use the current logged-in user


    # Fetch current user data
    user_data = users_db.get(current_user, {})
    username = user_data.get('username', '')
    address = user_data.get('address', '')
    password = user_data.get('password', '')

    # Title Label
    tk.Label(root, text="Edit Profile", font=("Helvetica", 16, "bold"),fg="black", bg="orange").pack(pady=20)

    # Username Field
    tk.Label(root, text="Username:", font=("Helvetica", 12),fg="white", bg="orange").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.insert(0, username)  # Pre-fill with current username
    username_entry.pack(pady=5)

    # Address (Barangay) Field
    tk.Label(root, text="Barangay:", font=("Helvetica", 12),fg="white", bg="orange").pack(pady=5)
    # Fetch barangay list from the database
    barangay_list = get_barangay_list()

    # Create a Combobox for the Barangay selection
    barangay_combobox = ttk.Combobox(root, values=barangay_list)
    barangay_combobox.pack(pady=5)

    # Password Field
    tk.Label(root, text="New Password:", font=("Helvetica", 12),fg="white", bg="orange").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.insert(0, password)  # Pre-fill with current password (optional)
    password_entry.pack(pady=5)

    # Confirm Password Field
    tk.Label(root, text="Confirm Password:", font=("Helvetica", 12),fg="white", bg="orange").pack(pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=5)

    # Feedback label
    feedback_label = tk.Label(root, text="", font=("Helvetica", 10), fg="red")
    feedback_label.pack(pady=5)

    # Save Changes Function
    def save_changes():
        new_username = username_entry.get()
        new_address = barangay_combobox.get()
        new_password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Validate fields
        if new_password != confirm_password:
            feedback_label.config(text="Passwords do not match!", fg="red")
            return
        if not new_username or not new_address:
            feedback_label.config(text="All fields are required!", fg="red")
            return

        # Update user data in the database
        users_db[current_user]['username'] = new_username
        users_db[current_user]['address'] = new_address
        users_db[current_user]['password'] = new_password

        feedback_label.config(text="Profile updated successfully!", fg="green")


    # Save Button
    tk.Button(root, text="Save Changes", command=save_changes, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)

    # Back Button to Profile Window
    tk.Button(root, text="Back", command=show_profile, font=("Helvetica", 12), bg="#f44336", fg="white").pack(pady=10)

def show_login_animation():
    global frames  # Use the global frames variable to retain image references

    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()


    # Load the GIF using Pillow (PIL)
    gif_path = "C:/Users/mjjme/Desktop/New folder (2)/123loop.gif"  # Ensure this path is correct and the file exists

    try:
        # Open the GIF file using PIL
        gif = Image.open(gif_path)
        frames.clear()  # Clear old frames if any

        # Extract each frame of the GIF and store in frames
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = ImageTk.PhotoImage(gif.copy())  # Convert to Tkinter-compatible image
            frames.append(frame)
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return

    # Create a label to display the GIF
    gif_label = tk.Label(root)
    gif_label.pack(pady=125)

    # Function to animate the GIF
    def animate_gif(count):
        if frames:  # Ensure frames are available
            gif_label.configure(image=frames[count])
            root.after(40, animate_gif, (count + 1) % len(frames))  # Loop through frames

    # Start the GIF animation
    animate_gif(0)

    # Simulate loading time
    root.after(5000, show_post_login_menu)  # Wait for 5 seconds then go to the main menu

def show_logout_animation():
    global frames  # Use the global frames variable to retain image references

    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()
   
    # Load the GIF using Pillow (PIL)
    gif_path = "C:/Users/mjjme/Desktop/New folder (2)/123loop.gif"  # Ensure this path is correct and the file exists

    try:
        # Open the GIF file using PIL
        gif = Image.open(gif_path)
        frames.clear()  # Clear old frames if any

        # Extract each frame of the GIF and store in frames
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = ImageTk.PhotoImage(gif.copy())  # Convert to Tkinter-compatible image
            frames.append(frame)
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return

    # Create a label to display the GIF
    gif_label = tk.Label(root)
    gif_label.pack(pady=125) 

    # Function to animate the GIF
    def animate_gif(count):
        if frames:  # Ensure frames are available
            gif_label.configure(image=frames[count])
            root.after(40, animate_gif, (count + 1) % len(frames))  # Loop through frames

    # Start the GIF animation
    animate_gif(0)

    # Simulate loading time
    root.after(5000, show_main_menu)  # Wait for 5 seconds then go to the main menu

# Start the main menu
show_main_menu()


# Start the tkinter mainloop
root.mainloop()
