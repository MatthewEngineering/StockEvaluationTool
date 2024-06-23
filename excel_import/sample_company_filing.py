# Sample DataFrames for statements with renamed 'Detail' column to 'Concept'
statement_A = pd.DataFrame({
    'Concept': ['Detail1', 'Detail2', 'Detail3'],
    'Value_A': [10, 20, 30]  # Renamed Value column for Statement A
})

statement_B = pd.DataFrame({
    'Concept': ['Detail4', 'Detail5', 'Detail6'],
    'Value_B': [40, 50, 60]  # Renamed Value column for Statement B
})

statement_C = pd.DataFrame({
    'Concept': ['Detail7', 'Detail8', 'Detail9'],
    'Value_C': [70, 80, 90]  # Renamed Value column for Statement C
})

statement_D = pd.DataFrame({
    'Concept': ['Detail10', 'Detail11', 'Detail12'],
    'Value_D': [100, 110, 120]  # Renamed Value column for Statement D
})

statement_E = pd.DataFrame({
    'Concept': ['Detail13', 'Detail14', 'Detail15'],
    'Value_E': [130, 140, 150]  # Renamed Value column for Statement E
})

statement_F = pd.DataFrame({
    'Concept': ['Detail16', 'Detail17', 'Detail18'],
    'Value_F': [160, 170, 180]  # Renamed Value column for Statement F
})

# Sample filings DataFrame with df_statements containing all statements
filings = pd.DataFrame({
    'primaryDocument': ['Filing1', 'Filing2', 'Filing3'], # Filing Name
    'reportDate': ['First Filing', 'Second Filing', 'Third Filing'], # Description
    'df_statements': [
        pd.DataFrame({'Internal Name': ['Statement A', 'Statement B', 'Statement C'], 'df_table': [statement_A, statement_B, statement_C]}),
        pd.DataFrame({'Internal Name': ['Statement D', 'Statement E', 'Statement F'], 'df_table': [statement_D, statement_E, statement_F]}),
        pd.DataFrame({'Internal Name': ['Statement A', 'Statement D', 'Statement F'], 'df_table': [statement_A, statement_D, statement_F]})
    ]
})
