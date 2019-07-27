import re
import io

start_date = 18
end_date = 27

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) > 0)

#from unidecode import unidecode
#def remove_non_ascii(text):
#    return unidecode(unicode(text, encoding = "utf-8"))

#io.open(in_file_name,encoding="utf_16_le" - Did not work

with open("exported-favourites.csv") as exported_favourites,\
    open("my-style-old.csv") as my_style_old, \
    open("my-style-new.csv",  mode='w') as my_style_new, \
    open("additions.csv",  mode='w') as additions:
        
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
                num = float(date.replace(" Aug",""))
                if num >= start_date and num <= end_date:
                    out_dates += date + " "
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

        data = (title,times,venue,duration,dates,R,B,link)
        return ",".join(data)+"\n"


    old_show_list = set(my_style_old)

        
    exported_favourites.readline() # skip the header line 
    for raw_line in exported_favourites:
        line = remove_non_ascii(raw_line)
        if(len(line) > 0):

            #try:
            converted = convert_exported(line)

            my_style_new.write(converted)
            if converted not in old_show_list:
                additions.write(converted)
            #except:
            #print("cannot process line: ", raw_line, "\n", line)

