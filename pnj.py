#!/usr/bin/env python
# Note: if you use Arch Linux, add the number 2 at the end of python -> python2
# -*- coding: utf-8 -*-

# Generador de nombres aleatorios para pnj para partidas de rol
# Idea de Desmenbrator
# Programado por Alfonso Saavedra "Son Link"
# Bajo licencia GPL 3

import random, gtk, sys
import gettext, locale
from os import access, path, R_OK

APP = 'pnj'
gettext.textdomain (APP)
gettext.bindtextdomain (APP, './locale')
_ = gettext.gettext
gettext.install(APP, './locale', unicode=1)

loc = locale.getdefaultlocale()[0]
if loc.find('es') == -1:
	# Si el idioma del sistema no es el español en cualquiera de sus variantes, se coge el ingles por defecto
	lang = gettext.translation(APP, './locale', languages=['en'])
	lang.install()

class GUI():
	def __init__(self):
		# Comprobamos antes de nada que los 2 directorios existen y que tienen permisos de ejecucion
		if not access('names', R_OK) or not access('lastnames', R_OK):
			self.error_dialog(_('No tienes permisos de lectura en las carpeta names y/o lastnames\nCompruebe los permisos'))
			sys.exit(1)
		else:
			mainwin = gtk.Window()
			mainwin.set_title(_('Generador de nombres aleatorios para PNJs'))
			mainwin.set_position(gtk.WIN_POS_CENTER_ALWAYS)
			mainwin.set_default_size(400,300)
			
			hbox = gtk.HBox(homogeneous=False)
			
			vbox = gtk.VBox()
			
			lang_label = gtk.Label(str=_('Elija el idioma:'))
			lang_label.set_alignment(0, 0)
			vbox.pack_start(lang_label, False, False, 0)
			
			liststore = gtk.ListStore(str, str)
			self.lang_select = gtk.ComboBox(liststore)
			cell = gtk.CellRendererText()
			self.lang_select.pack_start(cell, True)
			self.lang_select.add_attribute(cell, 'text', 1)
			liststore.append(['es', _(u'Español')])
			liststore.append(['jp', _('Japones')])
			liststore.append(['en', _('Ingles')])
			liststore.append(['pt', _(u'Portugués')])
			liststore.append(['ge', _(u'Alemán')])
			liststore.append(['fr', _(u'Francés')])
			liststore.append(['it', _('Italiano')])
			liststore.append(['ru', _('Ruso')])
			liststore.append(['ma', _(u'Musulmán')])
			liststore.append(['ch', _('Chino')])
			self.lang_select.connect('changed', self.check_combobox)
			
			vbox.pack_start(self.lang_select, False, False, 0)
			
			sex_label = gtk.Label(str=_('Elija el sexo:'))
			sex_label.set_alignment(0, 0)
			vbox.pack_start(sex_label, False, False, 0)
			
			liststore2 = gtk.ListStore(str, str)
			self.sex_select = gtk.ComboBox(liststore2)
			cell2 = gtk.CellRendererText()
			self.sex_select.pack_start(cell2, True)
			self.sex_select.add_attribute(cell2, 'text', 1)
			liststore2.append(['m', _('Masculino')])
			liststore2.append(['f', _('Femenino')])
			vbox.pack_start(self.sex_select, False, False, 0)
			self.sex_select.connect('changed', self.check_combobox)
			
			total_label = gtk.Label(str=_('Total a generar (1-100):'))
			sex_label.set_alignment(0, 0)
			vbox.pack_start(total_label, False, False, 0)

			self.total_value = gtk.SpinButton()
			self.total_value.set_range(1, 100)
			self.total_value.set_increments(1.0, 5.0)
			vbox.pack_start(self.total_value, False, False, 0)
			
			self.generate = gtk.Button(label=_('Generar listado'))
			self.generate.connect('clicked', self.generar)
			self.generate.set_sensitive(False)
			vbox.pack_start(self.generate, False, False, 0)
			
			self.save = gtk.Button(label=_('Guardar'))
			self.save.set_sensitive(False)
			self.save.connect('clicked', self.save_on_file)
			vbox.pack_start(self.save, False, False, 0)
			
			info = gtk.Button(label=_('Sobre'))
			info.connect('clicked', self.view_info)
			vbox.pack_start(info, False, False, 0)
			
			hbox.pack_start(vbox, False, False, 0)
			
			textview_container = gtk.ScrolledWindow()
			self.textview = gtk.TextView()
			self.textview.set_editable(False)
			textview_container.add(self.textview)
			hbox.add(textview_container)
			
			mainwin.add(hbox)
			mainwin.show_all()
			mainwin.connect('destroy', self.destroy)
		
	def generar(self, w):
		lang = self.lang_select.get_active_text()
		sex = self.sex_select.get_active_text()
		total = int(self.total_value.get_text())
		# Comprobamos antes si existen los archivos
		txt_names = 'names/'+sex+'_'+lang+'.txt'
		txt_lastnames = 'lastnames/'+lang+'.txt'
		if access(txt_names, R_OK) or access(txt_lastnames, R_OK):
			self.textview.set_buffer(None)
			self.textbuffer = self.textview.get_buffer()
			names = open(txt_names, 'r')
			list_names = names.readlines()
			lastnames = open(txt_lastnames, 'r')
			list_lastnames = lastnames.readlines()
			i = 1
			for i in range(0, total):
				n = random.randint(0, len(list_names[1:]))
				m = random.randint(0, len(list_lastnames[1:]))
				name = list_names[n].split()[0]
				lastname = list_lastnames[m].split()[0]
				if lang == 'ru' and sex == 'f' and lastname.endswith('ov') or lastname.endswith('ev') or lastname.endswith('in'):
					fullname = list_names[n].split()[0]+" "+list_lastnames[m].split()[0]+'a'
				else:
					fullname = list_names[n].split()[0]+" "+list_lastnames[m].split()[0]
				i += 1
				iter = self.textbuffer.get_end_iter()
				self.textbuffer.insert(iter, fullname+"\n")
						
			names.close()
			lastnames.close()
			self.save.set_sensitive(True)
				
		else:
			self.error_dialog(_('No se pudieron abrir los archivos de texto.\nCompruebe que estén en los directorios correspondientes, que los nombres sean los correctos y/o que tenga permisos de lectura sobre ellos'))
				
	def save_on_file(self, w):
		try:
			txt = self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter())
			select_files = gtk.FileChooserDialog(title=_('Seleccione donde se guardaran los nombres'),action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_SAVE,gtk.RESPONSE_OK, gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
			response = select_files.run()
			if response == gtk.RESPONSE_OK:
				select_files.hide()
				if path.exists(select_files.get_filenames()[0]):
					warning = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_YES_NO, message_format=_("¡Atención!"))
					warning.format_secondary_text(_(u'El archivo ya existe.\n¿Desea sobreescribirlo?'))
					def close(w, res):
						if res == gtk.RESPONSE_NO:
							w.hide()
						elif res == gtk.RESPONSE_YES:
							w.hide()
							f = open(select_files.get_filenames()[0], 'w')
							f.write(txt)
							f.close()
							
					warning.connect("response", close)
					warning.run()
				else:
					f = open(select_files.get_filenames()[0], 'w')
					f.write(txt)
					f.close()
			else:
				select_files.hide()
		except IOError:
			self.error_dialog(_('Ocurrió un error al guardar el archivo.\nCompruebe que tienes permisos de escritura en el directorio'))
			
	def view_info(self, widget):
		# esta funcion se limita a mostrar y cerrar el dialogo de la info
		info = gtk.AboutDialog()
		info.set_name(_('Generador de nombres aleatorios para PNJs'))
		info.set_version('1.0')
		f = open('COPYING', 'r')
		info.set_license(f.read())
		info.set_comments(_(u"Gracias a Desmenbrator por la idea.\nA javierrivera2 por sus consejos para mejorar el código\nY como no, a todos vosotros por descargarlo y usarlo ^^"))
		info.set_website('http://sonlinkblog.blogspot.com')
		info.set_translator_credits(_('Ingles: Son Link y Google'))
		info.set_website_label(_("Pagina del proyecto"))
		def close(w, res):
			w.hide()
		info.connect("response", close)
		info.run()
				
	def error_dialog(self, message):
		warning = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK, message_format=_("¡Error!"))
		warning.format_secondary_text(message)
		def close(w, res):
			w.hide()
		warning.connect("response", close)
		warning.run()
		
	def check_combobox(self, w):
		if self.lang_select.get_active_text() and self.sex_select.get_active_text():
			self.generate.set_sensitive(True)
	
	def destroy(self, w):
		gtk.main_quit()

if __name__ == "__main__":
    GUI()
    gtk.main()
