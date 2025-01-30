import json
import os
import pickle

import cv2 as cv


class Image:
    def __init__(self, image_data, meta_data=None):
        self._image_data = image_data
        self._meta_data = meta_data
        self._pickle_path = None

    @property
    def to_numpy(self):
        return self._image_data

    @property
    def meta_data(self):
        return self._meta_data

    def _show(self):
        t_frame = cv.resize(self.to_numpy, (512, 512))
        cv.imshow("Test", t_frame, )

    def print_metadata(self):
        print('meta data: ')
        if self._meta_data is not None:
            print(json.dumps(self._meta_data, indent=4, sort_keys=True))
        else:
            print('meta data not present')

    def show(self, time_ms=0):
        self._show()
        cv.waitKey(time_ms)

    def pickle_dump(self, filename):
        self._pickle_path = filename
        pickle.dump(self, open(self._pickle_path, "wb"))

    # get image in cv format
    def preview_get(self):
        data = self._image_data
        if 'pixel_format' in self._meta_data:
            pixel_format = self.meta_data['pixel_format']
            if pixel_format == 'BayerRG8':
                data = cv.cvtColor(data, cv.COLOR_BAYER_RG2RGB)
            if pixel_format == 'YUV422Packed':
                data = cv.cvtColor(data, cv.COLOR_YUV2RGB_UYVY)
        return data

    def preview_save(self, filename):
        data = self.preview_get()
        cv.imwrite(filename, data)

    def metadata_json_dump(self, filename, pickle_path=None):
        output_json = {}
        with open(filename, 'w') as file:
            output_json.update({'meta_data': self._meta_data})
            if pickle_path is not None:
                output_json.update({'pickle_path': pickle_path})
            elif self._pickle_path is not None:
                output_json.update({'pickle_path': self._pickle_path})
            json.dump(output_json, file, indent=4, sort_keys=True)

    def dump(self, image_name):
        self.pickle_dump(image_name + ".pkl")
        self.metadata_json_dump(image_name + '.json')

    @staticmethod
    def from_pickle(filename):
        image = pickle.load(open(filename, "rb"))
        return image

    @staticmethod
    def from_numpy(filename):
        image_data = cv.imread(filename=filename)
        image = Image(image_data)
        return image

    @staticmethod
    def from_file(filepath, meta_data=None):
        image_numpy = cv.imread(filepath)
        image = Image(image_data=image_numpy,
                      meta_data=meta_data)
        return image


class ImageHelpers:
    @staticmethod
    def acquisition_properties(exposure_time_ms=None, gain_db=None, device_temperature=None):
        properties = {}
        if exposure_time_ms is not None:
            properties.update({'exposure_time_ms': exposure_time_ms})
        if gain_db is not None:
            properties.update({'gain_db': gain_db})
        if device_temperature is not None:
            properties.update({'device_temperature': device_temperature})

        return properties

    @staticmethod
    def agromax_filename_parse(filename):
        properties_array = filename.split('.jpg')[0].split('_')
        meta_data = {}
        if len(properties_array) > 5:
            meta_data.update({"type": "sample"})
            meta_data.update({properties_array[3]: [float(properties_array[4]),
                                                    float(properties_array[5]),
                                                    float(properties_array[6])]})
            meta_data.update({properties_array[7]: float(properties_array[8])})
            meta_data.update({properties_array[9]: float(properties_array[10])})
            meta_data.update({properties_array[11]: {"top": [
                float(properties_array[12]),
                float(properties_array[13]),
                float(properties_array[14])
            ],
                "bottom": [
                    float(properties_array[15]),
                    float(properties_array[16]),
                    float(properties_array[17])
                ]}})
        elif len(properties_array) > 1:
            meta_data.update({"type": "mask"})
            meta_data.update({"name": filename.split('.png')[0]})
        else:
            meta_data.update({"type": "None"})
            meta_data.update({"name": filename.split('.png')[0]})

        return meta_data

    @staticmethod
    def image_from_agromax_file(path, filename):
        image_numpy = cv.imread(os.path.join(path, filename))
        meta_data = ImageHelpers.agromax_filename_parse(filename)
        return Image(image_data=image_numpy,
                     meta_data=meta_data)
