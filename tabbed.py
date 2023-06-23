import wx
import wx.aui  # Advanced User Interface
import numpy as np

class ImagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set up an image.
        height = 300
        width = 300
        n_channels = 3

        # Generate random image data.  This creates a 2D numpy array of shape 300x300x3, where n=3 for RGB.
        image_data = np.random.randint(0, 256, size=(height, width, n_channels), dtype=np.uint8)

        # Create a new wx.Image object using the image_data.
        image = wx.Image(width, height, image_data.tobytes())

        # Create a wx.StaticBitmap control to display the image.
        bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image))

        # Create a wx.Slider for brightness control
        slider_label = wx.StaticText(self, wx.ID_ANY, "Brightness")
        slider = wx.Slider(self, wx.ID_ANY, 0, -255, 255, style=wx.SL_HORIZONTAL)

        # Define an event handler.
        def on_slider_change(event):
            brightness = slider.GetValue()
            adjusted_image_data = np.clip(image_data + brightness, 0, 255).astype(np.uint8)
            updated_image = wx.Image(width, height, adjusted_image_data.tobytes())
            bitmap.SetBitmap(wx.Bitmap(updated_image))
            self.Layout()

        # Bind the event handler to the slider's EVT_SCROLL event.
        slider.Bind(wx.EVT_SCROLL, on_slider_change)

        # Create a vertical sizer and add the controls
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(slider_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        sizer.Add(slider, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        self.SetSizerAndFit(sizer)


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Image Display")

        # Create an AuiNotebook (tabbed panel) to hold multiple panels
        self.notebook = wx.aui.AuiNotebook(self)

        # Create the first tab and add the ImagePanel to it
        tab1 = ImagePanel(self.notebook)
        self.notebook.AddPage(tab1, "Tab 1")

        # Create additional tabs and add panels as needed
        # tab2 = ImagePanel(self.notebook)
        # self.notebook.AddPage(tab2, "Tab 2")
        # ...

        # Create a vertical sizer to hold the notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)


app = wx.App()
frame = MainFrame(None)
frame.Show()
app.MainLoop()
