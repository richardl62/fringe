import re
import io
import glob
import sys

start_date = 16
end_date = 22

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

def get_matching_old_show_line(line_to_match):
    def get_show_name(line) :
        return line.split(",")[0].strip()

    show_name = get_show_name(line_to_match)
    
    with open("my-style-old.csv") as my_style_old:

        for line in my_style_old:
            if show_name == get_show_name(line):
                return line
    
    return False

# /*, encoding='utf-8'*/
with open(get_exported_favourites(),encoding='windows-1252') as exported_favourites,\
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
            if "Aug" in date: 
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
        K="-"

        data = (title,times,venue,duration,dates,R,K,link)
        return ",".join(data)+"\n"

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
                old_line = get_matching_old_show_line(converted)
                if old_line:
                    my_style_new.write("%s\n"%old_line)
                    continue

                my_style_new.write(converted)
                additions.write(converted)

            except Exception as e:
                print("WARNING: Cannot process line ", lineno, ":", raw_line, "\n", 
                "Report error: ", e, "\n")

print("Done")




