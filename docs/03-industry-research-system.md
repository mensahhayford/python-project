# Industry Research & Petroleum Industry Management System

## Overview

A Python desktop application for storing, searching, and managing structured information about companies and organizations in the petroleum and related industries.

The application uses a Tkinter graphical interface and a JSON file for persistent data storage.

## Key Features

- 🔎 Search for organizations in the database
- ➕ Add new organizations
- 📋 View all available organizations
- 💾 Save organization information to a JSON database
- 🖥️ Interactive graphical user interface

Each organization can contain:

- Sector
- Headquarters
- Key fact
- Year founded
- CEO
- Industry role

## Technologies Used

- Python
- Tkinter
- JSON
- File handling
- Dictionaries
- Functions

## How It Works

The application loads information from `companies.json` when it starts.

Users can then:

1. Search for an existing organization.
2. View its stored information.
3. Add a new organization.
4. Save the new information to the JSON database.
5. View the organizations currently stored in the database.

### Basic Workflow

```text
companies.json
      ↓
Python Application
      ↓
Tkinter Interface
      ↓
Search / Add / List
      ↓
Updated JSON Database

Skills Demonstrated

This project demonstrates practical experience with:

* Python application development
* JSON data management
* File handling
* GUI development with Tkinter
* Structured data
* User input and validation
* Persistent data storage

Future Improvements

Potential improvements include:

* Editing existing organizations
* Deleting organizations
* Advanced search and filtering
* Sector-based filtering
* Data validation
* SQLite database integration
* Improved GUI design

Project Files

- [Python Application](../industry_system.py)
- [JSON Database](../companies.json)