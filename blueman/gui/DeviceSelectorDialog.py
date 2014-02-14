import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk
from gi.repository import GObject
from blueman.gui.DeviceSelectorWidget import DeviceSelectorWidget


class DeviceSelectorDialog(Gtk.Dialog):
    def __init__(self, title=_("Select Device"), parent=None, discover=True):

        GObject.GObject.__init__(self, title, parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                                                     Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))

        self.set_has_separator(False)
        self.props.resizable = False
        self.props.icon_name = "blueman"
        self.selector = DeviceSelectorWidget()
        self.selector.show()

        #self.selector.destroy()
        #self.selector = None

        align = Gtk.Alignment.new(0.5, 0.5, 1.0, 1.0)
        align.add(self.selector)

        align.set_padding(6, 6, 6, 6)
        align.show()
        self.vbox.pack_start(align, True, True, 0)


        #(adapter, device)
        self.selection = None

        self.selector.List.connect("device-selected", self.on_device_selected)
        self.selector.List.connect("adapter-changed", self.on_adapter_changed)
        if discover:
            self.selector.List.DiscoverDevices()

        self.selector.List.connect("row-activated", self.on_row_activated)

    def on_row_activated(self, treeview, path, view_column, *args):
        self.response(Gtk.ResponseType.ACCEPT)

    def on_adapter_changed(self, devlist, adapter):
        self.selection = None

    def on_device_selected(self, devlist, device, iter):
        self.selection = (devlist.Adapter.GetObjectPath(), device)

    def GetSelection(self):
        if self.selection:
            return (self.selection[0], self.selection[1].Copy())
        else:
            return None
		

