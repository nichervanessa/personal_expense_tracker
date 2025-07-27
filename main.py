import flet as ft
import json
import datetime
import os
from typing import List, Dict
class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = ["Food", "Transportation", "Entertainment", "Shopping", "Bills", "Health", "Education", "Other"]
        self.data_file = "expenses.json"
        self.load_expenses()
    
    def load_expenses(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.expenses = json.load(f)
        except Exception as e:
            print(f"Error loading expenses: {e}")
            self.expenses = []
    
    def save_expenses(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.expenses, f, indent=2)
        except Exception as e:
            print(f"Error saving expenses: {e}")
    
    def add_expense(self, amount: float, description: str, category: str):
        expense = {
            "id": len(self.expenses) + 1,
            "amount": amount,
            "description": description,
            "category": category,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.datetime.now().strftime("%H:%M")
        }
        self.expenses.append(expense)
        self.save_expenses()
        return expense
    
    def delete_expense(self, expense_id: int):
        self.expenses = [exp for exp in self.expenses if exp["id"] != expense_id]
        self.save_expenses()
    
    def get_expenses_by_date_range(self, days: int = 30):
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        return [exp for exp in self.expenses if exp["date"] >= cutoff_str]
    
    def get_expenses_by_category(self, category: str):
        return [exp for exp in self.expenses if exp["category"] == category]
    
    def get_total_spending(self, days: int = 30):
        expenses = self.get_expenses_by_date_range(days)
        return sum(exp["amount"] for exp in expenses)
    
    def get_category_totals(self, days: int = 30):
        expenses = self.get_expenses_by_date_range(days=days)
        totals = {}
        for exp in expenses:
            category = exp['category']
            totals[category] = totals.get(category, 0) + exp["amount"]
        return totals


def expense_tracker_app(page: ft.Page):
    page.title = "Personal Expense Tracker"
    page.window.width = 800
    page.window.height = 600
    page.padding = 10
    page.scroll = ft.ScrollMode.HIDDEN
    page.window.center()
    
    # Initialize expense tracker
    expenses_tracker = ExpenseTracker()
    
    # UI Components
    amount_field = ft.TextField(
        label="Amount ($)", 
        hint_text="0.00", 
        keyboard_type=ft.KeyboardType.NUMBER, 
        width=150
    )
    
    description_field = ft.TextField(
        label="Description", 
        hint_text="What did you spend on?", 
        expand=True
    )
    
    category_dropdown = ft.Dropdown(
        label="Category",
        value="Food",
        options=[ft.dropdown.Option(cat) for cat in expenses_tracker.categories],
        width=200
    )
    
    date_filter = ft.Dropdown(
        label="Show expenses from",
        value="30",
        options=[
            ft.dropdown.Option("7", "Last 7 days"),
            ft.dropdown.Option("30", "Last 30 days"),
            ft.dropdown.Option("90", "Last 3 months"),
            ft.dropdown.Option("365", "Last year"),
            ft.dropdown.Option("all", "All time"),
        ],
        width=200
    )

    expense_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    total_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Total Spent", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.RED_50,
        border_radius=10,
        width=200
    )

    avg_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Daily Average", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.BLUE_50,
        border_radius=10,
        width=200
    )

    count_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Transactions", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.GREEN_50,
        border_radius=10,
        width=200
    )
    
    category_breakdown = ft.Column()

    def get_category_color(category: str):
        colors = {
            "Food": ft.Colors.ORANGE_400,
            "Transportation": ft.Colors.BLUE_400,
            "Entertainment": ft.Colors.PURPLE_400,
            "Shopping": ft.Colors.PINK_400,
            "Bills": ft.Colors.RED_400,
            "Health": ft.Colors.GREEN_400,
            "Education": ft.Colors.INDIGO_400,
            "Other": ft.Colors.GREY_400
        }
        return colors.get(category, ft.Colors.GREY_400)
    
    def create_expense_card(expense):
        def delete_expense(e):
            expenses_tracker.delete_expense(expense["id"])
            update_display()
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            expense["category"][0], 
                            size=16, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.WHITE
                        ),
                        width=40,
                        height=40,
                        bgcolor=get_category_color(expense["category"]),
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(expense['description'], size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"{expense['category']} • {expense['date']} at {expense['time']}", 
                                size=12, 
                                color=ft.Colors.GREY_600
                            )
                        ],
                        expand=True
                    ),
                    ft.Text(f"${expense['amount']:.2f}", size=16, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        ft.Icons.DELETE, 
                        icon_color=ft.Colors.RED_400, 
                        on_click=delete_expense, 
                        tooltip="Delete Expense"
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=15,
            margin=ft.margin.only(bottom=10),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10
        )

    def create_category_bar(category: str, amount: float, total: float):
        percentage = (amount / total * 100) if total > 0 else 0
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(category, size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(f"${amount:.2f}", size=14, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=get_category_color(category),
                            border_radius=5,
                            height=8,
                            width=f"{percentage}%" if percentage > 0 else "1%"
                        ),
                        bgcolor=ft.Colors.GREY_200,
                        border_radius=5,
                        height=8,
                        width="100%"
                    ),
                    ft.Text(f"{percentage:.1f}%", size=12, color=ft.Colors.GREY_600)
                ]
            ),
            padding=10,
            margin=ft.margin.only(bottom=5)
        )
    
    def add_expense(e):
        try:
            amount = float(amount_field.value or 0)
            description = description_field.value.strip() if description_field.value else ""
            
            if amount <= 0:
                valid_amount_snack_bar=ft.SnackBar(
                        content=ft.Text("Please enter a valid amount greater than 0"),
                        bgcolor=ft.Colors.RED_400
                    )
                page.overlay.append(valid_amount_snack_bar)
                valid_amount_snack_bar.open=True
                return
            
            if not description:
                description_snack_bar=ft.SnackBar(
                        content=ft.Text("Please enter a description"),
                        bgcolor=ft.Colors.RED_400
                    )
                page.overlay.append(description_snack_bar)
                description_snack_bar.open=True
                return
            
            expenses_tracker.add_expense(
                amount=amount,
                description=description,
                category=category_dropdown.value
            )
            
            # Clear form
            amount_field.value = ""
            description_field.value = ""
            category_dropdown.value = "Food"
            page.update()
            
            success_snackbar=ft.SnackBar(
                    content=ft.Text("Expense added successfully!"),
                    bgcolor=ft.Colors.GREEN_600
                )
            page.overlay.append(success_snackbar)
            success_snackbar.open=True
            
            update_display()
            
        except ValueError:
            error_snack_bar=ft.SnackBar(
                    content=ft.Text("Please enter a valid amount"),
                    bgcolor=ft.Colors.RED_400
                )
            page.overlay.append(error_snack_bar)
            error_snack_bar.open=True

    def update_display(e=None):
        days = int(date_filter.value) if date_filter.value != "all" else 999
        
        if date_filter.value == "all":
            expenses = expenses_tracker.expenses
        else:
            expenses = expenses_tracker.get_expenses_by_date_range(days=days)
        
        expense_list.controls.clear()

        if expenses:
            sorted_expenses = sorted(expenses, key=lambda x: (x["date"], x["time"]), reverse=True)
            for expense in sorted_expenses:
                expense_list.controls.append(create_expense_card(expense))
        else:
            expense_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No expenses found", 
                        size=16, 
                        color=ft.Colors.GREY_500, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=20
                )
            )
        
        # Update statistics
        total_spent = sum(exp['amount'] for exp in expenses)
        expense_count = len(expenses)
        
        if date_filter.value != "all" and days > 0:
            daily_avg = total_spent / days
        else:
            unique_dates = len(set(exp["date"] for exp in expenses)) if expenses else 1
            daily_avg = total_spent / max(unique_dates, 1)
        
        total_card.content.controls[1].value = f"${total_spent:.2f}"
        avg_card.content.controls[1].value = f"${daily_avg:.2f}"
        count_card.content.controls[1].value = str(expense_count)

        # Update category breakdown
        category_totals = {}
        for exp in expenses:
            category = exp["category"]
            category_totals[category] = category_totals.get(category, 0) + exp['amount']
        
        category_breakdown.controls.clear()
        
        if category_totals:
            category_breakdown.controls.append(
                ft.Text("Spending by Category", size=18, weight=ft.FontWeight.BOLD)
            )
            sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_categories:
                category_breakdown.controls.append(
                    create_category_bar(category, amount, total_spent)
                )
        
        page.update()

    # Create add button
    add_button = ft.ElevatedButton(
        "Add Expense", 
        icon=ft.Icons.ADD, 
        on_click=add_expense,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_400, 
            color=ft.Colors.WHITE
        )
    )
    
    # Set up date filter change handler
    date_filter.on_change = update_display
    
    # Build the UI
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Personal Expense Tracker", 
                        size=28, 
                        weight=ft.FontWeight.BOLD, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=ft.padding.only(bottom=20)
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Add New Expense", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    amount_field,
                                    description_field,
                                    category_dropdown,
                                    add_button
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ]
                    ),
                    padding=20,
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Row(
                    controls=[
                        total_card,
                        avg_card,
                        count_card,
                        ft.Container(expand=True),
                        date_filter
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(height=20),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Recent Expenses", size=18, weight=ft.FontWeight.BOLD),
                                    expense_list,
                                ]
                            ),
                            expand=2,
                            padding=10,
                        ),
                        ft.Container(
                            content=category_breakdown,
                            expand=1,
                            padding=10,
                            bgcolor=ft.Colors.GREY_50,
                            border_radius=10
                        )
                    ],
                    expand=True
                )
            ],
            expand=True
        )
    )
    
    # Initial display update
    update_display()


if __name__ == '__main__':
    ft.app(target=expense_tracker_app, view=ft.AppView.FLET_APP)