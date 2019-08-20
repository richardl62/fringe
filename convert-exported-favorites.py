import re
import io
import glob
import sys

start_date = 17
end_date = 26

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) > 0)

#from unidecode import unidecode
#def remove_non_ascii(text):
#    return unidecode(unicode(text, encoding = "utf-8"))

#io.open(in_file_name,encoding="utf_16_le" - Did not work

def get_exported_favourites():
    filenames = glob.glob('fringe_search_results*')

    if len(filenames) == 0 :
        print("Error: file called 'fringe_search_results*' not found")
        sys.exit()

    if len(filenames) > 1 :
        print("Error: More  than one file called \'fringe_search_results*\' was found")
        sys.exit()

    return filenames[0]

# /*, encoding='utf-8'*/
with open(get_exported_favourites(),encoding='windows-1252') as exported_favourites,\
    open("my-style-old.csv") as my_style_old, \
    open("my-style-new.csv",  mode='w') as my_style_new, \
    open("additions.csv",  mode='w') as additions, \
    open("raw_lines.txt",mode='w') as raw_lines, \
    open("ascii_lines.txt",mode='w') as ascii_lines:   
    def date_in_range(date):
        return float(date) >= start_date and float(date) <= end_date

    def process_dates(raw_dates):
        # dates are in a string line "9 Aug, 13 Aug, 21 Aug" (with the quotes)
        # and can sometimes include in July 
        #date_array = raw_dates.replace("Aug","").replace(" ","").replace('"',"").split(",")

        out_dates=""
        #for date in date_array:
        #    if date_in_range(date):
        #        out_dates += date + " "
        for date in raw_dates.replace("\"","").split(",") :
            if "Jul" not in date: 
                num = date.replace(" Aug","")
                if float(num) >= start_date and float(num) <= end_date:
                    out_dates += num + " "
        return out_dates.rstrip()


    def process_duration(raw_duration):

        hours = "0"
        match_hours = re.search(r"([0-9]+) hour", raw_duration)
        if match_hours:
            hours = match_hours.group(1)

        mins = "00"
        match_mins = re.search(r"([0-9]+) minutes", raw_duration)
        if match_mins:
            mins = match_mins.group(1)
            if len(mins) == 1:
                mins = "0" + mins
            
        return "%s:%s" % (hours, mins)

    def process_link(raw_link):
        return "https://tickets.edfringe.com" + raw_link

    def remove_commas(str):
        return str.replace(",","")

    def convert_exported(row):
        elems = row.split("	")
        
        title = remove_commas(elems[0])
        venue = remove_commas(elems[2])
        duration = process_duration(elems[3])
        times = remove_commas(elems[4])
        dates = process_dates(elems[5])
        link = process_link(elems[6])
        R="-"
        B="-"
        K="-"

        data = (title,times,venue,duration,dates,R,B,K,link)
        return ",".join(data)+"\n"

    def get_show_name(converted) :
        return converted.split(",")[0]

    # read show names from the old show list
    shows_in_old_list = set()
    for line in my_style_old:
        show_name = get_show_name(line)
        shows_in_old_list.add(show_name)



    lineno = 0
    for raw_line in exported_favourites:

        if not raw_line:
            break

        line = remove_non_ascii(raw_line)
        if(len(line) > 0):
            try:
                lineno += 1
                raw_lines.write("%d: %s" % (lineno, raw_line) )
                ascii_lines.write("%d: %s" % (lineno, line) )
                if(lineno == 1):
                    continue


                converted = convert_exported(line)
                my_style_new.write(converted)
                show_name = get_show_name(converted)
                if show_name not in shows_in_old_list:
                    additions.write(converted)
            except Exception as e:
                print("WARNING: Cannot process line ", lineno, ":", raw_line, "\n", 
                "Report error: ", e, "\n")

print("Done")




