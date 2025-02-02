import tabula

import os
import pandas as pd

import re
from datetime import datetime, timedelta

def extract_date_from_filename(filename):
    # Regular expression to find 'Week_1_Jan_2025' or similar patterns
    match = re.search(r"Week_(\d+)_([a-zA-Z]+)_(\d{4})", filename)
    
    if match:
        week_number = int(match.group(1))
        month_name = match.group(2)
        year = int(match.group(3))
        
        # Convert month name to month number
        month_number = datetime.strptime(month_name, '%b').month
        
        # Find the first day of the month
        first_day_of_month = datetime(year, month_number, 1)
        
        # based on January 2025 having 5 spreadsheets let's just pick "wednesday" as the release date

        days_to_first_wed = (2 - first_day_of_month.weekday()) % 7
        first_wed = first_day_of_month + timedelta(days=days_to_first_wed)
        
        # Calculate the date of the given week (week_number)
        target_date = first_wed + timedelta(weeks=week_number - 1)
        
        return target_date
    else:
        raise ValueError("Filename does not contain a recognizable date format.")

PLANNING_STAGES = [ 'DEVELOPMENT REVIEW', 'PENDING RESUBMITTAL', 'PUBLIC HEARING', 'APPROVED', 'UNDER CONSTRUCTION', 'WITHDRAWN', 'CLOSED' ]

def spreadsheet_to_dataframe(filename):
    # read spreadsheet into the per-page frame
    dfs = tabula.read_pdf( filename, lattice=True, pages='all', pandas_options={'header': None})

    # turn the filename into a date, it's in the format "Active_Developments_Week_1_Jan_2025.pdf"
    date = extract_date_from_filename(filename)

    # combine them first into a single dataframe
    combined = pd.concat( dfs, ignore_index=True )

    last_stage = None
    clean_df = None
    
    # Brute force find the stage headers 
    for i in range(0,len(combined)):
        firstcell = combined.iloc[i,0]
        for stage in PLANNING_STAGES:
            if firstcell == stage:
                if last_stage is not None:
                    # We've found a complete stage, now turn it into a dataframe
                    # actual data is after the header...
                    data = combined.iloc[ last_stage[1] + 2: i ].copy()
                    # set the header
                    data.columns = list(combined.iloc[last_stage[1]+1])
                    # set the stage of all of these
                    data['Stage'] = last_stage[0]
                    # add to the combined version
                    clean_df = pd.concat( [clean_df, data], ignore_index=True)
                last_stage = (stage, i)

    clean_df['Date'] = date

    clean_df = clean_df.fillna('')
    return clean_df

def list_pdfs(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    return pdf_files

def convert_pdfs(folder):
    pdf_files = list_pdfs(folder)

    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        df = spreadsheet_to_dataframe( os.path.join(folder_path, pdf) )
        
        df.to_json(pdf_path + '.json', index=False)
        df.to_csv(pdf_path + '.csv',errors='replace',index = False)

folder_path = 'C:\\fundev\\longmont_planning_bot\\data\\'  # Replace this with the path to your folder
convert_pdfs(folder_path)