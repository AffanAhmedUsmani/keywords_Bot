

from pathlib import Path
from tkinter import INSERT, Tk, Canvas, END, Entry, Text, Button, PhotoImage, filedialog
from calendar import WEDNESDAY
import requests
from selenium import webdriver
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from numpy import append
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("700x600")
window.configure(bg="#FFFFFF")


class gui:
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        700.0,
        600.0,
        fill="#C2B3B3",
        outline="")

    canvas.create_text(
        1205.0,
        727.0,
        anchor="nw",
        text="Start || >",
        fill="#FFFFFF",
        font=("Inter Bold", 24 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        380.0,
        383.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        highlightthickness=0
    )
    entry_1.place(
        x=220.5,
        y=360.0,
        width=319.0,
        height=45.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        380.0,
        455.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        highlightthickness=0
    )
    entry_2.place(
        x=220.5,
        y=432.0,
        width=319.0,
        height=45.0
    )

    canvas.create_text(
        11.0,
        369.0,
        anchor="nw",
        text="Excel File Path :",
        fill="#010101",
        font=("Inter Bold", 24 * -1)
    )

    canvas.create_text(
        11.0,
        449.0,
        anchor="nw",
        text="Keyword :",
        fill="#010101",
        font=("Inter Bold", 24 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        348.5,
        190.0,
        image=entry_image_3
    )
    entry_3 = Text(
        bd=0,
        foreground="green",
        bg="#010101",
        highlightthickness=0
    )
    entry_3.place(
        x=11.0,
        y=50.0,
        width=675.0,
        height=278.0
    )

    canvas.create_text(
        11.0,
        29.0,
        anchor="nw",
        text="Running Log :\n",
        fill="#FFFFFF",
        font=("Inter ExtraBold", 15 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: File_dialog(),
        relief="flat"
    )
    button_1.place(
        x=572.0,
        y=369.0,
        width=114.0,
        height=29.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: start(),
        relief="flat"
    )
    button_2.place(
        x=70.0,
        y=521.0,
        width=132.0,
        height=29.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: savefile(),
        relief="flat"
    )
    button_3.place(
        x=499.0,
        y=521.0,
        width=132.0,
        height=29.0
    )


obj = gui()
Names = []
Websites = []
Emails = []
Phones = []


def File_dialog():
    filename = filedialog.askdirectory()
    obj.entry_1.insert(0, filename)

    return None


def start():
    if obj.entry_2 != None:
        name = obj.entry_2.get()
        url = 'https://www.google.com/maps/search/'+name
        # PATH = "chromedriver.exe"
        # driver = webdriver.Chrome(PATH)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=option)
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        if soup.find("h1", {"class": "DUwDvf"}):
            h1 = soup.find("h1", {"class": "DUwDvf"})
            business = h1.find_all("span")[0].string
            Names.append(business)
            divs = soup.find_all("div", {"class": "Io6YTe"})
            found = False
            for div in divs:
                if re.match(r"[\d\s\+\(\)]+", div.string):
                    found = True
                    Phones.append(div.string)
                    break
            if not found:
                Phones.append("")
            if soup.find("div", {"class": "ITvuef"}):
                div = soup.find("div", {"class": "ITvuef"})
                website = "https://www." + \
                    div.find("div", {"class": "Io6YTe"}).string
                Websites.append(website)
                req = requests.get(website)
                htmlContent = req.content
                websoup = BeautifulSoup(htmlContent, 'html.parser')
                EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
                email = re.compile(EMAIL_REGEX)
                matches = email.finditer(websoup.get_text())
                found = False
                for match in matches:
                    Emails.append(match.group())
                    found = True
                    break
                if not found:
                    Emails.append("")
            else:
                Websites.append("")
                Emails.append("")
        else:
            text = "No business found \n"
            obj.entry_3.insert(INSERT, text)
            obj.entry_3.yview(END)
            window.update()
    else:
        text = "\n enter a keyword to start \n"
        obj.entry_3.insert(INSERT, text)
        obj.entry_3.yview(END)
        window.update()


def savefile():
    d = {'Business Name': Names, 'Website': Websites,
         'Phone Numer': Phones, 'Email': Emails}
    df = pd.DataFrame(data=d)
    path = obj.entry_1.get()
    df.to_excel("{}/results.xlsx".format(path))


window.resizable(False, False)
window.mainloop()
