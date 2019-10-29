import glob
from random import randint
from image_utils import get_relevant_image, save_image, load_image


def load_extended_ck_data():
    x, y = [], []
    path = 'data/own/*.png'
    for img_path in sorted(glob.glob(path)):
        img = load_image(img_path)
        img = img.reshape((96, 96, 1))
        x.append(img)
        emotion_index = img_path.find('_', 0) + 1
        y.append(img_path[emotion_index])

    return x, y


def extract_extended_ck_data(path_to_ck_emotions='data/CK+/Emotion/*'):
    def build_paths(subjects):
        paths = dict.fromkeys(subjects)
        for subject in subjects:
            seqs = glob.glob(subject + '/*/*.txt')
            if not seqs:
                paths.pop(subject)
            else:
                paths[subject] = seqs
        return paths

    def extract_seq(subject):
        if len(paths[subject]) == 1:
            seq = paths[subject][0]
            paths[subject].remove(seq)
            return seq
        seq_index = randint(1, len(paths[subject])) - 1
        seq = paths[subject][seq_index]
        paths[subject].remove(seq)
        return seq

    def build_image_path(subject_path, seq, frame):
        return subject_path + '_' + seq + '_' + f"{frame:08d}" + ".png"

    def get_emotion(seq_path):
        with open(seq_path, 'r') as file:
            emotion = int(float(file.read().strip()))
        return emotion

    def fill_data(seq):
        parts = seq.split('_')
        subject_path = parts[0].replace('Emotion', 'cohn-kanade-images')
        last_frame = int(parts[2])
        x.append(get_relevant_image(build_image_path(subject_path, parts[1], 1)))
        x.append(get_relevant_image(build_image_path(subject_path, parts[1], last_frame - 2)))
        x.append(get_relevant_image(build_image_path(subject_path, parts[1], last_frame - 1)))
        x.append(get_relevant_image(build_image_path(subject_path, parts[1], last_frame)))
        emotion = get_emotion(seq)
        y.append(emotion)
        y.append(emotion)
        y.append(emotion)
        y.append(emotion)

    x, y = [], []
    subjects = sorted(glob.glob(path_to_ck_emotions))
    paths = build_paths(subjects)
    while len(paths) != 0:
        o = []
        for i in range(0, 10):
            num_subjects = len(paths)
            subject_shift = 0
            for j in range(0, num_subjects, 10):
                if j + i > num_subjects - 1:
                    i = 10
                    break
                else:
                    subject_index = j + i - subject_shift
                    d = len(list(paths.keys()))
                    subject = list(paths.keys())[subject_index]
                seq = extract_seq(subject)
                fill_data(seq)
                # remove subject if there are no sequences left
                if len(paths[subject]) == 0:
                    paths.pop(subject)
                    print(f'Removed subject: {subject}, Subject lefts: {len(paths)}')
                    subject_shift += 1

    return x, y



