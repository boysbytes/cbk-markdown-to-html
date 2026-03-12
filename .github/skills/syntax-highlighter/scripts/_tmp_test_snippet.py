# Calculate total sales for each fruit
total_sales = df[days].sum(axis=1)
df['Total'] = total_sales

# Create pie chart
plt.figure(figsize=(10, 8))
colors = ['steelblue', 'gold', 'purple', 'coral']
plt.pie(df['Total'], labels=df['Fruit'], autopct='%1.1f%%', 
       colors=colors, startangle=90, explode=[0.05, 0, 0, 0])
plt.title('Total Fruit Sales for the Week')
plt.axis('equal')  # Equal aspect ratio ensures circular pie
plt.show()

# Display total sales values
print("\nTotal sales by fruit:")
for fruit, total in zip(df['Fruit'], df['Total']):
   print(f"{fruit}: {total} units")
