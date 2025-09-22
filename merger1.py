import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


#Býr til Tkinter
root = tk.Tk()
root.withdraw()  

# Hér stimplar einstaklingur inn hvar folderið er með 
directory = filedialog.askdirectory(title="Veldu slóðina þar sem skjölin sem þú vilt sameina eru staðsett:")

if not directory:
    print("Ekkert valið. Prógrammið hættir")
    exit()


# Merge files for each sample and R number combination
merged_files = {} # Þetta er tómt dictionary

# Fer í gegnum alla filea í möpunni og athugar hvort þeir hafa ".fastq.gz" endi

for filename in os.listdir(directory):
    if filename.endswith(".fastq.gz"):
        parts = filename.split("_")             # Filenameið splittað með "_" ef það hefur þau skilyrði fyrir ofan
        if len(parts) >= 4:                     # Forrtið assumear að það sé skipt í 4 hluta, er að tjékka hér hvort það sé skipt í 4 hluta***
            sample = "_".join(parts[:-3])
            r_number = parts[-2][-1]

            if sample not in merged_files:
                merged_files[sample] = {}

            if r_number not in merged_files[sample]:
                merged_files[sample][r_number] = []

            merged_files[sample][r_number].append(filename)

merged_info = []  # Geymir upplýsingar fyrir sameinuðu skjölin

for sample, r_numbers in merged_files.items():
    for r_number, files in r_numbers.items():
        output_filename = f"{sample}_R{r_number}_merged.fastq.gz"
        output_path = os.path.join(directory, output_filename)

        with open(output_path, "ab") as output_file:
            for filename in files:
                input_path = os.path.join(directory, filename)
                with open(input_path, "rb") as input_file:
                    shutil.copyfileobj(input_file, output_file)

        merged_info.append(f"Eftirfarandi skjöl voru sameinuð: {files} í eitt skjal: {output_filename}")

# Displayar sameinuð skjöl í messagebox
messagebox.showinfo("Skjöl sem voru sameinuð:", "\n".join(merged_info))


# ***Þegar forritið splittar upp splittast það í:     
    #Part 1: F152-23 (Nafnið á sýni)
    #Part 2: S2 (Auknúmer??)
    #Part 3: L001 (L númer)
    #Part 4: R1 (R númer)