import camelot
import tkinter as tk
import time
tables = camelot.read_pdf("data/2024/reports/20023805.pdf", flavor="stream", columns=['60, 100, 260,320,380, 440'],row_tol=40)
tables[0].df
camelot.plot(tables[0], kind='contour').show()
tk.mainloop()