# Motorcycle Stability Analysis: Tank Slapper Phenomena

[![Docker Support](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains a numerical and symbolic study of **High-Speed Wobble (Tank Slapper)** events in motorcycles. The project aims to identify the critical speeds and geometric configurations that lead to unstable oscillations in the steering assembly.

---

## 📋 Research Overview

A "Tank Slapper" is a rapid, oscillating movement of the handlebars. In dynamics terms, this is often a **Hopf Bifurcation** where the damping ratio of the steering system's "wobble mode" becomes negative.

**Key studies:**

### 1. Rake & Trail

Influence of steering head angle and offset on mechanical trail.

### 2. Gyroscopic Effects

The stabilizing/destabilizing forces of the front wheel's angular momentum.

### 3. The Caster Effect (Self-Centering Dynamics)

The fundamental stability of a motorcycle's front end relies on the **Caster Effect**, which is the tendency of the steered wheel to align itself with the direction of travel.

### 4. Tank Slapper: A Deep Dive

A "Tank Slapper" is a violent, high-frequency (typically 7–10 Hz) oscillation of the handlebars, technically known as a **Wobble Mode** instability.

### 5. Preventing the Tank Slapper

Mitigation of the tank slapper event.

---

## 🛠 Tech Stack

- **Language:** Python 3.11
- **Simulation:** `SciPy` (ODE integration), `NumPy` (Linear Algebra)
- **Environment:** Docker & JupyterLab

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have [Docker](https://docs.docker.com/get-docker/) installed on your host machine.

### 2. Build the Environment

Clone the repo and set up the scripts:

```bash
git clone https://github.com/your-username/motorcycle-stability.git
cd motorcycle-stability

# Make scripts executable
chmod +x .scripts/*.sh
```

Build the Docker container using the provided script:

```bash
./.scripts/build.sh
```

This builds the image tagged as `motorcycle-dynamics`.

### 3. Run the Research Environment

Start the JupyterLab server with the local directory mounted:

```bash
./.scripts/run.sh
```

This will:

- Start a Docker container
- Mount your current directory to `/research` inside the container
- Expose JupyterLab on port **5555** (mapped from container's 8888)

Navigate to `localhost:5555` in your browser to access the notebooks.

**Alternative - Manual Docker command:**

If you prefer to run Docker directly:

```bash
docker run -p 5555:8888 -v $(pwd):/research motorcycle-dynamics
```

---

## 📂 Project Structure

```text
.
├── .scripts/           # Build and run automation scripts
│   ├── build.sh        # Docker image build script
│   └── run.sh          # Container startup script
├── assets/             # Images and visual resources
├── notebooks/          # Exploratory analysis and stability plots
├── src/                # Modular Python package
│   └── charts/         # Visualization and plotting modules
│       └── fork.py     # Motorcycle geometry plotting
├── Main.ipynb          # Primary research notebook
├── Dockerfile          # Container definition
├── .gitignore          # Git ignore rules
└── README.md           # You are here
```

---

## 📊 Methodology

1. **Linearization:** Deriving the state-space model of the motorcycle front end.
2. **Eigenvalue Analysis:** Plotting the movement of poles in the complex plane as forward speed increases.
3. **Time-Domain Simulation:** Inducing a "kick" impulse to observe the onset of non-linear oscillations.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

**Author:** Alexander Avramov
