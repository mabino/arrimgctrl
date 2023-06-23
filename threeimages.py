import wx
from PIL import Image, ImageEnhance

class ImagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_path = ""
        self.gamma = 1.0

        self.slider = wx.Slider(self, value=100, minValue=1, maxValue=200, style=wx.SL_HORIZONTAL)
        self.slider.Bind(wx.EVT_SCROLL, self.on_slider_scroll)

        self.image_ctrl = wx.StaticBitmap(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.slider, 0, wx.EXPAND)
        sizer.Add(self.image_ctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def set_image(self, image_path):
        self.image_path = image_path
        self.update_image()

    def update_image(self):
        image = Image.open(self.image_path)

        # Calculate the available space for the image
        tab_size = self.GetParent().GetClientSize()
        max_width = tab_size.GetWidth()
        max_height = tab_size.GetHeight() - self.slider.GetSize().GetHeight()

        # Calculate the scaled dimensions while maintaining the aspect ratio
        image_ratio = image.width / image.height
        display_ratio = max_width / max_height

        if image_ratio > display_ratio:
            scaled_width = max_width
            scaled_height = int(max_width / image_ratio)
        else:
            scaled_width = int(max_height * image_ratio)
            scaled_height = max_height

        scaled_image = image.resize((scaled_width, scaled_height), Image.ANTIALIAS)
        enhanced_image = self.adjust_gamma(scaled_image, self.gamma)
        bitmap = self.image_to_bitmap(enhanced_image)
        self.image_ctrl.SetBitmap(bitmap)
        self.Refresh()

    def adjust_gamma(self, image, gamma):
        enhancer = ImageEnhance.Brightness(image)
        enhanced_image = enhancer.enhance(gamma)
        return enhanced_image

    def image_to_bitmap(self, image):
        width, height = image.size
        image = image.convert("RGB")
        data = image.tobytes()
        bitmap = wx.Bitmap.FromBuffer(width, height, data)
        return bitmap

    def on_slider_scroll(self, event):
        self.gamma = self.slider.GetValue() / 100.0
        self.update_image()

    def OnSize(self, event):
        self.update_image()
        event.Skip()


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.tab_ctrl = wx.Notebook(self)

        self.image_panel_1 = ImagePanel(self.tab_ctrl)
        self.image_panel_2 = ImagePanel(self.tab_ctrl)
        self.image_panel_3 = ImagePanel(self.tab_ctrl)

        self.tab_ctrl.AddPage(self.image_panel_1, "Image 1")
        self.tab_ctrl.AddPage(self.image_panel_2, "Image 2")
        self.tab_ctrl.AddPage(self.image_panel_3, "Image 3")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.tab_ctrl, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.image_panel_1.set_image("image1.jpg")
        self.image_panel_2.set_image("image2.jpg")
        self.image_panel_3.set_image("image3.jpg")

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.Layout()
        event.Skip()


if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow(None, "Image Viewer")
    frame.Show()

    app.MainLoop()
