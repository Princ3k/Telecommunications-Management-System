# Telecommunications Management System

## Overview

This project is a **Telecommunications Management System** designed to simulate the core functionalities of a telecommunication service provider. It includes features for managing customers, contracts, phone lines, call history, and billing. The system also provides tools for data visualization and testing.

## Features

### Customers and Phone Lines
- Each customer can have one or more phone lines.
- Phone lines are associated with different contract types.

### Contract Management
- Supports three types of contracts:
  - **Prepaid Contracts**: Customers pay in advance and operate with a credit limit.
  - **Term Contracts**: Fixed-term agreements for a specified duration.
  - **Month-to-Month (MTM) Contracts**: Flexible agreements without long-term obligations.

### Call Tracking
- Tracks detailed call data, including duration and cost.
- Computes charges based on the associated contract type.

### Billing System
- Generates detailed bills for customers based on their usage.
- Applies contract-specific rules for discounts, penalties, or extra charges.

### Data Handling
- Processes customer and call data from a JSON file (`dataset.json`).
- Converts raw data into structured Python objects for manipulation.

### Visualization
- Includes graphical tools to display insights such as customer behavior and system performance.

## File Structure

- **application.py**: Main entry point for running the system.
- **customer.py**: Manages customer data and interactions.
- **phoneline.py**: Handles phone line operations and associations.
- **contract.py**: Defines the logic for different contract types.
- **call.py**: Tracks and calculates call details.
- **bill.py**: Handles billing and financial transactions.
- **filter.py**: Implements filtering functionality for analyzing data.
- **utils.py**: Provides utility functions to support the main system.
- **visualizer.py**: Visualizes data and system performance.
- **dataset.json**: Sample data for customers, phone lines, and calls.

## How to Use

1. **Set Up the Environment**:
   - Install Python 3.x if not already installed.

2. **Run the System**:
   - Execute `application.py` to start the simulation:
     ```bash
     python application.py
     ```

3. **Explore the Features**:
   - Interact with the system to manage customers, track calls, and view bills.
   - Use the visualizer to analyze customer data and contract usage.

## Customization

- Modify the `dataset.json` file to test the system with new data.
- Extend the functionality by adding new contract types or features.

## License

This project is open for educational and personal use. Contributions and modifications are welcome.

---

Enjoy managing and exploring the Telecommunications Management System! 🚀
