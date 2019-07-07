from PIL import Image, ImageFont, ImageDraw
from random import choice as rand_choice, randint
from data import *
import wave
import subprocess
import os


def gen_flag_sequence(flags, times, repeat_colours=True, enforce_only_one_name_for_white=False):
    white_reset = rand_choice(whites)
    white_control = Colour(255, 255, 255)

    last_info = None
    sequence_build = []
    for flag_ind in range(times):
        chosen_flag = rand_choice(flags)
        chosen_info = rand_choice(chosen_flag.segments)

        if enforce_only_one_name_for_white:
            if chosen_info.colour == white_control:
                chosen_info = white_reset

        if not repeat_colours:
            last_info = chosen_info

            while chosen_info.colour == last_info.colour:
                chosen_flag = rand_choice(flags)
                chosen_info = rand_choice(chosen_flag.segments)

                if enforce_only_one_name_for_white:
                    if chosen_info.colour == white_control:
                        chosen_info = white_reset

        sequence_build.append(chosen_info)
        last_info = chosen_info

    return sequence_build


def create_wave_hamburger(sequence, path):
    wave_data = []
    sequence.insert(0, "pause")
    sequence.insert(0, "pause")
    sequence.append("pause")

    for part in sequence:
        wave_open = wave.open("v_{}.wav".format(part), "rb")
        wave_data.append([wave_open.getparams(), wave_open.readframes(wave_open.getnframes())])
        wave_open.close()

    output = wave.open(path, 'wb')
    output.setparams(wave_data[0][0])
    for part in wave_data:
        output.writeframes(part[1])
    output.close()


def compose_text_from_sequence(sequence):
    string_build = ""
    for info_part in sequence:
        string_build += info_part.name


def interpret_hamburger(string):
    build_str = ""
    sequence = []
    total_height = 0

    for char in string:
        build_str += char
        if build_str in burger_list:
            sequence.append(build_str)
            total_height += burger_list[build_str]

            build_str = ""

    return sequence, total_height


def gen_vertical_hamburger(length, path, wav_path):
    # find the sum of all parts then add together
    sequence = []
    total_height = 0

    if isinstance(length, int):
        for part in range(length):
            sequence.append(rand_choice(list(burger_list.keys())))
            total_height += burger_list[sequence[part]]
    elif isinstance(length, str):
        sequence, total_height = interpret_hamburger(length)

    image_dimensions = (100 + (20 * len(sequence)), (total_height + 120) + (total_height % 2))
    image = Image.new("RGB", image_dimensions, (255, 255, 255))
    image_draw = ImageDraw.Draw(image)

    offset = total_height + 50
    sequence.reverse()
    for part in sequence:
        img_path = "b_{}.png".format(part)
        paste_img = Image.open(img_path)

        image.paste(paste_img, ((image_dimensions[0] // 2) - 56, offset - paste_img.height), paste_img)
        offset -= burger_list[part]

    sequence.reverse()
    name_build = "".join(part for part in sequence)

    text_font = ImageFont.truetype("calibri.ttf", 24)
    w, h = image_draw.textsize(name_build, font=text_font)
    image_draw.text(((image_dimensions[0] - w) / 2,
                     total_height + 70),
                    name_build, fill="black", font=text_font)

    image.save(path)
    create_wave_hamburger(sequence, wav_path)


def gen_image_from_sequence(sequence, path):
    # 200 high, 100 long for each colour
    image_dimensions = (100 * (len(sequence) + 1), 420)

    image = Image.new("RGB", image_dimensions, (255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    name_build = ""
    for seg_index, seg_info in enumerate(sequence):
        image_draw.rectangle(((50 + 100 * seg_index, 50), (150 + 100 * seg_index, 250)),
                             fill=seg_info.colour.colour_tuple)

        name_build += seg_info.name

    image_draw.line(((50, 300), (image_dimensions[0] - 50, 300)), fill="black", width=3)

    image_draw.line(((49, 49), (49, 251)), fill="black", width=1)
    image_draw.line(((51 + 100 * len(sequence), 49), (51 + 100 * len(sequence), 251)), fill="black", width=1)
    image_draw.line(((50, 49), (image_dimensions[0] - 50, 49)), fill="black", width=1)
    image_draw.line(((50, 251), (image_dimensions[0] - 50, 251)), fill="black", width=1)

    text_font = ImageFont.truetype("calibri.ttf", 48)
    w, h = image_draw.textsize(name_build, font=text_font)
    image_draw.text(((image_dimensions[0] - w) / 2,
                     333),
                    name_build, fill="black", font=text_font)

    image.save(path)


# input burger
#gen_vertical_hamburger(input("enter burger>> "), "test_input_burger.jpg", "test_wave_burger.wav")
#subprocess.call("d:/ffmpeg/bin/ffmpeg -loop 1 -y -i test_input_burger.jpg -i test_wave_burger.wav -shortest test_video_burger.mp4", shell=True)

# video burger
for i in range(250):
    gen_vertical_hamburger(3 + (i // 25), "the burger folder videos/test_input_burger.jpg", "the burger folder videos/test_wave_burger.wav")
    subprocess.call(
        "d:/ffmpeg/bin/ffmpeg -loop 1 -y -i \"the burger folder videos/test_input_burger.jpg\" -i \"the burger folder videos/test_wave_burger.wav\" -shortest \"the burger folder videos/video_burger_{}.mp4\"".format(i + 1),
        shell=True, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

os.remove("the burger folder videos/test_input_burger.jpg")
os.remove("the burger folder videos/test_wave_burger.wav")

file = open("mylist.txt", "w")
file.write("\n".join("file \'the burger folder videos/video_burger_{}.mp4\'".format(i + 1) for i in range(250)))
file.close()

subprocess.call("d:/ffmpeg/bin/ffmpeg -f concat -safe 0 -i mylist.txt -c copy video_burger_combine.mp4")

os.remove("mylist.txt")

# burger generation
#for i in range(500):
#    gen_vertical_hamburger(3 + (i // 20), "the burger folder//burger_test_{}.png".format(i + 1))

# flag generation
#for i in range(1000):
#    info_sequence = gen_flag_sequence(flag_list, 3 + (i // 10), False, True)
#    gen_image_from_sequence(info_sequence, "the flag folder//test_flag_img{}.png".format(i + 1))
