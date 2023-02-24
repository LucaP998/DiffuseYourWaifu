import random
import os
import shutil
import logging
from dotenv import load_dotenv
from PIL import Image
from instagrapi import Client
from .ig_costants import names, surnames, hashtag_ai, hashtag_anime
from .settings import DEBUG


load_dotenv()


class NoWaifuFound(Exception):
    pass


class NoWaifuUploaded(Exception):
    pass

class WaifuDirectoryNotExists(Exception):
    pass


class DiffuseYourWaifu():
    _client = None
    DEFAULT_IMAGE_TODO_FOLDER = "./img_todo"
    DEFAULT_IMAGE_DONE_FOLDER = "./img_done"

    def __init__(self, username, password):
        self.username = username
        self.password = password

        if not os.path.exists(self.DEFAULT_IMAGE_TODO_FOLDER):
            os.makedirs(self.DEFAULT_IMAGE_TODO_FOLDER)
        if not os.path.exists(self.DEFAULT_IMAGE_DONE_FOLDER):
            os.makedirs(self.DEFAULT_IMAGE_DONE_FOLDER)

    @property
    def client(self):
        if not self._client:
            self._client = Client()
            self._client.login(self.username, self.password)
        return self._client

    def _get_full_name(self):
        return f"{random.choice(names)} {random.choice(surnames)}"

    def _get_hashtag(self):
        return "{} {}".format(
            hashtag_ai,
            random.choice(hashtag_anime)
        )

    def get_post_description(self, show_name=True, show_hashtag=True, extra_hashtag=[]):
        return "{name}\n\n{hashtag} {extra}".format(
            name=self._get_full_name() if show_name else '',
            hashtag=self._get_hashtag() if show_hashtag else '',
            extra=' '.join(extra_hashtag)
        )


    def correct_hashtags(self, extra_hashtags):
        corrected_hashtag_list =[]
        for hashtag in extra_hashtags:
            corrected_hashtag_list.append(f"#{extra_hashtags}")
        return corrected_hashtag_list

    def _get_random_photo(self):
        for file_path in os.listdir(self.DEFAULT_IMAGE_TODO_FOLDER):
            if file_path.lower().endswith("jpg"):
                return f"{self.DEFAULT_IMAGE_TODO_FOLDER}/{file_path}"
            if file_path.lower().endswith("png"):
                path = f"{self.DEFAULT_IMAGE_TODO_FOLDER}/{file_path}"
                image_to_convert = Image.open(path)
                rgb_image = image_to_convert.convert('RGB')
                new_path = path.replace('png', 'jpg').replace(
                    'PNG', 'jpg')  # ugly
                rgb_image.save(new_path)
                os.remove(path)
                return new_path

        raise NoWaifuFound(
            f'No waifu found in {self.DEFAULT_IMAGE_TODO_FOLDER}')

    def _move_photo_to_done(self, path):
        shutil.move(path, os.path.join(self.DEFAULT_IMAGE_DONE_FOLDER))
        print(f"\n\nimage successfully moved to {self.DEFAULT_IMAGE_DONE_FOLDER} folder")

    def upload_photo(self, image_path=None, extra_hashtag=[]):
        if not image_path:
            image_path = self._get_random_photo()

        if not os.path.exists(image_path):
            raise WaifuDirectoryNotExists()

        description = self.get_post_description(extra_hashtag=extra_hashtag)
        print(f'Upload WAIFU from: {image_path}\n\nPOST:\n\n{description}')
        if not DEBUG:
            uploaded_media = self.client.photo_upload(image_path, description)
            if not uploaded_media:
                raise NoWaifuUploaded
            print(f"\n\nwaifu successfully uploaded to url: https://www.instagram.com/p/{uploaded_media.code}/")

        self._move_photo_to_done(image_path)


diffuse_your_waifu_client = DiffuseYourWaifu(os.getenv("INSTAGRAM_USERNAME"),
                                             os.getenv("INSTAGRAM_PASSWORD"))
