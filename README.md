# INFECTED: Asymmetric OS Simulation (In development)🦠💻

INFECTED is a retro-styled, asymmetric multiplayer game built entirely in Python. It pits two distinct playstyles against each other: a **Virus Swarm** (multiple players) attempting to navigate and infect a system of directories, and an **Antivirus Command Center** (a single player) tasked with managing system resources, tracking down anomalies, and terminating malicious processes.

Featuring a custom-built Virtual File System (VFS), a from-scratch interactive terminal engine, and hardware-accelerated CRT shaders (to be added), this project is a love letter to 1980s mainframe aesthetics and classic hacking simulators.

![Screenshot Placeholder](link-to-your-screenshot-here.png)
*Replace this with a screenshot of the Amber CRT Antivirus Client!*

---

## 🕹️ Game Mechanics & Player Abilities

**INFECTED** revolves around an intense game of digital cat-and-mouse. The game is highly asymmetric: the Virus player relies on stealth, speed, and misdirection, while the Antivirus player relies on resource management, deduction, and sheer processing power.

### The Core Loop
1. The **Virus** spawns in a random `/users` directory and must navigate the sprawling, procedurally generated VFS maze to locate the critical `sys/kernel.dll` file.
2. The **Antivirus** must monitor system resources. When the Virus performs actions, they spawn processes that consume CPU and RAM, leaving a digital footprint.
3. The Antivirus must track down the anomaly and `kill` the malicious process before the Virus can successfully execute its payload.

### 🦠 The Virus (Swarm Interface)
The Virus player acts as an invasive anomaly. Their interface is a sleek, neon-green Tactical Map and TUI. Their actions are generally fast and cheap, but highly detectable if they aren't careful.

**Goal:** Infiltrate the `sys` folder and compromise the `kernel.dll`.

| Ability | Description | Threat Level |
| :--- | :--- | :--- |
| **Navigate** | Silently traverse the VFS using the TUI. Moving leaves no immediate CPU trace, but might trigger passive syslog alerts if entering restricted zones. | Low |
| **Infect / Replicate** | Corrupt dummy files to create decoys or spread swarm presence. This creates sudden, minor spikes in the host's RAM. | Medium |
| **Cloak** | Temporarily hide from the Antivirus's `ps` (process status) table. Highly effective for slipping past active scans, but slows down movement speed. | High |
| **Execute Payload** | The win condition. Targeting `kernel.dll` initiates a massive CPU spike on the host machine, giving the Antivirus one final window to retaliate. | Critical |

### 🛡️ The Antivirus (Command Center)
The Antivirus player acts as the system administrator. Their interface is a heavy, amber CRT terminal. They have absolute power over the system, but their abilities are constrained by physical hardware limits (CPU Stamina and RAM Capacity). 

**Goal:** Protect System Integrity and terminate the Virus.

| Command | Resource Cost | Description |
| :--- | :--- | :--- |
| **`ls` / `cd`** | *Free* | Navigate the file system to manually inspect folders for tampered files or unusual sizes. |
| **`syslog`** | *Low CPU* | Query the system logs to check for unauthorized access warnings or firewall breaches. |
| **`ps`** | *Free* | Pull up the Task Manager. Crucial for spotting unknown processes (PIDs) that are suddenly eating CPU or RAM. |
| **`scan <dir>`** | *Medium RAM* | Run a deep diagnostic on a specific folder. Temporarily locks up RAM but forces any cloaked Virus in that directory to reveal itself. |
| **`freeze <dir>`** | *High RAM* | Quarantine an entire folder. The Virus cannot enter or leave it, but the host must permanently dedicate RAM to maintain the freeze. |
| **`kill <PID>`** | *Massive CPU* | The Ultimate Weapon. Terminates a process instantly. However, it drains nearly all CPU stamina. **Friendly Fire Warning:** Accidentally killing core system processes (PID 0, 1, or 2) will critically damage your own System Integrity! |

## 🌟 Key Features

### The Antivirus Client (Command Center)
* **Custom Terminal Engine:** A from-scratch, fully interactive CLI featuring accurate soft text-wrapping, cursor tracking, and command history (`UP`/`DOWN` arrows).
* **Hardware-Accelerated CRT Shaders (to be added in future):** Uses `moderngl` to hijack the Pygame rendering pipeline, injecting GLSL shaders directly into the GPU to simulate authentic barrel distortion, chromatic aberration (RGB splitting), phosphor bloom, and scanlines.
* **Resource Simulation:** Commands have actual "costs." A custom `SystemMonitor` tracks active processes (PIDs). Heavy commands (like `kill`) spike the simulated CPU and drain RAM. 
* **Friendly Fire Mechanics:** Recklessly killing core system processes damages the System Integrity (Health) bar, forcing the player to carefully read system logs and `ps` tables before acting.

### The Virus Client (Swarm Interface)
* **Procedural VFS Generation:** The game map is a Virtual File System. Every match uses a recursive algorithm (Depth-First Search) to generate a unique, sprawling labyrinth of folders and decoy files.
* **Interactive 2D Node Map:** A custom camera viewport system mathematically maps the recursive VFS into a 2D space, allowing the player to pan around a visual representation of the network.
* **Retro TUI (Text User Interface):** Navigate the generated file system using classic keyboard controls to hunt for the target kernel files.
---

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/ashutoshvrm05/Infected-multiplayer-game.git
cd Infected-multiplayer-game
```

**2. Set up a Virtual Environment (Recommended)**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install pygame moderngl
pip install pygame
```

## 🎮 How to Play

Currently, the project contains the two standalone client environments.

**Boot the Antivirus Command Center:**
```bash
python av_client.py
```
**Controls:** Keyboard typing.

**Commands to try:**  
- ls (List files)
- cd <folder> (Navigate)
- ps (View active processes and PIDs)
- test_spike (Simulate a malware attack on your CPU, currently for testing)
- kill <PID> (Terminate a process—careful not to kill PID 0, 1, or 2!)

**Boot the Virus Swarm Interface:**

```Bash
python virus_client.py
```
**Controls:**  
-UP / DOWN Arrows: Select files in the TUI.
- ENTER: Open folder / Trigger action menu.
- LEFT CLICK + DRAG: Pan the tactical node map on the left side of the screen.

## 🧠 Technical Highlights for Developers
-The Soft-Wrap Algorithm: The terminal handles long strings dynamically without crashing the cursor. It runs a simulation of the word-wrapping math on the text up to the cursor's index to perfectly calculate 2D X/Y screen coordinates for the blinking block.

-State-to-View Synchronization: UI rendering is strictly decoupled from state changes, ensuring backspaces, arrow key navigation, and word-wrapping never desynchronize the display.

-Multi-Pass Bloom Compositing: The glowing text isn't a simple blur. It uses an additive RGB blending technique with multiple alpha-dimmed layers to create a "hot core" neon effect.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Core Engine:** [Pygame](https://www.pygame.org/) (Canvas rendering, event handling, font generation)
* **GPU Pipeline (to be added in the future):** [ModernGL](https://github.com/moderngl/moderngl) (GLSL Shader compilation and hardware acceleration)


## 📄 License
This project is open-source and available under the MIT License.
