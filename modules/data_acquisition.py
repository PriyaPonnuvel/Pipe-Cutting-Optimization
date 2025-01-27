import os
import pandas as pd

def upload_and_validate_file(file):
    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Define the path to save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    
    # Save the file to the server
    file.save(file_path)

    try:
        # Check if the uploaded file is a valid CSV
        if not file.filename.lower().endswith('.csv'):
            raise ValueError('Invalid file type. Only CSV files are allowed.')

        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(file_path)

        # Validate the required columns
        if 'Size' not in data.columns or 'Quantity' not in data.columns:
            raise ValueError('Invalid file format. The file must contain `Size` and `Quantity` columns.')

        # Return the sizes and quantities as a list of tuples
        return list(zip(data['Size'], data['Quantity']))
    
    except pd.errors.EmptyDataError:
        raise ValueError('The file is empty or cannot be read properly.')
    except pd.errors.ParserError:
        raise ValueError('There was an error parsing the CSV file.')
    except Exception as e:
        raise ValueError(f'Error processing the file: {str(e)}')
