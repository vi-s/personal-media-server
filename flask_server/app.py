from flask import Flask
from flask import jsonify
import shelve
import os
import subprocess


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# Perform the Unix df -h command and send output as response
@app.route("/dfh")
def dfh():
    # Popen has a bug... it doesnt take the second argument in the
    # list into account, which is why I had to combine the flag
    # param into the same string as the df call. Now there is only one
    # string in the command args list... this is the only way it would work.
    proc = subprocess.Popen(
        ["df -h"], 
        stdout=subprocess.PIPE, 
        shell=True
    )
    (out, err) = proc.communicate() # Communicate blocks

    return "<html><body>{0}</body></html>".format(
        shellout_to_tblhtml(out)
    )    
    # Simple method just inserting BRs
    # out = out.replace('\n', '<br>')

# Perform the Unix df -k command and send output as response
@app.route("/dfk")
def dfk():
    proc = subprocess.Popen(
        ["df -k"], 
        stdout=subprocess.PIPE, 
        shell=True
    )
    (out, err) = proc.communicate()
    
    return "<html><body>{0}</body></html>".format(
        shellout_to_tblhtml(out)
    )

# View download history
@app.route("/peekdl")
def peekdl():
    try:
        folder_memdb_fp = os.environ["FOLDER_MEMDB_FP"]
        folder_mem_shelf = shelve.open(
            folder_memdb_fp, 
            flag='r'
        )
        return jsonify(folder_mem_shelf)
    except Exception, e:
        print str(e)
        return "Error accessing folder_mem.db"

# View webm conversion status
@app.route("/peekwebm")
def peekwebm():
    try:
        webm_prog_fp = os.environ["WEBM_PROG_FP"]
        webm_shelf = shelve.open(
            webm_prog_fp, 
            flag='r'
        )
        return jsonify(webm_shelf)
    except Exception, e:
        print str(e)
        return "Error accessing webm_prog.db"

# Transform output of multiple lines seperated by '\n' char
# and multiple data cells on each line seperated by ' ' char
# into an html table.
def shellout_to_tblhtml(shellout):
    outlines = shellout.split('\n')
    ret_html = ''

    header_contents = ''
    for itm in outlines[0].split(' '):
        if itm:
            header_contents += "<th>{0}</th>".format(itm)

    header_html = "<tr>{0}</tr>".format(header_contents)
    ret_html += header_html

    for row in outlines[1:]:
        rowitms = row.split(' ')
        rowcontents = ''
        for itm in rowitms:
            if itm:
                rowcontents += "<td>{0}</td>".format(itm)
        rowhtml = '<tr>{0}</tr>'.format(rowcontents)
        ret_html += rowhtml 

    ret_html = "<table>{0}</table>".format(ret_html)
    return ret_html


if __name__ == "__main__":
    # host='0.0.0.0' makes the server externally visible
    # since we are listening on all possible IP addresses
    app.run(host='0.0.0.0', debug=True)
