import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.chdir(os.path.dirname(__file__))
# ^^^Change the working directory to the location of this script^^^
# ^^^This is important for relative paths to work correctly^^^

sales_data = pd.read_csv("data/Fashion_Retail_Sales.csv")

"""Statistical Analysis of the  Sales Data"""

# Revenue analysis
def total_revenue(datafile): # Function to find the total revenue
    total_revenue = datafile["Purchase Amount (USD)"].sum()
    return total_revenue

def revenue_per_day(datafile): # Function to find the revenue per day
    datafile["Date_Purchased_Parsed"] = pd.to_datetime(datafile["Date Purchase"], dayfirst=True) # Convert the date column to datetime format
    parsed_dates = datafile["Date_Purchased_Parsed"].dt.date # Extract just the dates
    revenue_per_day = datafile.groupby(parsed_dates)["Purchase Amount (USD)"].sum()
    return revenue_per_day

def revenue_per_week(datafile): # Function to find the revenue per week
    datafile["Date_Purchased_Parsed"] = pd.to_datetime(datafile["Date Purchase"], dayfirst=True) # Convert the date column to datetime format
    parsed_dates = datafile["Date_Purchased_Parsed"].dt.date # Extract just the dates
    revenue_per_week = datafile.groupby(pd.Grouper(key="Date_Purchased_Parsed", freq="W"))["Purchase Amount (USD)"].sum()
    return revenue_per_week

def revenue_per_month(datafile): # Function to find the revenue per month
    datafile["Date_Purchased_Parsed"] = pd.to_datetime(datafile["Date Purchase"], dayfirst=True) # Convert the date column to datetime format
    parsed_dates = datafile["Date_Purchased_Parsed"].dt.date # Extract just the dates
    revenue_per_month = datafile.groupby(pd.Grouper(key="Date_Purchased_Parsed", freq="M"))["Purchase Amount (USD)"].sum()
    return revenue_per_month

# Functions to find the top selling items
def top_selling(datafile): # Function to find the top selling items
    top_selling = datafile.groupby("Item Purchased")["Purchase Amount (USD)"].sum().sort_values(ascending=False)
    return top_selling

# Functions to find customer spending patterns
def avg_per_customer(datafile): # Function to find the average spending per customer
    avg_per_customer = datafile.groupby("Customer Reference ID")["Purchase Amount (USD)"].mean()
    return avg_per_customer

def median_per_customer(datafile): # Function to find the median spending per customer
    median_per_customer = datafile.groupby("Customer Reference ID")["Purchase Amount (USD)"].median()
    return median_per_customer

def totals_per_customer(datafile): # Function to find the total spending per customer
    totals_per_customer = datafile.groupby("Customer Reference ID")["Purchase Amount (USD)"].sum()
    return totals_per_customer 
    
def purchases_per_customer(datafile): # Function to find the number of purchases per customer
    purchases_per_customer = datafile.groupby("Customer Reference ID")["Item Purchased"].count()
    return purchases_per_customer

# Product feedback analysis
def review_per_item(datafile): # Function to find the number of reviews per item
    feedback_analysis = datafile.groupby("Item Purchased")["Review Rating"].value_counts()
    return feedback_analysis

def avg_review_per_item(datafile): # Function to find the average review rating per item
    avg_review_per_item = datafile.groupby("Item Purchased")["Review Rating"].mean()
    return avg_review_per_item
# ^^^Correlate customer spending with review ratings: does higher reviews = higher spending?^^^


"""Visualizations of the Sales Data"""
# Revenue analysis
def plot_revenue_per_day(datafile): # Function to plot the revenue per day
    revenue = revenue_per_day(datafile)
    plt.figure(figsize=(10, 5))
    plt.plot(revenue.index, revenue.values)
    plt.title("Revenue per Day")
    plt.xlabel("Date")
    plt.ylabel("Revenue (USD)")
    
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_revenue_per_week(datafile): # Function to plot the revenue per week
    revenue = revenue_per_week(datafile)
    plt.figure(figsize=(10, 5))
    plt.plot(revenue.index, revenue.values, marker='o', ms=3)
    plt.title("Revenue per Week")
    plt.xlabel("Date")
    plt.ylabel("Revenue (USD)")

    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_revenue_per_month(datafile): # Function to plot the revenue per month
    revenue = revenue_per_month(datafile)
    plt.figure(figsize=(10, 5))
    plt.plot(revenue.index, revenue.values, marker='o', ms=3)
    plt.title("Revenue per Month")
    plt.xlabel("Date")
    plt.ylabel("Revenue (USD)")

    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

# Top selling items
def plot_top_selling(datafile): # Function to plot the top selling items
    top_selling_items = top_selling(datafile).head(10)
    plt.figure(figsize=(10, 5))
    top_selling_items.plot(kind='bar')
    plt.title("Top Selling Items")
    plt.xlabel("Item")
    plt.ylabel("Revenue (USD)")

    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

# Customer spending patterns
def plot_customer_spending_patters(datafile): # Function to plot the customer spending patterns
    avg_spending = avg_per_customer(datafile)
    median_spending = median_per_customer(datafile)
    total_spending = totals_per_customer(datafile)
    purchase_counts = purchases_per_customer(datafile)

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    axs[0, 0].boxplot([avg_spending], labels=["Avg Spend"], showmeans=True)
    axs[0, 0].set_title("Average Customer Spending")
    axs[0, 0].set_ylabel("USD")
    axs[0, 0].grid(axis='y', linestyle='--', alpha=0.7)

    axs[0, 1].boxplot([median_spending], labels=["Median Spend"], showmeans=True)
    axs[0, 1].set_title("Median Customer Spending")
    axs[0, 1].set_ylabel("USD")
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.7)

    axs[1, 0].boxplot([total_spending], labels=["Total Spend"], showmeans=True)
    axs[1, 0].set_title("Total Customer Spending")
    axs[1, 0].set_ylabel("USD")
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.7)

    axs[1, 1].boxplot([purchase_counts], labels=["Purchase Count"], showmeans=True)
    axs[1, 1].set_title("Customer Purchase Frequency")
    axs[1, 1].set_ylabel("Count")
    axs[1, 1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def plot_spend_vs_purchases(datafile): # Are customers who spend more also the ones who purchase more or just big ticket items?
    total_spend = totals_per_customer(datafile)
    purchase_count = purchases_per_customer(datafile)

    plt.figure(figsize=(8, 6))
    plt.scatter(purchase_count, total_spend, alpha=0.7, edgecolors='k')
    plt.title("Total Spend vs. Number of Purchases")
    plt.xlabel("Purchase Count")
    plt.ylabel("Total Spending (USD)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(datafile):
    df = pd.DataFrame({
        "Avg Spend": avg_per_customer(datafile),
        "Median Spend": median_per_customer(datafile),
        "Total Spend": totals_per_customer(datafile),
        "Purchase Count": purchases_per_customer(datafile)
    })

    corr = df.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Between Customer Metrics")
    plt.tight_layout()
    plt.show()

# Customer feedback analysis
def plot_review_per_item(datafile): # Function to plot the number of reviews per item
    review = avg_review_per_item(datafile).sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    review.plot(kind='bar', color='skyblue')
    plt.title("Average Review Rating per Item")
    plt.xlabel("Item")
    plt.ylabel("Average Review Rating")
    plt.ylim(0, 5) # Assuming review ratings are between 0 and 5
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_review_vs_sales(datafile): # Correlate customer spending with review ratings: does higher reviews = higher spending?
    avg_reviews = avg_review_per_item(datafile)
    sales = datafile.groupby("Item Purchased")["Purchase Amount (USD)"].sum()

    df = pd.DataFrame({
        "Average Rating": avg_reviews,
        "Total Sales": sales
    })

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Average Rating", y="Total Sales", s=80)
    plt.title("Average Review Rating vs Total Sales")
    plt.xlabel("Average Review Rating")
    plt.ylabel("Total Sales (USD)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()








