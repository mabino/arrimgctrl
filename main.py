import wx
import numpy as np

# Set up an image.
height = 300
width = 300
n_channels = 3

# Generate random image data.  This creates a 2D numpy array of shape 300x300x3, where the n=3 for RGB.
image_data = np.random.randint(0, 256, size=(height, width, n_channels), dtype=np.uint8)
print(image_data.shape)

# Create a new wx.Image object using the image_data.
image = wx.Image(width, height, image_data.tobytes())

# Create a wx App object, a Frame object and use the wx.StaticBitmap control to display the image.

app = wx.App()
frame = wx.Frame(None, title="Image Display")
bitmap = wx.StaticBitmap(frame, wx.ID_ANY, wx.Bitmap(image))

# Create a wx.Slider for brightness control
slider_label = wx.StaticText(frame, wx.ID_ANY, "Brightness")
slider = wx.Slider(frame, wx.ID_ANY, 0, -255, 255, style=wx.SL_HORIZONTAL)

# Define an event handler.

def on_slider_change(event):
    brightness = slider.GetValue()
    adjusted_image_data = np.clip(image_data + brightness, 0, 255).astype(np.uint8)
    updated_image = wx.Image(width, height, adjusted_image_data.tobytes())
    bitmap.SetBitmap(wx.Bitmap(updated_image))
    frame.Layout()

# Bind the event handler to an event, in this case the slider's EVT_SCROLL such that it will be called.
slider.Bind(wx.EVT_SCROLL, on_slider_change)

# Create a vertical sizer and add the controls
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
sizer.Add(slider_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)
sizer.Add(slider, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
frame.SetSizerAndFit(sizer)

frame.Show()
app.MainLoop()
