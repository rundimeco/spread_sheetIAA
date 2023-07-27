import glob
import json
import pandas
from tools_iaa import *
import sys
from pathlib import Path

def get_df(input_files):
  print("Files provided with appropriate extension :")
  print(json.dumps(list(set(input_files)), indent = 2))
  files_csv = set([x for x in input_files if Path(x).suffix in [".csv", "txt"]])
  files_excel = set([x for x in input_files if Path(x).suffix in [".xls", ".xlsx", "ods"]])
  print("Transforming into Pandas Dataframes ...")
  try:
    data_frames = [pandas.read_csv(path) for path in files_csv]
  except:
    print("Debugging Pandas error")
    for path in files_csv :
        print(path)
        data_frames = [pandas.read_csv(path, delimiter = ";") for path in files_csv]
  data_frames += [pandas.read_excel(path) for path in files_excel ]
  return data_frames

def get_iaa_from_files(input_files):
  data_frames = get_df(input_files)
  
  annotateurs = []
  sheet_headers = []
  
  for cpt_df, df in enumerate(data_frames):
      annotations = []
      cats = list(df.columns)
      sheet_headers.append(cats)
      for cpt_line, line in df.iterrows():
          this_annot = "-"
          for cpt_val, val in enumerate(line[1:]):
              if pandas.isna(val)==False:
                  this_annot = str(val)
          annotations.append(this_annot)
          #check double annotation
          #check all_columns ou fusion --> si colonnes exclusives
          #if cpt_line>100:break
      annotateurs.append(annotations)

  check_regularity(input_files, annotateurs, sheet_headers)

  results = get_iaa(annotateurs)


if __name__=="__main__":
  if len(sys.argv)==1:
    dir_path = "dummy_data/csv/"
    print(f"No directory provided, using default directory : {dir_path}")
    input_files = glob.glob(f"{dir_path}/*.csv")
  elif len(sys.argv)==2:
    dir_path = sys.argv[1]
    print(f"Using  : {dir_path}")
    input_files = glob.glob(f"{dir_path}/*.csv")
    input_files +=glob.glob(f"{dir_path}/*.xls*")
    input_files +=glob.glob(f"{dir_path}/*.txt*")
  else:
    input_files = sys.argv[1:]
  #TODO: filter out unsupported formats ?

  assert len(input_files)>1, NB_files_error(input_files)
  results = get_iaa_from_files(input_files)

