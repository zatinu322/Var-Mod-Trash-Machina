import random
import math

OFFSETS_EXE = {
    # low_fuel_threshold
    0x124CCD: "0x009E5980",
    }


def generate_offsets():
    offsets = {
        "render": generate_render_quality(),
        "gravity": generate_gravity(),
        "fov": generate_fov(),
        "armor": generate_armor()
    }

    return offsets


def generate_render_quality():
    res = [16, 32, 64, 128, 256]
    rand_512 = res[random.randint(1, 4)]

    models_render = {
        0x30808B: rand_512,  # model rendering
        0x308092: rand_512,  # same as previous
    }

    return models_render


def generate_gravity():
    rand_300 = float(random.randint(40, 300))
    rand_grav = float(random.randint(-20, -2))

    gravity = {
        0x124CF1: rand_300,
        0x202D25: rand_grav,
    }

    return gravity


def generate_fov():
    rand_aspect = random.uniform(0.2, 0.95)
    aspect_ratio = 16 / 9
    target_fov_x_deg = 90.0
    target_fov_x_rads = math.radians(target_fov_x_deg)
    target_fov_y_rads = 2 * math.atan(
        math.tan(target_fov_x_rads / 2) * (1 / aspect_ratio)
    )
    coeff_fov_x_from_y = target_fov_x_rads / target_fov_y_rads

    fov = {
        # aspect
        0x5E5A74: rand_aspect,  # 009E5A74
        0x1D7CB: "0x009E5A74",  # 009E5A74
        # aspect ratio hack for Frustum Culling
        # fov_x passed to CClipper::CreateScreenFrustums
        0x3A6128: target_fov_x_rads,
        # hacked "aspect_ratio" coeff to calc fov_y
        0x5E497C: coeff_fov_x_from_y,
    }

    return fov


def generate_armor():
    colors = [
        "fc93e5", "d126ac", "e180db", "c664b1", "c664c3", "df45bd",
        "f7df47", "fac04e", "6ab8b3", "94aba1", "ff6a46", "84bd9b",
        "e1f9ca", "80a4b7", "b4d9d7", "9e1b32", "6dc6e7", "747679",
        "005072", "b5bf00", "ea6529", "003f90", "26a894", "203345",
        "94aba1", "b9b2ad", "b7d1ce", "72e3dc", "f05081", "b96b85",
        "048399", "7b5037", "9d8161", "4f493f", "969286", "5f5a4d",
        "908471", "c1b59f", "e3ded1", "9f8170", "646f87", "008aff",
        "85e6ff", "ffe9fa", "c61548", "ff3200", "257b9c", "b3d2d5"
    ]

    sexy_armor_color = {
        0x11CD4F: generate_color(colors),
        0x11CD62: generate_color(colors),
        0x11CD75: generate_color(colors),
        0x11CD88: generate_color(colors),
        0x11CD9B: generate_color(colors),
        0x11CDAE: generate_color(colors),
        0x11CDC1: generate_color(colors),
        0x11CDD4: generate_color(colors),
        0x11CDE7: generate_color(colors),
        0x11CE0D: generate_color(colors),
        }

    return sexy_armor_color


def generate_color(colors_list):
    hex_number = colors_list[random.randint(0, len(colors_list) - 1)]
    hex_number = "ff" + hex_number

    return hex_number
