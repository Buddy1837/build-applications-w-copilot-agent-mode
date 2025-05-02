import pdfplumber
import logging
import warnings
import re
from collections import Counter

# Suppress ALL warnings and logging
warnings.filterwarnings('ignore')
logging.getLogger().setLevel(logging.ERROR)

def normalize_whitespace(text):
    """Normalize whitespace in text"""
    return ' '.join(str(text).split())

def is_noise_content(text):
    """Check if text is likely noise or non-tabular content"""
    noise_indicators = [
        'def ', 'print', 'return', '()', '{}', '[]', 
        'import', 'class', 'function', '"""', '#',
        'example:', 'output:', '//', '=', '+', '-',
        'if ', 'else:', 'for ', 'while ', '•', 
        'following', 'note:', 'educator:', 'professor',
        'python', 'code', 'variable', 'statement',
        'indent', '.py', 'import', 'call', 'null',
        'important', 'program', 'execute', 'values',
        'true', 'false', 'none', 'text', 'type'
    ]
    
    text = str(text).lower()
    return (
        any(indicator.lower() in text for indicator in noise_indicators) or
        len(text) < 3 or  # Too short
        text.count(' ') > 5 or  # Too many words - likely a sentence
        sum(1 for c in text if c.isalnum()) < 2  # Not enough actual content
    )

def clean_cell(cell):
    """Clean and validate cell content"""
    if cell is None:
        return None
    text = normalize_whitespace(cell)
    return None if not text or is_noise_content(text) else text

def get_table_structure(table):
    """Analyze and extract proper table structure"""
    if not table or len(table) < 3:
        return None
    
    # Clean all rows first
    cleaned_rows = []
    for row in table:
        cleaned_cells = [clean_cell(cell) for cell in row]
        valid_cells = [cell for cell in cleaned_cells if cell]
        if len(valid_cells) >= 3:
            cleaned_rows.append(valid_cells)
    
    if len(cleaned_rows) < 3:
        return None
    
    # Find most common row length
    lengths = Counter(len(row) for row in cleaned_rows)
    target_length = lengths.most_common(1)[0][0]
    
    # Only keep rows that match the structure
    structured_rows = []
    for row in cleaned_rows:
        if abs(len(row) - target_length) <= 1:
            # Pad shorter rows to match length
            while len(row) < target_length:
                row.append('')
            structured_rows.append(row[:target_length])  # Trim longer rows
    
    return structured_rows if len(structured_rows) >= 3 else None

with pdfplumber.open("smp.pdf") as pdf:
    seen_tables = set()
    table_count = 0
    
    for page_num, page in enumerate(pdf.pages, 1):
        tables = page.extract_tables(table_settings={
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
            "intersection_y_tolerance": 4,  # Even stricter tolerance
            "intersection_x_tolerance": 4,
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 3,
            "min_words_horizontal": 3
        })
        
        for table in tables:
            structured_rows = get_table_structure(table)
            if structured_rows:
                # Format table with consistent column widths
                col_widths = [max(len(str(row[i])) for row in structured_rows) 
                            for i in range(len(structured_rows[0]))]
                
                formatted_rows = []
                for row in structured_rows:
                    formatted_cells = [str(cell).ljust(width) for cell, width 
                                    in zip(row, col_widths)]
                    formatted_rows.append(' | '.join(formatted_cells))
                
                table_str = '\n'.join(formatted_rows)
                if table_str and table_str not in seen_tables:
                    seen_tables.add(table_str)
                    table_count += 1
                    print(f'\nTable {table_count} (Page {page_num}):')
                    print('-' * max(80, max(len(row) for row in formatted_rows)))
                    print(table_str)
                    print('-' * max(80, max(len(row) for row in formatted_rows)))