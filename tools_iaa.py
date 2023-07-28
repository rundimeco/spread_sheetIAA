import json
from nltk import agreement
import pandas
from pathlib import Path

class Struct:
  def __init__(self, **entries):
    self.__dict__.update(entries)

def get_basic_options():
    return Struct(**{"force":False, "limit":0})

def get_df(input_files):
  print("Files provided with appropriate extension :")
  print(json.dumps(list(set(input_files)), indent = 2))
  files_csv = set([x for x in input_files if Path(x).suffix in [".csv", "txt"]])
  files_excel = set([x for x in input_files if Path(x).suffix in [".xls", ".xlsx", "ods"]])
  print("Transforming into Pandas Dataframes ...")
  data_frames = []
  for path in files_csv:
    try:
      data_frames.append(pandas.read_csv(path))
    except:
      data_frames.append(pandas.read_csv(path, delimiter = ";"))
  data_frames += [pandas.read_excel(path) for path in files_excel ]
  return data_frames

def get_iaa_from_files(input_files, options=get_basic_options()):
  data_frames = get_df(input_files)
  
  annotators = []
  sheet_headers = []
  tokens = [] 
  limit_line = int(options.limit)
  for cpt_df, df in enumerate(data_frames):
      this_tokens = []
      annotations = []
      cats = list(df.columns)
      sheet_headers.append(cats)
      for cpt_line, line in df.iterrows():
          this_annot = "-"
          #discarding empty lines:
          if pandas.isna(line[0]) or line[0]==","or line[0]=="\t":
              limit_line+=1#To be sure to reach the limit
              continue
          this_tokens.append(line[0])
          for cpt_val, val in enumerate(line[1:]):
              if pandas.isna(val)==False:
                  this_annot = str(val)
          annotations.append(this_annot)
          #TODO:check double annotation
          #check all_columns ou fusion --> si colonnes exclusives
          if int(options.limit)>0:
              if cpt_line==limit_line:
                  break
      annotators.append(annotations)
      tokens.append(this_tokens)
  print("Checking alignments")
  print([len(x) for x in tokens])
  print([len(x) for x in annotators])
  if int(options.limit)>0:#Making sure all annotations have the same length
      tokens=[x[:int(options.limit)] for x in tokens]
      annotators=[x[:int(options.limit)] for x in annotators]
  print([len(x) for x in tokens])
  print([len(x) for x in annotators])
  check_tokens(tokens)
  check_regularity(input_files, annotators, sheet_headers, options)
  if options.force==True:#align with the smallest number of lines
    min_annot = min([len(x) for x in annotators])
    annotators = [x[:min_annot] for x in annotators]
  results = get_iaa(annotators)

def get_iaa(annotators, verbose = True):
  donnees = []
  print(f"Computing agreement between {len(annotators)} annotators")
  for i in range(len(annotators)):
    for j in range(len(annotators[0])):
      donnees.append([str(i), str(j), annotators[i][j]])
  ratingtask = agreement.AnnotationTask(data=donnees)
  results = { 
  "kappa "  : ratingtask.kappa(),
  "fleiss " : ratingtask.multi_kappa(),
  "alpha "  : ratingtask.alpha(),
  "scotts " : ratingtask.pi()}
  if verbose :
    print(json.dumps(results, indent = 2))
    for annot in annotators:
        print(annot[25:35])
  return results

def check_tokens(tokens):
  for cpt_line in range(0, len(tokens[0]), 20):
      for cpt_file in range(len(tokens)-1):
          list1 = [str(x) for x in tokens[cpt_file][cpt_line:cpt_line+20]]
          list2 = [str(x) for x in tokens[cpt_file+1][cpt_line:cpt_line+20]]
          comp_tokens(list1, list2, cpt_file, cpt_line)

def comp_tokens(list1, list2, cpt_file, cpt_line):
    if list1!=list2:
      print(f"File {cpt_file} VS {cpt_file+1} alignement error")
    else:
      return True
    for paire in zip(list1, list2):
        print(paire, paire[0]==paire[1], cpt_line)
        assert paire[0]==paire[1]
        cpt_line+=1

def  check_regularity(input_files, annotators, sheet_headers, options):
  #Check number of lines
  NB_annots = [len(x) for x in annotators]
  if options.force==False:
    assert min(NB_annots) == max(NB_annots), size_error(input_files, NB_annots) 
  print("Headers found :")
  print(sheet_headers)
  #Check headers regularity
  regular_sheet_headers = ["-".join([str(y) for y in x ]) for x in sheet_headers]
  assert len(set(regular_sheet_headers))==1, header_errors(regular_sheet_headers) 
  
def size_error(csv_files, NB_annots):
  size_annot = [f"{csv_files[i]} : {NB_annots[i]}" for i in range(len(NB_annots))]
  s = "Incorrect number of annotations : \n"
  s+= json.dumps(size_annot, indent = 2)
  return s

def NB_files_error(csv_files):
  s = "Insufficient number of files :\n"
  return s+json.dumps(csv_files, indent = 2)

def header_errors(regular_sheet_headers):
  s = "Problem with headers :\n"
  return s+json.dumps(regular_sheet_headers, indent = 2)

