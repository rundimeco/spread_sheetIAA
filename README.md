# spread_sheetIAA
Inter Annotator Agreement on Excel/Calc/CSV files.
Compares the annotations present in 2+ files

Designed for NER annotation but can probably used for other tasks

Command line basic usage :
- python get_iaa.py --> example on dummy_data
- python get_iaa.py PATH --> works on any supported format fund in PATH
- python get_iaa.py PATH/\*.csv --> works only on csv files in PATH

Options :
- force_align     Force alignment of files with different number of lines (Default: False)
- limit limit the analysis to the first X lines (Default no limit)

As a function:
- get_iaa_from_files(LIST OF FILE PATH)
- see test.py for an example


Supports:
- xls, xlsx
- csv and txt
- ods

Raises errors if :
- has less than 2 annotation files
- headers do not match
- number of lines do not match
