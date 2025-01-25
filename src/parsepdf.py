import tabula

import os
import pandas as pd

PLANNING_STAGES = [ 'DEVELOPMENT REVIEW', 'PENDING RESUBMITTAL', 'PUBLIC HEARING', 'APPROVED', 'UNDER CONSTRUCTION', 'WITHDRAWN', 'CLOSED' ]

def spreadsheet_to_dataframe(filename):
    # read spreadsheet into the per-page frame
    dfs = tabula.read_pdf( filename, lattice=True, pages='all', pandas_options={'header': None})

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

    clean_df = clean_df.fillna('')
    return clean_df

def list_pdfs(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    return pdf_files

folder_path = 'C:\\fundev\\longmont_planning_bot\\data\\'  # Replace this with the path to your folder
pdf_files = list_pdfs(folder_path)

for pdf in pdf_files:
    df = spreadsheet_to_dataframe( os.path.join(folder_path, pdf) )
    print(df)
