from extract_data import extract_extended_ck_data
from image_utils import save_image

x, y = extract_extended_ck_data()

for i in range(len(x)):
    path = f'data/own/{i}_{y[i]}.png'
    save_image(x[i], path)