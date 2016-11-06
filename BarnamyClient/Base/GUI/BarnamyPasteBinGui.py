



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class BarnamyPasteBinGui(Gtk.ApplicationWindow):

    def __init__(self, Base, parent_win_entry):
        self.BarnamyBase = Base
        self.parent_win_entry = parent_win_entry
        Gtk.Window.__init__(self)
        self.resize(800, 600)
        self.connect('delete-event', self.hide_pastebin_window)
        self.barnamy_pixbuf = GdkPixbuf.Pixbuf.new_from_file("Theme/GuiGtk/B7_100x102.png")
        self.set_icon(self.barnamy_pixbuf)
        self.selected_paste_bin = None
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Barnamy PasteBin"
        self.set_titlebar(hb)
        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        paste_bin_bt = Gtk.Button('Send')
        paste_bin_bt.connect('clicked', self.on_paste_bin_bt_clicked)
        self.set_border_width(10)
        paste_bin_store = Gtk.ListStore(str)
        paste_bin_store.append(["bpaste"])
        paste_bin_store.append(["fpaste"])
        paste_bin_cb = Gtk.ComboBox.new_with_model(paste_bin_store)
        paste_bin_cb.connect("changed", self.on_paste_bin_cb_changed)
        renderer_text = Gtk.CellRendererText()
        paste_bin_cb.pack_start(renderer_text, True)
        paste_bin_cb.add_attribute(renderer_text, "text", 0)
        self.paste_bin_text = Gtk.TextView()
        scrolledwindow.add(self.paste_bin_text)
        vbox1.pack_start(paste_bin_cb, False, False, 0)
        vbox1.pack_start(scrolledwindow, True, True, 0)
        vbox1.pack_start(paste_bin_bt, False, False, 0)
        self.add(vbox1)

    def hide_pastebin_window(self, widget, event):
        self.hide()
        return True

    def on_paste_bin_cb_changed(self, widget):

        tree_iter = widget.get_active_iter()
        if tree_iter != None:
            model = widget.get_model()
            paste_bin = model[tree_iter][0]
            self.selected_paste_bin = paste_bin

    def on_paste_bin_bt_clicked(self, widget):
        date = []
        textbuffer = self.paste_bin_text.get_buffer() 
        startiter, enditer = textbuffer.get_bounds() 
        text = textbuffer.get_text(startiter, enditer, True) 
        if self.selected_paste_bin == 'bpaste':
            data = ['bpaste', text]
        elif self.selected_paste_bin == 'fpaste':
            data = ['fpaste', self.BarnamyBase.nick, 'Barnamy pastebin', text]
        url = self.BarnamyBase.barnamy_actions['paste_bin'](data)
        self.parent_win_entry.set_text(url)
        textbuffer.set_text('')
        self.hide()

