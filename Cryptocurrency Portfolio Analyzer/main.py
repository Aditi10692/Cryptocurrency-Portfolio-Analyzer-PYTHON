import requests
import matplotlib.pyplot as plt
from collections import defaultdict
import heapq


class CryptoPortfolioAnalyzer:
    def __init__(self):
        self.portfolio = defaultdict(lambda: {"quantity": 0, "buy_price": 0})
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"

    def add_to_portfolio(self):
        while True:
            try:
                symbol = input(
                    "\nEnter cryptocurrency ID (bitcoin, ethereum, solana): "
                ).lower()

                quantity = float(input("Enter quantity: "))
                buy_price = float(input("Enter purchase price per coin (USD): "))

                self.portfolio[symbol]["quantity"] += quantity
                self.portfolio[symbol]["buy_price"] = buy_price

                print(f"✓ Added {quantity} {symbol.upper()}")

            except ValueError:
                print("Please enter valid numeric values.")
                continue

            more = input("Add another cryptocurrency? (yes/no): ").lower()
            if more != "yes":
                break

    def fetch_real_time_prices(self):
        if not self.portfolio:
            print("Portfolio is empty.")
            return {}

        symbols = ",".join(self.portfolio.keys())

        try:
            response = requests.get(
                self.api_url,
                params={"ids": symbols, "vs_currencies": "usd"},
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                print("Error fetching prices.")
                return {}

        except requests.exceptions.RequestException:
            print("Network error. Check internet connection.")
            return {}

    def calculate_portfolio_value(self):
        prices = self.fetch_real_time_prices()

        if not prices:
            return

        total_value = 0
        total_investment = 0

        print("\n" + "=" * 75)
        print("PORTFOLIO OVERVIEW")
        print("=" * 75)

        print(
            f"{'Coin':<12}{'Qty':<12}{'Buy Price':<15}"
            f"{'Current Price':<18}{'Profit/Loss':<15}"
        )

        print("-" * 75)

        for symbol, data in self.portfolio.items():
            quantity = data["quantity"]
            buy_price = data["buy_price"]

            current_price = prices.get(symbol, {}).get("usd", 0)

            investment = quantity * buy_price
            current_value = quantity * current_price
            profit_loss = current_value - investment

            total_value += current_value
            total_investment += investment

            print(
                f"{symbol.upper():<12}"
                f"{quantity:<12.4f}"
                f"${buy_price:<14.2f}"
                f"${current_price:<17.2f}"
                f"${profit_loss:<14.2f}"
            )

        total_profit = total_value - total_investment

        print("-" * 75)
        print(f"Total Investment : ${total_investment:.2f}")
        print(f"Current Value    : ${total_value:.2f}")
        print(f"Net Profit/Loss  : ${total_profit:.2f}")
        print("=" * 75)

    def visualize_portfolio(self):
        prices = self.fetch_real_time_prices()

        if not prices:
            return

        allocations = {}

        for symbol, data in self.portfolio.items():
            current_price = prices.get(symbol, {}).get("usd", 0)
            allocations[symbol.upper()] = (
                data["quantity"] * current_price
            )

        if not allocations:
            print("No data available.")
            return

        plt.figure(figsize=(8, 8))
        plt.pie(
            allocations.values(),
            labels=allocations.keys(),
            autopct="%1.1f%%",
            startangle=140,
        )

        plt.title("Cryptocurrency Portfolio Allocation")
        plt.show()

    def recommend_diversification(self):
        prices = self.fetch_real_time_prices()

        if not prices:
            return

        heap = []

        for symbol, data in self.portfolio.items():
            current_price = prices.get(symbol, {}).get("usd", 0)
            value = data["quantity"] * current_price

            heapq.heappush(heap, (-value, symbol))

        print("\nTop Holdings")

        for i in range(min(3, len(heap))):
            value, symbol = heapq.heappop(heap)
            print(f"{i+1}. {symbol.upper()} : ${-value:.2f}")

        print("\nDiversification Suggestion:")
        print(
            "Avoid allocating too much capital to a single asset."
        )
        print(
            "Consider spreading investments across multiple cryptocurrencies."
        )

    def run(self):
        print("=" * 55)
        print("CRYPTOCURRENCY PORTFOLIO ANALYZER")
        print("=" * 55)

        while True:
            print("\n1. Add Cryptocurrency")
            print("2. View Portfolio Value")
            print("3. Visualize Portfolio")
            print("4. Diversification Recommendation")
            print("5. Exit")

            choice = input("\nEnter choice (1-5): ")

            if choice == "1":
                self.add_to_portfolio()

            elif choice == "2":
                self.calculate_portfolio_value()

            elif choice == "3":
                self.visualize_portfolio()

            elif choice == "4":
                self.recommend_diversification()

            elif choice == "5":
                print("Thank you for using the analyzer!")
                break

            else:
                print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    analyzer = CryptoPortfolioAnalyzer()
    analyzer.run()