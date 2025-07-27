# personal_expense_tracker

A modern, cross-platform personal expense tracking application built with Python and Flet. Take control of your finances with real-time analytics, category management, and beautiful visualizations that work on desktop, web, and mobile.

## ✨ Features

### 💸 Expense Management
- **Quick Add**: Add expenses with amount, description, and category
- **Smart Categories**: 8 predefined categories with color-coded indicators
- **Instant Validation**: Real-time form validation and error handling
- **Easy Deletion**: Remove expenses with a single click

### 📊 Analytics & Insights
- **Real-time Statistics**: Total spending, daily averages, and transaction counts
- **Visual Breakdowns**: Interactive category spending charts
- **Time-based Filtering**: View expenses by 7 days, 30 days, 3 months, year, or all time
- **Spending Patterns**: Percentage-based category analysis

### 💾 Data Management
- **Persistent Storage**: Automatic JSON file backup
- **Data Recovery**: Robust error handling and data loading
- **Export Ready**: JSON format for easy data migration
- **Lightweight**: No database setup required

### 🎨 User Experience
- **Material Design**: Clean, modern interface
- **Responsive Layout**: Adapts to different screen sizes
- **Cross-Platform**: Windows, macOS, Linux, web, iOS, Android
- **Real-time Updates**: Instant UI updates without page refreshes

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker-python.git
   cd expense-tracker-python
   ```

2. **Install dependencies**
   ```bash
   pip install flet
   ```

3. **Run the application**
   ```bash
   python expense_tracker.py
   ```


## 📱 Platform Deployment

### Desktop Application
```windows
flet run expense_tracker.py
```

### Web Application
```bash
flet run --web expense_tracker.py
```


## 🎯 How to Use

### Adding Expenses
1. Enter the expense amount in the "Amount ($)" field
2. Provide a description of what you spent money on
3. Select the appropriate category from the dropdown
4. Click "Add Expense" to save

### Viewing Analytics
- **Statistics Cards**: View total spent, daily average, and transaction count
- **Category Breakdown**: See spending distribution by category
- **Time Filters**: Use the dropdown to filter expenses by time period

### Managing Data
- **Delete Expenses**: Click the delete icon next to any expense
- **Filter by Date**: Use the date filter to focus on specific time periods
- **Data Backup**: Your data is automatically saved to `expenses.json`

## 🏗️ Project Structure

```
expense-tracker-python/
├── expense_tracker.py          # Main application file
├── expenses.json              # Data storage (auto-created)
├── README.md                 # This file
├── assets/                   # Images and resources
│   └── ico.ico            # App icon

```

## 🛠️ Technical Details

### Architecture
- **Backend**: `ExpenseTracker` class handles data management
- **Frontend**: Flet components for cross-platform UI
- **Storage**: JSON file for lightweight persistence
- **Validation**: Client-side form validation with user feedback

### Key Components
- **Data Models**: Structured expense objects with timestamps
- **UI Components**: Material Design cards, dropdowns, and buttons
- **Event Handling**: Reactive UI updates and user interactions
- **Analytics Engine**: Real-time calculation of spending metrics



