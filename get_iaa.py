import glob
import sys
from tools_iaa import *



if __name__=="__main__":
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-f", "--force_align",
    action="store_true", dest="force", default=False,
    help="Force alignment of files with different number of lines (Default: False)")
  parser.add_option("-l", "--limit", dest="limit", default=0,
                  help="Limit to the first X lines (Default no limit)", metavar="LIMIT")
  (options, args) = parser.parse_args()
  if options.force:
      sys.argv = [x for x in sys.argv if "--force" not in x]
  if options.limit:
      sys.argv.remove("--limit")
      sys.argv.remove(options.limit)
  #print(options)
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
  results = get_iaa_from_files(input_files, options)

