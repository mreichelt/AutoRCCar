from pathlib import Path
import cv2
import pygame
import glob
import shutil

NUM_KEYS = [getattr(pygame, 'K_' + str(num)) for num in range(10)]


def main():
    pygame.init()
    for file in glob.glob('training_images/*.jpg'):
        image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        try:
            label = label_image(image)
        except KeyboardInterrupt:
            break

        if label < 0:
            continue

        save(
            image=file,
            label=chr(label),
        )

    cv2.destroyAllWindows()
    cv2.waitKey(0)


def save(image, label, root=Path('labeled_images')):
    if isinstance(root, str):
        root = Path(root)
    root = root / label
    root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image, str(root))


def await_key():
    while True:
        # noinspection PyArgumentList
        for _ in pygame.event.get(pygame.KEYDOWN):
            pressed = pygame.key.get_pressed()
            pressed_nums = list(filter(lambda key: pressed[key], NUM_KEYS))
            if len(pressed_nums) == 1:
                return pressed_nums[0]

            if pressed[pygame.K_s]:
                return -1
            if pressed[pygame.K_ESCAPE] or pressed[pygame.K_x] or pressed[pygame.K_q]:
                raise KeyboardInterrupt


def label_image(image):
    cv2.imshow('to-label', image)
    key = await_key()
    return key


if __name__ == '__main__':
    main()
