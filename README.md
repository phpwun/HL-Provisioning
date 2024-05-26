
# Android Provisioning Automation

This repository contains two main iterations of an automation system designed to streamline the provisioning process of Android devices. The project utilizes Android ADB in Iteration 1 and integrates Appium and Selenium in Iteration 2 for enhanced automation capabilities.

## Overview

The goal of this project is to demonstrate an effective approach to automating the setup and configuration of Android devices. By automating this process, we can significantly reduce manual effort and increase the efficiency and reliability of device provisioning.

### Technologies Used

- **Android ADB**: Used in Iteration 1 for basic automation and device interaction.
- **Appium**: Introduced in Iteration 2 for UI automation.
- **Selenium**: Used alongside Appium in Iteration 2 to handle more complex UI scenarios.

## Project Structure

The repository is organized into two main folders:

- **[Iteration-1](./Iteration-1)**: Contains the initial version of the automation using Android ADB. This iteration focuses on establishing a basic automation framework and scripting necessary actions using ADB commands.
  
- **[Iteration-2](./Iteration-2)**: Advances the automation setup by incorporating Appium and Selenium. This iteration enhances the ability to handle complex UI interactions and broadens the scope of automation.

- **[Iteration-3](./Iteration-3)**: Further expands on automation techniques by adding additional tools and scripts. This iteration aims to refine and optimize the provisioning process using advanced scripting and command-line tools.

### Iteration-3 Details

- **adb Directory**: Contains essential tools like adb.exe and other DLLs necessary for ADB operations and device interactions.
- **Extra Tools**:
  - `Provision.ps1`: Automates specific provisioning tasks.
  - `window_dump.xml`: Captures device UI layout for analysis and automation.
- **Scripts**:
  - `find.py`: Searches and interacts with device elements.
  - `Main.ps1`: Main script for orchestrating provisioning tasks.
  - `Test.ps1`: Tests and validates the automation scripts.

## Getting Started

To get started with this project, you will need to set up your development environment. Here are the steps to prepare for each iteration:

### Prerequisites

- Android Studio and SDK Tools
- Node.js and npm (for Appium)
- Java (for Selenium)
- Python (for scripting in Iteration-3)

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
   - For additional tools in Iteration-3:
     ```
     Ensure Python is installed and setup scripts are configured correctly.
     ```

## Usage

Each folder contains detailed instructions on how to run the automation scripts:

- **Iteration-1:** Follow the README within the Iteration-1 folder.
- **Iteration-2:** Refer to the README in the Iteration-2 folder for detailed usage instructions.
- **Iteration-3:** Review the README in the Iteration-3 folder to understand the additional tools and scripts.

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

Your Name - [aritterdls@gmail.com](mailto:aritterdls@gmail.com)

Project Link: [https://github.com/phpwun/Halfbaked-Provisioning](https://github.com/phpwun/Halfbaked-Provisioning)
