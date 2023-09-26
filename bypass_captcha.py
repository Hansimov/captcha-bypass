import pyautogui
import cv2
from pathlib import Path
from PIL import Image, ImageGrab
from mss import mss


class ImageMatcher:
    def __init__(self, source_image_path, template_image_path):
        self.source_image = cv2.imread(str(source_image_path))
        self.template_image = cv2.imread(str(template_image_path))

    def match(self):
        """
        OpenCV: Template Matching
        * https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html

        Return: (left, top, right, bottom)
        """
        res = cv2.matchTemplate(
            self.source_image, self.template_image, cv2.TM_CCOEFF_NORMED
        )
        _, _, _, match_location = cv2.minMaxLoc(res)
        match_left = match_location[0]
        match_top = match_location[1]
        match_right = match_location[0] + self.template_image.shape[1]
        match_bottom = match_location[1] + self.template_image.shape[0]
        match_region = (match_left, match_top, match_right, match_bottom)

        self.match_region = match_region
        return match_region

    def draw_rectangle(self):
        cv2.rectangle(
            img=self.source_image,
            pt1=self.match_region[:2],
            pt2=self.match_region[2:],
            color=(0, 255, 0),
            thickness=2,
        )  # BGR
        # return rectangle_region

    def display(self):
        cv2.imshow("Detected", self.source_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class CaptchaBypasser:
    def __init__(self):
        self.captcha_image_path = (
            Path(__file__).parent / "captcha-verify-you-are-human.png"
        )
        self.screen_shot_image_path = Path(__file__).parent / "screenshot.png"

    def get_screen_shots(self):
        ImageGrab.grab(all_screens=True).save(self.screen_shot_image_path)

    def get_captcha_location(self):
        with mss() as sct:
            all_monitor = sct.monitors[0]
            # print(all_monitor["top"], all_monitor["left"])
            monitor_top = all_monitor["top"]
            monitor_left = all_monitor["left"]

        image_matcher = ImageMatcher(
            source_image_path=self.screen_shot_image_path,
            template_image_path=self.captcha_image_path,
        )

        match_region = image_matcher.match()
        image_matcher.draw_rectangle()
        image_matcher.display()
        # print(self.captcha_location)


if __name__ == "__main__":
    captcha_bypasser = CaptchaBypasser()
    captcha_bypasser.get_screen_shots()
    captcha_bypasser.get_captcha_location()
