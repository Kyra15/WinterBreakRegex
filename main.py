# import libraries
import os
import re
from collections import defaultdict

folder_path = "/Users/kyramovva/Downloads/PWP2022"
# open the PWP folder and create a list of all the files
def openfiles():
 og_files = os.listdir(folder_path)
 og_filenames = []
 for i in og_files:
     og_filenames.append(i)
 return sorted(og_filenames)

# a smaller list I used for testing
test = ["IMG_0016.JPG", "IMG_0014.JPG", "IMG_0015.JPG", "SM__0002.JPG", "SM__0007.JPG", "MMA1002.JPG", "MMA1003.JPG", "WJ2_0016.JPG", "WJ2_0014.JPG", "WJ2_0015.JPG"]

newfiles = []
d = defaultdict(list)
pref = []
sorted_grouped = []


# search through the list of files, create two variables, the prefix, and the numbers+extension
def search(lst):
  for f in lst:
    regexpref = re.search(r'^\w{4}', f)
    regexnum = re.search(r'\d+\.JPG*', f[4:])
    # try to group the regex search then create a list with three elements: prefix, number, and the extension
    try:
      newnum = regexnum.group()
      newpref = regexpref.group()
      splitname = newnum.split(".")
      splitname.insert(0, newpref)
      newfiles.append(splitname)
    except Exception as e:
      print("num", regexnum, "prefix", regexpref, e)
  return newfiles

# sort the list into sublists based on the prefix
def make_unique(lst):
  sorted_grouped = []
  endstring = "KyraMovva"
  for file in lst:
    d[file[0]].append(file)
    sorted_grouped = list(d.values())
  for i in sorted_grouped:
     i.sort(key=lambda j: j[1])
  # number each of the items in the sublists and use that to determine the how many characters of "yraMovva" that comes before "_KYRA"
  new_group = enumerate(sorted_grouped)
  renamed = []
  for item in new_group:
    item = list(item)
    str_for_end = endstring[:item[0]+1]
    # format each name to include a new prefix and the correct suffix
    for x in item[1]:
      str = f"PWP2024_000{x[1]}{str_for_end}_KYRA.{x[2]}"
      renamed.append(str)
  # save the old image names in the same order as the new names
  oldones = []
  for group in sorted_grouped:
      for item in group:
        new_it = "".join(item)
        final_it = new_it[:-3] + "." + new_it[-3:]
        oldones.append(final_it)
  return oldones, renamed

# writes the old and new names to a csv file
# renames all the names in the folder
def rename_export(old, new):
  with open("returntext.csv", "w") as f:
    f.write("Old,New\n")
    for i in range(len(old)):
      f.write(f"{old[i]},{new[i]}\n")
      os.rename(f"{folder_path}/{old[i]}", f"{folder_path}/{new[i]}")


filelist = openfiles()
foundfiles = search(filelist)
old, final = make_unique(newfiles)
rename_export(old, final)

