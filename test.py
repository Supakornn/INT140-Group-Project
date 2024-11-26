import string

rows = 5 
cols = 5 
available_seat = "\U0001FA91"
reserved_seat = "❌"

seating_chart = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]

column_headers = "   " + "  ".join(f"{i+1}" for i in range(cols))
print(column_headers)

for i, row in enumerate(seating_chart):
    row_label = string.ascii_uppercase[i] 
    row_display = " ".join(available_seat if seat == 0 else reserved_seat for seat in row)
    print(f"{row_label}  {row_display}")
