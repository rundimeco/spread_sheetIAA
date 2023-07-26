import json
from nltk import agreement

def get_iaa(annotateurs, verbose = True):
  donnees = []
  
  for i in range(len(annotateurs)):
    for j in range(len(annotateurs[0])):
      donnees.append([str(i), str(j), annotateurs[i][j]])
  ratingtask = agreement.AnnotationTask(data=donnees)
  results = { 
  "kappa "  : ratingtask.kappa(),
  "fleiss " : ratingtask.multi_kappa(),
  "alpha "  : ratingtask.alpha(),
  "scotts " : ratingtask.pi()}
  if verbose :
    print(json.dumps(results, indent = 2))
  return results

def  check_regularity(input_files, annotateurs, sheet_headers):
  #Check number of lines
  NB_annots = [len(x) for x in annotateurs]
  assert min(NB_annots) == max(NB_annots), size_error(input_files, NB_annots) #
  
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

