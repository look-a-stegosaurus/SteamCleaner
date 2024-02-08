

#   ____  _                          ____ _
#  / ___|| |_ ___  __ _ _ __ ___    / ___| | ___  __ _ _ __   ___ _ __
#  \___ \| __/ _ \/ _` | '_ ` _ \  | |   | |/ _ \/ _` | '_ \ / _ \ '__|
#   ___) | ||  __/ (_| | | | | | | | |___| |  __/ (_| | | | |  __/ |
#  |____/ \__\___|\__,_|_| |_| |_|  \____|_|\___|\__,_|_| |_|\___|_|
#
#
#
#
#                                        ___    ,'""""`.
#                                     ,`""   """"'      `.
#                                    .'        _.         `._
#                                   .'       ,'              `"""`.
#                                  ,'    .-"``.    ,-'            `.
#                _                ,'    (        ,'                :
#               |_|             ,'     ,'           __,            `.     _
#               | |       ,""""'     .' ;-.    ,  ,'  \             `"""`|_|
#              _| |_    ,'           `-(   `._(_,'     )_                | |
#            _| | | | _ '         ,---. \ @ ;   \ @ _,'                 _| |_
#           | | | | |' |         ,'      ,--'-    `;'                 _ | | | |_
#           \          /        ,'      (      `. ,'                 | `| | | | |
#            \        /        ,'        \    _,','                  \          |
#              \    /  / /     ;          `--'  ,'                    \.       /`.
#              ,'\  \./ /     ;          __    (                    ,  \     /  `.
#              ;   \. ./      `____...  `99b   `.                  ,' ./   /    ,'
#              ;    ...----'''' )  _.-  .66P    `.                ,'     /    ,'
# _....----''' '.       __..--"_.-:.-' .'        `.             ,''.   ./`--'
#                  _.--'  _.-'' .-'`-.:..___...--' `-._      ,-"'   `-'
#            _.--'    _.-'    .'   .' .'               `"""""
#     __.-''      _.-'     .-'   .'  /
#  '          _.-' .-'  .-'        .'
#         _.-'  .-'  .-' .'  .'   /
#     _.-'      .-'   .-'  .'   .'
# _.-'       .-.    ,'   .'    /
#        _.-'    .-'   .'    ,'"


import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ExifTags

def extractPixelData(inputImagePath, outputImagePath):
    with Image.open(inputImagePath) as image:
        pixelData = image.getdata()
        newImage = Image.new(image.mode, image.size)
        newImage.putdata(pixelData)
        newImage.save(outputImagePath)

def browseInputFiles():
    inputFilePaths = filedialog.askopenfilenames(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff")]
    )
    fileViewerListbox.delete(0, tk.END)
    for filePath in inputFilePaths:
        fileViewerListbox.insert(tk.END, filePath)

def cleanImages():
    selectedIndices = fileViewerListbox.curselection()
    if not selectedIndices:
        return

    selectedFilePaths = [fileViewerListbox.get(index) for index in selectedIndices]
    for inputFilePath in selectedFilePaths:
        _, extension = os.path.splitext(inputFilePath)
        outputFileName = os.path.basename(inputFilePath) + "_cleaned" + extension
        outputImagePath = os.path.join(outputLocationEntry.get(), outputFileName)
        extractPixelData(inputFilePath, outputImagePath)

    statusLabel.config(text="Images cleaned and saved to: " + outputLocationEntry.get())

def showRawHeaderInfo():
    selectedIndices = fileViewerListbox.curselection()
    if not selectedIndices:
        return

    selectedFilePath = fileViewerListbox.get(selectedIndices[0])
    with Image.open(selectedFilePath) as image:
        headerInfo = f"Image Header Information\n" \
                     f"-------------------------\n" \
                     f"File Name: {os.path.basename(selectedFilePath)}\n" \
                     f"Format: {image.format}\n" \
                     f"Mode: {image.mode}\n" \
                     f"Size: {image.size}\n"
        metadata = image.info
        if metadata:
            headerInfo += f"\nAdditional Metadata:\n"
            for key, value in metadata.items():
                headerInfo += f"{key}: {value}\n"

    headerWindow = tk.Toplevel(window)
    headerWindow.title("Raw Image Header Information")
    headerLabel = tk.Label(headerWindow, text=headerInfo, justify=tk.LEFT)
    headerLabel.pack(padx=10, pady=10)
    writeButton = tk.Button(
        headerWindow, text="Write to File", command=lambda: writeHeaderInfo(headerInfo, selectedFilePath)
    )
    writeButton.pack(padx=10, pady=5)

def parseExifData(exifData):
    parsedExifData = {}
    for tagId, value in exifData.items():
        tagName = ExifTags.TAGS.get(tagId, tagId)
        parsedValue = value
        if tagName == 'MakerNote' and isinstance(value, bytes):
            parsedValue = value.decode('utf-8', 'ignore')
        if tagName == 'UserComment' and isinstance(value, bytes):
            parsedValue = value.decode('utf-8', 'ignore')
        parsedExifData[tagName] = parsedValue
    return parsedExifData

def showParsedHeaderInfo():
    selectedIndices = fileViewerListbox.curselection()
    if not selectedIndices:
        return
    selectedFilePath = fileViewerListbox.get(selectedIndices[0])
    with Image.open(selectedFilePath) as image:
        exifData = image._getexif()
        parsedExifData = parseExifData(exifData) if exifData else {}
    headerWindow = tk.Toplevel(window)
    headerWindow.title("Parsed Image Header Information")
    headerInfo = f"Image Header Information\n" \
                 f"-------------------------\n" \
                 f"File Name: {os.path.basename(selectedFilePath)}\n" \
                 f"Format: {image.format}\n" \
                 f"Mode: {image.mode}\n" \
                 f"Size: {image.size}\n"
    if parsedExifData:
        headerInfo += f"\nParsed EXIF Data:\n"
        for tagName, value in parsedExifData.items():
            headerInfo += f"{tagName}: {value}\n"
    headerLabel = tk.Label(headerWindow, text=headerInfo, justify=tk.LEFT)
    headerLabel.pack(padx=10, pady=10)
    writeButton = tk.Button(
        headerWindow, text="Write to File", command=lambda: writeParsedHeaderInfo(parsedExifData, selectedFilePath)
    )
    writeButton.pack(padx=10, pady=5)

def writeHeaderInfo(headerInfo, selectedFilePath):
    outputFilePath = selectedFilePath + "_headerinfo.txt"
    with open(outputFilePath, "w") as outputFile:
        outputFile.write(headerInfo)
    statusLabel.config(text="Raw header information written to: " + outputFilePath)

def writeParsedHeaderInfo(parsedExifData, selectedFilePath):
    outputFilePath = selectedFilePath + "_parsedheaderinfo.txt"
    with open(outputFilePath, "w") as outputFile:
        outputFile.write("Parsed Image Header Information\n")
        outputFile.write("-------------------------\n")
        for tagName, value in parsedExifData.items():
            outputFile.write(f"{tagName}: {value}\n")
    statusLabel.config(text="Parsed header information written to: " + outputFilePath)

def browseOutputLocation():
    outputDirectoryPath = filedialog.askdirectory()
    outputLocationEntry.delete(0, tk.END)
    outputLocationEntry.insert(tk.END, outputDirectoryPath)

window = tk.Tk()
window.title("Image Header Cleaner")
inputFilesLabel = tk.Label(window, text="Input Files:")
inputFilesLabel.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
fileViewerListbox = tk.Listbox(window, selectmode=tk.MULTIPLE, width=50)
fileViewerListbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W + tk.E)
fileViewerScrollbar = tk.Scrollbar(window)
fileViewerScrollbar.grid(row=1, column=2, sticky=tk.N + tk.S)
fileViewerListbox.config(yscrollcommand=fileViewerScrollbar.set)
fileViewerScrollbar.config(command=fileViewerListbox.yview)
browseInputButton = tk.Button(window, text="Browse", command=browseInputFiles)
browseInputButton.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
outputLocationLabel = tk.Label(window, text="Output Location:")
outputLocationLabel.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
outputLocationEntry = tk.Entry(window, width=40)
outputLocationEntry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
browseOutputButton = tk.Button(window, text="Browse", command=browseOutputLocation)
browseOutputButton.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
cleanButton = tk.Button(window, text="Clean Images", command=cleanImages)
cleanButton.grid(row=4, column=1, padx=10, pady=10)
headerInfoButton = tk.Button(window, text="Show Raw Header Info", command=showRawHeaderInfo)
headerInfoButton.grid(row=5, column=0, padx=10, pady=5)
parsedHeaderInfoButton = tk.Button(window, text="Show Parsed Header Info", command=showParsedHeaderInfo)
parsedHeaderInfoButton.grid(row=5, column=1, padx=10, pady=5)
statusLabel = tk.Label(window, text="")
statusLabel.grid(row=6, column=0, columnspan=3, padx=10, pady=5)
window.mainloop()
