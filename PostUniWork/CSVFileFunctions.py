import csv

def ExportToCSV(fileName, data):
    # Inputs:
    # - fileName: the name of the CSV file to write data to
    # - data: the data to export to a CSV file (must be a list of lists where each inner list represents a row in excel)

    with open(fileName, 'a', newline='') as csv_file:
        writer_obj = csv.writer(csv_file)  
        for row in data:
            writer_obj.writerow(row)
        csv_file.close()
