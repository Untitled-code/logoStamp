from PIL import Image

def imagesConcatenate(bg, overlay, directory, timestamp):
    width, height = bg.size #getting size of background
    bg = bg.convert("RGBA")
    overlay = overlay.convert("RGBA")
    if width > height: #for horizontal picture
        bg.paste(overlay, (1100, (height - 150)), overlay)
    elif height > width: #for vertical picture
        bg.paste(overlay, ((width - 400), 1350), overlay)

    print(f"Final picture is: Width:{width} and height:{height}")
    # bg.show()
    bg.save(f"{directory}/fp_logo{timestamp}.jpg", format="png")
    # return whole_image

def changeImageSize(image):
    width, height = image.size  # measure size
    print(f"Background image is: Width:{width} and height:{height}")
    maxSize = 1500
    if width > height:
        ratio = maxSize / image.size[0]
    elif height > width:
        ratio = maxSize / image.size[1]
    newWidth = int(ratio * image.size[0])
    newHeight = int(ratio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def main(file, directory, timestamp):
    background = Image.open(file)
    overlay = Image.open("./nikcenter-logo1.png")
    bg = changeImageSize(background)  # changing size proportianlly woth new width
    imagesConcatenate(bg, overlay, directory, timestamp)


if __name__ == "__main__":
    main(filename, directory, timestamp)