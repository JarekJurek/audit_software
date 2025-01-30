import errno
import json
import os
import pickle

import cv2 as cv

from .image import Image


class ImageSeries:
    FILE_NAME_GEN = 'ogx_image_'

    def __init__(self, series_dir, meta_data, cache_size=1):
        self._images = []
        self._cache = []
        self._dir = series_dir
        self._meta_data = meta_data

        self._cache_size = cache_size
        self._counter = 0

        self._iter_counter = 0
        if not os.path.exists(self._dir):
            try:
                os.makedirs(self._dir)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if not os.path.exists(os.path.join(self._dir, 'images')):
            try:
                os.makedirs(os.path.join(self._dir, 'images'))
                os.makedirs(os.path.join(self._dir, 'preview'))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def __iter__(self):
        self._iter_counter = 0
        return self

    def __next__(self):
        if (self._iter_counter >= len(self)):
            raise StopIteration
        self._iter_counter += 1
        return self[self._iter_counter - 1]

    @property
    def meta_data(self):
        return self._meta_data

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, value):
        self._dir = value

    def __len__(self):
        return len(self._images) + len(self._cache)

    def __getitem__(self, item):
        if item < len(self._images):
            return Image.from_pickle(os.path.join(self._dir, 'images', self._images[item] + '.pkl'))
        elif item < len(self):
            index = item - len(self._images)
            return self._cache[index]
        else:
            raise RuntimeError('Index out of range')

    def remove(self, index):
        if item < len(self._images):
            os.remove(os.path.join(self._dir, 'images', self._images[item] + '.pkl'))
            del self._images[index]
        elif item < len(self):
            index = item - len(self._images)
            del self._cache[index]
        else:
            raise RuntimeError('Index out of range')

    def find_image(self, key, value):
        for img in self._images:
            with open(os.path.join(self._dir, 'images', img + '.json'), 'r') as file:
                meta_data = json.load(file)
                if key in meta_data['meta_data']:
                    if value == meta_data['meta_data'][key]:
                        return Image.from_pickle(
                            os.path.join(self._dir, 'images', img + '.pkl')), self._images.index(img)
        return None

    def find_image_criteria(self, criteria):
        for img in self._images:
            with open(os.path.join(self._dir, 'images', img + '.json'), 'r') as file:
                meta_data = json.load(file)
                guard = True
                for key, value in criteria:
                    if key not in meta_data['meta_data']:
                        guard = False
                        break
                    if value != meta_data['meta_data'][key]:
                        guard = False
                        break
                if guard:
                    return Image.from_pickle(os.path.join(self._dir, 'images', img + '.pkl'))
        return None

    def images_exist(self):
        for img in self._images:
            if not os.path.exists(os.path.join(self._dir, 'images', img + '.pkl')):
                return False
        return True

    def _dequeue_cache(self):
        file_name = self.FILE_NAME_GEN + str(self._counter)
        path = os.path.join(self._dir, 'images', file_name)
        img = self._cache.pop()
        self._images.append(file_name)
        img.dump(path)
        self._counter += 1

    def save_cache(self):
        while len(self._cache) > 0:
            self._dequeue_cache()

    def append(self, image):
        if len(self._cache) == self._cache_size:
            self._dequeue_cache()
        self._cache.insert(0, image)

    def metadata_json_dump(self):
        output_json = {}
        with open(os.path.join(self._dir, 'series_metadata.json'), 'w') as file:
            output_json.update({'meta_data': self._meta_data})
            json.dump(output_json, file, indent=4, sort_keys=True)

    def dump(self, save_preview=True):
        self.save_cache()
        images_meta_data = {}
        for img in self._images:
            with open(os.path.join(self._dir, 'images', img + '.json'), 'r') as file:
                meta_data = json.load(file)
                images_meta_data.update({img: meta_data})
            if save_preview:
                ogx_image = Image.from_pickle(os.path.join(self._dir, 'images', img + '.pkl'))
                ogx_image.preview_save(os.path.join(self._dir, 'preview', img + '.jpg'))

        self._meta_data.update({'image_meta_data': images_meta_data})
        self.metadata_json_dump()
        pickle.dump(self, open(os.path.join(self._dir, 'series.pkl'), "wb"))

    def get_image(self, idx):
        img_name = self._images[idx]
        img_path = os.path.join(self._dir, 'images', img_name + '.pkl')
        ogx_image = Image.from_pickle(img_path)

        cv_img = ogx_image.preview_get()
        return cv_img, img_name

    def preview(self, preview_size=(512, 512)):
        if len(self._images) == 0:
            return

        font = cv.FONT_HERSHEY_SIMPLEX
        idx_prev = -1
        idx = 0
        while True:
            if idx_prev != idx:
                cv_img, img_name = self.get_image(idx)

                img_resized = cv.resize(cv_img, preview_size)
                if idx == 0:
                    cv.putText(img_resized, 'press \'a\' or \'d\' keys to navigate', (10, 20), font, 0.5,
                               (255, 255, 255))
                cv.putText(img_resized, img_name + '.pkl', (10, img_resized.shape[0] - 10), font, 0.5, (255, 255, 255))

            cv.imshow('ogx_image', img_resized)
            key = cv.waitKey(50)

            if key == ord('d'):
                idx = idx + 1
                if idx >= len(self._images):
                    idx = 0
            elif key == ord('a'):
                idx = idx - 1
                if idx < 0:
                    idx = len(self._images) - 1
            elif key == 27:
                break

    @staticmethod
    def from_pickle(series_dir):
        image_series = pickle.load(open(os.path.join(series_dir, 'series.pkl'), "rb"))
        image_series.dir = series_dir
        if not image_series.images_exist():
            raise RuntimeError('Series is incomplete!; unable to load properly')
        return image_series
