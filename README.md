﻿
# Android Provisioning Automation

This repository contains multiple iterations of an automation system designed to streamline the provisioning process of Android devices. The project utilizes Android ADB in Iteration 1 and integrates Appium and Selenium in Iteration 2 for enhanced automation capabilities, with subsequent iterations building further on this foundation.

## Overview

The goal of this project is to demonstrate an effective approach to automating the setup and configuration of Android devices. By automating this process, we can significantly reduce manual effort and increase the efficiency and reliability of device provisioning.

### Technologies Used

- **Android ADB**: Used in Iteration 1 for basic automation and device interaction.
- **Appium**: Introduced in Iteration 2 for UI automation.
- **Selenium**: Used alongside Appium in Iteration 2 to handle more complex UI scenarios.
- **Python**: Used in Iterations 3 and 4 for scripting and automation tasks.
- **PowerShell**: Used across various iterations for scripting on Windows environments.

## Project Structure

The repository is organized into several folders, each representing an iteration of the project:

- **[Iteration-1](./Iteration-1)**: Contains the initial version of the automation using Android ADB. This iteration focuses on establishing a basic automation framework and scripting necessary actions using ADB commands.
  
- **[Iteration-2](./Iteration-2)**: Advances the automation setup by incorporating Appium and Selenium. This iteration enhances the ability to handle complex UI interactions and broadens the scope of automation.

- **[Iteration-3](./Iteration-3)**: Further expands on automation techniques by adding additional tools and scripts. This iteration aims to refine and optimize the provisioning process using advanced scripting and command-line tools.

- **[Iteration-4](./Iteration-4)**: Continues to refine automation processes with a focus on integrating more complex scripting solutions to automate various tasks.
  - `Full-Score.py`: Python script for analyzing or scoring provisioning processes.
  - `Main.ps1`: PowerShell script managing the main automation workflow.
  - `Main.py`: Main Python script driving automation logic.
  - `Test.py`: Python script for testing the automation scripts and ensuring their reliability.

## Getting Started

To get started with this project, you will need to set up your development environment. Here are the steps to prepare for each iteration:

### Prerequisites

- Android Studio and SDK Tools
- Node.js and npm (for Appium)
- Java (for Selenium)
- Python (for later iterations)

### Setup

1. **Clone the Repository:**
   ```
   git clone https://github.com/phpwun/Halfbaked-Provisioning.git
   ```
   
2. **Navigate to the Project Directory:**
   ```
   cd Halfbaked-Provisioning
   ```

3. **Installation:**
   - For ADB:
     ```
     Install Android Studio and ensure ADB is correctly set up.
     ```
   - For Appium and Selenium:
     ```
     npm install -g appium
     # Install Selenium and required drivers
     ```
   - For Python scripts in later iterations:
     ```
     Ensure Python is installed and scripts are configured correctly.
     ```

## Usage

Each folder contains detailed instructions on how to run the automation scripts:

- **Iteration-1:** Follow the README within the Iteration-1 folder.
- **Iteration-2:** Refer to the README in the Iteration-2 folder for detailed usage instructions.
- **Iteration-3:** Review the README in the Iteration-3 folder to understand the additional tools and scripts.
- **Iteration-4:** Examine the README in the Iteration-4 folder for the latest scripts and their functionalities.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

[aritterdls@gmail.com](mailto:aritterdls@gmail.com)

[https://github.com/phpwun/Halfbaked-Provisioning](https://github.com/phpwun/Halfbaked-Provisioning)
