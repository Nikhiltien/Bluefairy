from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

# Initialize the application
app = QApplication([])

# Create the main window
main_window = QMainWindow()
main_window.setWindowTitle("Bluefairy")

# Create a central widget to hold the layout and widgets
central_widget = QWidget()
main_window.setCentralWidget(central_widget)

# Create a vertical layout
layout = QVBoxLayout()

# Add buttons for game navigation
next_button = QPushButton("Next Move")
prev_button = QPushButton("Previous Move")
jump_button = QPushButton("Jump to Move")

# Add buttons to layout
layout.addWidget(next_button)
layout.addWidget(prev_button)
layout.addWidget(jump_button)

# Set layout to central widget
central_widget.setLayout(layout)

# Show the main window
main_window.show()

# Run the application
app.exec_()
