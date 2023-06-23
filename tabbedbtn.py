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

        self.notebook = wx.aui.AuiNotebook(self)
        tab1 = ImagePanel(self.notebook)
        self.notebook.AddPage(tab1, "Tab 1")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)

        # Add a button to create an additional tab
        self.add_tab_button = wx.Button(self, wx.ID_ANY, "Add Tab")
        sizer.Add(self.add_tab_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizerAndFit(sizer)

        # Bind an event handler to the button
        self.add_tab_button.Bind(wx.EVT_BUTTON, self.on_add_tab)

    def on_add_tab(self, event):
        # Create a new tab and add it to the notebook
        new_tab = ImagePanel(self.notebook)
        self.notebook.AddPage(new_tab, "New Tab")
        self.Layout()


app = wx.App()
frame = MainFrame(None)
frame.Show()
app.MainLoop()
