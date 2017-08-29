import csv,json

printer_in_file = "papercut-print-log-2017-08"
per_printer_output = 'processed/'+printer_in_file+'.json'
users_output = 'processed/'+printer_in_file+'.users.json'

def generateJSONLog():
    excluded_printers = ['P000DontWatchMe']
    printer_dictionary = {}
    user_total_dictionary = {}
    with open('rawLogs/'+printer_in_file+".csv",newline='') as csvfile:
        printreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(printreader,None)
        next(printreader,None)
        for printjob in printreader:
            printuser = printjob[1]
            print_pages = printjob[2]
            print_copies = printjob[3]
            printername = printjob[4]
            num_pages = int(print_pages)*int(print_copies)
            if printername in excluded_printers:
                continue
            if printuser in user_total_dictionary:
                user_total_dictionary[printuser] += num_pages;
            else:
                user_total_dictionary[printuser] = num_pages;
            if printername in printer_dictionary:
                if printuser in printer_dictionary[printername]:
                    printer_dictionary[printername][printuser] += num_pages
                else:
                    printer_dictionary[printername][printuser] = num_pages
                printer_dictionary[printername]['_total'] += num_pages
            else:
                printer_dictionary[printername] = {}
                printer_dictionary[printername]['_total'] = num_pages
                if printuser in printer_dictionary[printername]:
                    printer_dictionary[printername][printuser] += num_pages
                else:
                    printer_dictionary[printername][printuser] = num_pages
    outfile = open(per_printer_output, 'w')
    outfile.write(json.dumps(printer_dictionary))
    outfile2 = open(users_output, 'w')
    outfile2.write(json.dumps(user_total_dictionary))



def write_html_log():
    html_out_file = "output/"+printer_in_file+".html"
    html_out = open(html_out_file, 'w');
    printer_dictionary = json.load(open(per_printer_output))
    def printer_panel(name, users):
        html_out.write("""
                <div class="col-md-4">
                    <div class="panel-group">
                        <div class="panel panel-primary">
                                <div class="panel-heading">
                                    <a data-toggle="collapse" href="#"""+str(name)+"""\">
                                    <h3 class="panel-title"><b>"""+str(name)+"""</b>: """+str(users['_total'])+"""</h3>
                                    </a>
                                </div>
                            <div id=\""""+str(name)+"""\" class="panel-collapse collapse">
                                <div class="panel-body">""")
        for name,pages in users.items():
            if name == "_total":
                html_out.write("Printer Total: "+str(pages)+"<br>")
            else:
                html_out.write("<b>"+str(name)+"</b> : "+str(pages)+"<br>")
        html_out.write("""
                                </div>
                            </div>
                        </div>
                    </div> 
                </div>""");

    html_out.write("""
    <html>
    <head>
        <title>Printer Usage Output</title>
        <link rel="stylesheet" href="css/bootstrap.min.css">
        <link rel="stylesheet" href="css/naughty_printers.css">
        <script src="js/jquery-3.2.1.min.js"></script>
        <script src="js/bootstrap.min.js"></script>
        <script src="js/naughty_printers.js"></script>
    </head>
    <body>
    <nav class="navbar navbar-inverse navbar-static-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">School Printer Monitoring</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li><a href="index.html">Home</a></li>
            </div><!--/.nav-collapse -->
          </div>
        </nav>
        <div class="container">
            <div class="row">
                
            </div>
            <div class="row">
    """)
    for printer, users in printer_dictionary.items():
        printer_panel(printer, users)
    html_out.write("""
        </div>
    </body>
    </html>
    """)

generateJSONLog()
write_html_log()