import re
import io
in_file_name = 'local/exported-favourites.csv'
out_file_name = 'local/my_style.csv'
start_date = 18
end_date = 27

#in_file = 'simple.csv'

# ------------------------------------------------------------------------ #

#io.open(in_file_name,encoding="utf_16_le" - Did not work

with open(in_file_name) as in_file, io.open(
    out_file_name,  mode='w') as out_file: 
        
    def date_in_range(date):
        return float(date) >= start_date and float(date) <= end_date

    def process_dates(raw_dates):
        #make an array of dates
        date_array = raw_dates.replace("Aug","").replace(" ","").replace('"',"").split(",")

        out_dates=""
        for date in date_array:
            if date_in_range(date):
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

    def process_row(row):
        elems = row.split("	")
        
        title = elems[0].replace(",","")
        venue = elems[2].replace(",","")
        duration = process_duration(elems[3])
        times = elems[4].replace(","," ")
        dates = process_dates(elems[5])
        link = elems[6]
        R="-"
        B="-"

        return (title,times,venue,duration,dates,R,B,link)

        
    in_file.readline() 
    for line in in_file:
        out_elems = process_row(line)
        out_file.write(",".join(out_elems)+"\n")

