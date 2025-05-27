'''
Extract the following key from the provided financialDocument:
 
Document content:
{data}.
 
extract this specific field:
 
1. Total revenue:
Extract the Total revenue from the document.   
If keyword 'Total revenue' is not present there are some synonyms that you can use to extract the value which serve the same purpose as Total revenue will do.
* Synonyms list for total revenue:
  Rental Income
  Lease Revenue
  Rent Revenue
  Rental Earnings
  Lease Income
  Property Income
  Rental Proceeds
  Income from Rentals
  Rental Receipts
  Rent Collections
  Rental Yield
  Lease Proceeds
  Rental Cash Flow
  Income from Tenants
  Rental Revenue Stream, Sales.

 
2. Total expense:
Extract the Total expense from the document.   
If keyword 'Total expense' is not present there are some synonyms that you can use to extract the value which serve the same purpose as Total expense will do.
*Synonyms list for total expense:
  Total Expenses.


3. Net operating income:
Extract the Net operating income from the document.   
If keyword 'Net operating income' is not present there are some synonyms that you can use to extract the value which serve the same purpose as Net operating income will do.
* Synonyms list for net operating income:
  Operating Profit
  Operating Income
  Business Income
  Operating Margin
  Earnings Before Interest and Taxes (EBIT)
  Net Operating Profit
  Net Operating Earnings
  Operating Results
  Net Operating Revenue
  Net Operating Surplus
  Net Operating Income
  Net Operating Cash Flow
  Operating Financial Results
  Net Operating Performance
  Net Operating Yield
  Net Operating Return
  Net loss of the year
  Net income(loss)
  Net income(profit)
  Excess of revenues over expenses before other items
  surplus
  Deficit, 
  
Return the results in this JSON format:
 
```json
{{
  "totalRevenue": "",
  "totalExpense": "",
  "netOperatingIncome": ""
}}
```
Output Format:
For each field in each document, include status information. The output format should be a JSON with a "extracted_data" array containing objects for each financialDocument.  Each field should have a nested object with these properties:
 
value: The extracted value
status: "success" if extracted, "warning" if not found
reason: Empty string if success, explanation if not extracted
 
For example, each document in the results array should have this structure:
Each document in the results array should follow this structure (described in plain text to avoid API errors):
 
totalRevenue object with value, status, and reason
totalExpense object with value, status, and reason
netOperatingIncome object with value, status, and reason
'''