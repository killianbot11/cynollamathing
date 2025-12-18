import requests
import tkinter as tk
from ollama import chat
from ollama import ChatResponse
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO
import re
import time
import json
import requests



# HAIII!! >_<
# my codee 
# kinda does suck with random notes places but
# i should of probably made a tutorial in the notes if i didnt forget lolz
# ah i shoulddd probably use a tool or somthing to allow me to edit the layoutz



with open('data.json', 'r') as file:
    data = json.load(file)

result = None
# annoyed
# normal
# smug
# reactiones
# angry
# fear
# shocked
# name
# mood
# color

value1 = data['value1']
value2 = data['value2']
vaulem = data['mood']
vaulec = data['color']
vaulen = data['name']
print(f"Value 1 is: {value1}")
print(f"Value 2 is: {value2}")
print(f"name is {vaulen}")
print(f"color is {vaulec}")
print(f"mood is {vaulem}")


#normal = ""
#annoyed = ""
#smug = ""
#angry = ""
#fear = ""
#shocked = ""
name = vaulen
color = vaulec
mood = vaulem

annoyed = "face/"+"annoyed.png" 
normal = "face/"+"normal.png" 
smug = "face/"+"smug.png" 
angry = "face/"+"angry.png" 
fear = "face/"+"fear.png" 
shocked = "face/"+"shocked.png" 
#name = "cynessa" 
#color = "#000000" 
#mood = "is kinda depressed, there name is cynessa, they somtimes have a childish personality, also they like to talk and switch expressions"




root = tk.Tk()






def ollama():
    user = entry.get()
    
    response = chat(model='gemma3', messages=[
        {"role": "system", "content": f"Your character profile: {mood}" "btw keep the messages short to like 10-15 words"
            "make sure your response contains one of these's words smug, annoyed, normal, angry, shocked, fear"
            "if you want to show an image say [ image ] in the message for you to show an image of whatever google gives, btw if you want you can be very detailed" },
        {"role": "user", "content": user},
    ])
    
    global result
    result = response['message']['content']
    print("Ollama says:", result)
    
    # Extract search term from brackets
    search_term = extract_bracketed(result)
    if search_term:
        print("Searching for:", search_term)
        img_url = imagesearch(search_term)
        if img_url:
            img = download_image(img_url)
            if img:
                popup_image(img)
            else:
                print("Failed to download image")
        else:
            print("No image found")
    else:
        print("No bracketed search term found")
    
    # Show character reaction
    imagetest()
    talk()

def extract_bracketed(text):
    """
    Returns the first substring inside [] in the given text.
    Example: "[Wii remote]" -> "Wii remote"
    """
    match = re.search(r"\[(.*?)\]", text)
    if match:
        return match.group(1)  # only the text inside brackets
    return None    




def imagetest():
    
    print(result)
    print("ran!")
    img2 = ImageTk.PhotoImage(Image.open(normal))
    
    image_label.configure(image=img2)
    image_label.image = img2
    # basic stuff might add it where it can blink or somthing


    if "annoyed".lower() in result.lower():
      print("annoyed")
      img3 = ImageTk.PhotoImage(Image.open(annoyed))
      image_label.configure(image=img3)
      image_label.image = img3
      print("anooyed")
      time.sleep(1)
      image_label.configure(image=img2)
      image_label.image = img2
 #
    elif "Smug".lower() in result.lower():
       print("smug")
       img4 = ImageTk.PhotoImage(Image.open(smug))
       image_label.configure(image=img4)
       image_label.image = img4
       print("smug")
       time.sleep(1)
       image_label.configure(image=img2)
       image_label.image = img2

    
    elif "emptyreaction".lower() in result.lower():
       print("no reactioN!!")
       img4 = ImageTk.PhotoImage(Image.open(reactiones))
       image_label.configure(image=img4)
       image_label.image = img4
       print("noreaction!!")
       time.sleep(1)
       image_label.configure(image=img2)
       image_label.image = img2


    elif "angry".lower() in result.lower():
       print("angry")
       img5 = ImageTk.PhotoImage(Image.open(angry))
       image_label.configure(image=img5)
       image_label.image = img5
       print("angry")
       time.sleep(1)
       image_label.configure(image=img2)
       image_label.image = img2


    elif "fear".lower() in result.lower():
       print("fear!!")
       img6 = ImageTk.PhotoImage(Image.open(fear))
       image_label.configure(image=img6)
       image_label.image = img6
       print("fera!")
       time.sleep(1)
       image_label.configure(image=img2)
       image_label.image = img2

       
    elif "shocked".lower() in result.lower():
       print("shocked")
       img7 = ImageTk.PhotoImage(Image.open(shocked))
       image_label.configure(image=img7)
       image_label.image = img7
       time.sleep(1)
       image_label.configure(image=img2)
       image_label.image = img2




def imagesearch(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": value1,
        "key": value2,
        "searchType": "image",
        "num": 1
    }
    response = requests.get(url, params=params).json()
    try:
        return response["items"][0]["image"]["thumbnailLink"]  # string URL
    except Exception as e:
        print("No image found:", e)
        return None
def search():
    query = entry.get()
    result = imagesearch(query)  
    if result is None:
        print("No image found.")
        return

    img_url = result["thumbnailLink"]  #
    img = download_image(img_url)
    if img is not None:
        popup_image(img, scale_factor=3)
    else:
        print("Failed to download image.")
def download_image(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)

    content_type = response.headers.get("content-type", "")
    if not content_type.startswith("image/"):
        print("Not an image:", content_type)
        return None

    try:
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        return img
    except Exception as e:
        print("Pillow cannot open image:", e)
        return None



def popup_image(img, scale_factor=3):
    win = tk.Toplevel()
    win.wm_title("image")
    win.geometry("300x315")
    max_dim = 800  # max width or height
    w, h = img.size
    scale = min(max_dim / w, max_dim / h, scale_factor)
    img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(win, image=img_tk)
    label.image = img_tk  # keep reference
    label.pack()

    
def talk():
   print("newmessage")
   messagebox.showwarning(name, result)



def open_Toplevel2():  
    
    # Create widget
    top2 = tk.Toplevel() 
    
    # define title for window
    top2.title("Toplevel2")
    
    # specify size
    top2.geometry("330x300")
    
    # Create label
    label2 = tk.Label(top2,
                  text = "the settings menu or some shit i lokey forgot mao")
    color2 = tk.Label(top2,
                  text = "color! use like a hex code or somthing idfk")
    colot = tk.Entry(top2, width=40)
    
    mood1 = tk.Label(top2,
                  text = "mood vaule down!")
    moodt = tk.Entry(top2, width=40)
    
    label3 = tk.Label(top2,
                  text = "name for it ")
    namet = tk.Entry(top2, width=40)
   
    
    # Create exit button.
    button3 = tk.Button(top2, text = "Exit", 
                    command = top2.destroy)
    button_save = tk.Button(
        top2, 
        text="Save", 
        command=lambda: moodcolocha(namet, moodt, colot)
    )
    color2.pack()
    colot.pack(padx=10, pady=10)
    mood1.pack()
    moodt.pack(padx=10, pady=10)
    label3.pack()
    namet.pack(padx=10, pady=10)
    label2.pack()
    button3.pack()
    button_save.pack()
  #  global name 
   # global color
  #  global mood
   # name = namet.get()
   # color = moodt.get()
   # mood = colot.get()
    
    # Display until closed manually.
    top2.mainloop()

def moodcolocha(namet, moodt, colot):
    global name, mood, color, vaulec, vaulem, vaulen, data

    name = namet.get()
    mood = moodt.get()
    color = colot.get()

    vaulec = color
    vaulen = name
    vaulem = mood

    data["name"] = name
    data["mood"] = mood
    data["color"] = color

    root.wm_title(name)
    image_label.configure(bg=color)
    root.configure(bg=color)

    print(f"Saved values -> Name: {name}, Mood: {mood}, Color: {color}")

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# or access fields directly from the response object

################

root.title("test")


# the box!
root.wm_title(name)
img1 = ImageTk.PhotoImage(Image.open(normal))
image_label = tk.Label(root, image=img1)
image_label.configure(bg=color)
image_label.pack(padx=40, pady=15)
entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=10)
button = tk.Button(root, text="Send", command=ollama)
button.pack(padx=10, pady=5)
button2 = tk.Button(root, text="open setting i guess", command=open_Toplevel2)
button2.pack(padx=10, pady=5)
root.configure(bg=color)
root.mainloop()