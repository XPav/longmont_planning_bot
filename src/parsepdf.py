import tabula

pdf_path = "C:\\fundev\\longmont_planning_bot\\data\\Active_Developments_Week_1_Jan_2025.pdf"

dfs = tabula.read_pdf(pdf_path, lattice=True, pages='all')
# read_pdf returns list of DataFrames
print(len(dfs))
print(dfs[0])