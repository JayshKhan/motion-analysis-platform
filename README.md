# <img src="assets/logo.jpeg" alt="MAP Logo" width="60" height="60" align="left">  Motion Analysis Platform (M.A.P.)

<br>

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6%2B-brightgreen.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!NOTE]
>  The project is currently Under Developement so the below README may not provide whole information Yet.*
> 
## Welcome to the Future of Motion Planning!

**M.A.P.** isn't just another motion planning framework; it's your interactive playground for exploring the fascinating world of robotics algorithms!  Dive deep into 2D environments, design challenging scenarios, and unleash the power of pathfinding with a user interface so intuitive, it feels like magic.

[//]: # (<p align="center">)

[//]: # (  <img src="docs/_static/screenshot_main_menu.png" alt="Main Menu Screenshot" width="400">)

[//]: # (  <img src="docs/_static/screenshot_environment_editor.png" alt="Environment Editor Screenshot" width="400">)

[//]: # (</p>)

## Why M.A.P.? Because We've Got It All:

*   **⚡️ <ins>Visualize the Magic</ins>:** Witness algorithms come to life with real-time visualization! Watch as your chosen pathfinders navigate complex mazes, dance around obstacles, and race towards their goals.
*   **🤖 <ins>Become the Algorithm Architect</ins>:** Unleash your inner genius! Import and test your own custom motion planning algorithms with ease. M.A.P.'s flexible design welcomes innovation.
*   **🕵️‍♀️ <ins>Sensors Galore</ins>:**  Don't limit your robots! Equip them with custom-designed sensors through a seamless import system. The world is your oyster (or at least, your 2D grid).
*   **🎓 <ins>Learn by Doing</ins>:** M.A.P. is more than just a tool; it's an educational adventure. Perfect for students, researchers, and anyone curious about the captivating realm of robotics.
*   **🎨 <ins>Effortless Environment Design</ins>:** Craft intricate worlds with a user-friendly environment editor. Save, load, and modify your creations with simple clicks and keystrokes. No more tedious coding of grids!
*   **🚀 <ins>Ready, Set, Execute!</ins>:** Select your algorithm, set your start and goal, and hit "Run"! M.A.P.'s dedicated execution screen puts you in the control room of your robotic simulations.

## Feature Frenzy:

| Feature                  | Description                                                                                                                                               |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Environment Editor**   | Design custom 2D environments with obstacles. Save and load your creations.                                                                                |
| **Algorithm Selection** | Choose from pre-built algorithms (Bug, Potential Field, more to come!) or import your own.                                                                  |
| **Sensor Import**        | Integrate custom sensor models (must inherit from `SensorModel`) to enhance your robots' perception.                                                     |
| **Execution Screen**     | Set start/goal positions, run algorithms, and visualize the pathfinding process.                                                                           |
| **Real-time Visualization** | Watch algorithms in action as they explore the environment and discover paths.                                                                             |
| **User-Friendly UI**     | Intuitive Pygame-based interface for a smooth and engaging experience.                                                                                    |
| **Modular Design**       | Easily extendable architecture. Add new algorithms, sensors, and features with a well-defined structure.                                                  |
| **Cross-Platform**       | Runs wherever Python and Pygame go! (Windows, macOS, Linux)                                                                                                  |
| **Open Source (MIT)**    | Contribute, modify, and share! Let's build the future of motion planning together.                                                                        |

## Getting Started

### Prerequisites

Make sure you have Python 3.12+ installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/motion-analysis-platform.git
    cd motion-analysis-platform
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the following command from the project root:

```bash
python main.py
```

This will launch the main menu, from where you can:
*   **Edit Environment:** Create your own 2D world.
*   **Import Sensor Model:** Give your robots the gift of sight (or other senses).
*   **Select Algorithm:** Choose your pathfinding champion.
*   **Start!:** Set the start and goal, and watch the algorithm work its magic.

## Architecture

Below are diagrams illustrating the architecture of the Motion Analysis Platform. 

### Stacked Architecture

You can render this diagram using a PlantUML extension in your IDE or an online tool.

```plantuml
@startuml

!theme vibrant

title Motion Analysis Platform - Stacked Architecture

package "User Interface (UI) Layer" {
    [Pygame Rendering Engine] as Pygame
    [UI Screens (main_menu, editor, etc.)] as Screens
    [UI Components (buttons, assets)] as Components
}

package "Application Logic Layer" {
    [Main Application (MAPApp)] as App
    [Screen Management] as ScreenManager
}

package "Core Logic Layer" {
    [Motion Planning Algorithms] as Algorithms
    [Environment Representation] as Environment
    [Sensor Models] as Sensors
}

package "Data & Configuration Layer" {
    [Configuration (config.py)] as Config
    [Asset Files (images, etc.)] as Assets
}

Pygame -down-> App
Screens -down-> App
Components -down-> Screens

App -down-> ScreenManager
ScreenManager -down-> Algorithms
ScreenManager -down-> Environment
ScreenManager -down-> Sensors

Algorithms ..> Environment : Reads
Sensors ..> Environment : Reads

App ..> Config : Reads
Components ..> Assets : Reads

@enduml
```

### Class Diagram

A visual representation of the class diagram can be found in our full [documentation](https://yourusername.github.io/motion-analysis-platform/architecture.html).

## Documentation

Detailed documentation, including a comprehensive API reference and tutorials, will be hosted on GitHub Pages. Once you push to `main`, the documentation will be available at `https://yourusername.github.io/motion-analysis-platform/`.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

M.A.P. is released under the **MIT License**. Feel free to use, modify, and distribute it as you see fit.

## Acknowledgements

*   **Pygame:**  The amazing library that powers our UI.
*   **Python:** The versatile language that makes it all possible.
*   **All the brilliant minds** who have contributed to the field of motion planning.

## The Future is Bright - And Full of Robots:

M.A.P. is under active development. I envision a future where this platform becomes a vibrant hub for motion planning research, education, and experimentation.

**Stay tuned for:**

*   More pre-built algorithms (RRT, PRM, and beyond!).
*   Advanced sensor models.
*   3D environments (because why not?).
*   AI-powered features.
*   A thriving community of users and contributors.

## Let's build something amazing together!

<p align="center">
  <img src="docs/_static/screenshot_execution_screen.png" alt="Execution Screen Screenshot" width="600">
</p>

---
