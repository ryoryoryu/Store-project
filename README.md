# Python Mini Store Project

## Project Description

This is a terminal-based Python application that simulates a mini store. Users can buy products, and the store keeps track of inventory, calculates prices, and generates receipts in CSV format. 
The project demonstrates the use of Python concepts such as classes, OOP, functions, loops, conditional statements, file handling, and CSV management.

## Features

* View available products with prices and quantities.
* Purchase multiple products in one transaction.
* Inventory management with automatic quantity reduction.
* Handles eggs as packs of 10 and salt in grams.
* Calculates total cost and gives change.
* Generates receipts as CSV files with timestamps.
* Prevents purchase if products are out of stock.

## Products in Store

* Bread: 1 loaf = 1.5 GEL, 50 loaves in stock
* Eggs: 10 pieces per pack = 6 GEL, 150 pieces in stock
* Sunflower Oil: 500ml bottle = 12 GEL, 20 bottles in stock
* Salt: 100g = 2.5 GEL, 2000 grams in stock

## Technologies Used

* Python 3
* CSV module for generating receipts
* Object-Oriented Programming (Classes, Objects)
* File handling and basic error handling
* Functions, loops, and conditional statements

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/ryoryoryu/Store-project
```

2. Navigate into the project directory:

```bash
cd Store-project
```

3. Run the main Python script:

```bash
python store.py
```

4. Follow the terminal prompts to buy products and view your receipt.

## How it Works

* The store displays available products with prices.
* The user selects products and quantities.
* The store checks stock availability.
* The total price is calculated.
* User enters the money, and the program gives the correct change.
* A receipt is saved in a CSV file without overwriting previous receipts.

## Author

* ryoryoryu
* GitHub: (https://github.com/ryoryoryu)

