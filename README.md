# spread_sheetIAA
Inter Annotator Agreement on Excel/Calc/CSV files

Compares the annoations of 2+ files

Command line usage :
- python get_iaa.py --> example on dummy_data
- python get_iaa.py PATH --> works on any supported format fund in PATH
- python get_iaa.py PATH/\*.csv --> works only on csv files in PATH

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
