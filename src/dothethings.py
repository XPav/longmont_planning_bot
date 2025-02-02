import scrapeplanningpage
import parsepdf

webpage_url = 'https://longmontcolorado.gov/planning-and-development-services/plans-and-reports/active-development-log-and-map/' 
text_to_search_for = 'Active Development Log'  
output_folder = '.\\data'

# Download it!
file = scrapeplanningpage.download_pdf( webpage_url, text_to_search_for, output_folder)

# Make it into a dataframe!
df = parsepdf.spreadsheet_to_dataframe( file )

# Convert it to CSV and JSON!
df.to_json(file + '.json', index=False)
df.to_csv(file + '.csv',errors='replace',index = False)

# Maybe should jam this all in a single dataframe?

# Then do some diffs

# Then output to places

