#!/usr/bin/python
# -*- coding: utf-8 -*-

# Generador de nombres aleatorios para pnj para partidas de rol
# Idea de Desmenbrator
# Programado por Alfonso Saavedra "Son Link"
# Bajo licencia GPL 3

import sys, os, random, gtk, gobject
from optparse import OptionParser
import gettext
import locale
	 
gettext.textdomain("programita")  
gettext.bindtextdomain("programita", "./locale")
_ = gettext.gettext     

class GUI():
	def __init__(self):
		# Comprobamos antes de nada que los 2 directorios existen y que tienen permisos de ejecucion
		if not os.access('nombres', os.R_OK) or not os.access('apellidos', os.R_OK):
			print 'No tienes permisos de lectura en los directorios'
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
			liststore.append(['es', _('Español')])
			liststore.append(['jp', _('Japones')])
			liststore.append(['en', _('Ingles')])
			liststore.append(['pt', _('Portugués')])
			liststore.append(['ge', _('Alemán')])
			liststore.append(['fr', _('Francés')])
			liststore.append(['it', _('Italiano')])
			liststore.append(['ru', _('Ruso')])
			liststore.append(['ma', _('Musulmán')])
			liststore.append(['ch', _('Chino')])
			
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
			
			total_label = gtk.Label(str=_('Total a generar (1-100):'))
			sex_label.set_alignment(0, 0)
			vbox.pack_start(total_label, False, False, 0)

			self.total_value = gtk.SpinButton()
			self.total_value.set_range(1, 100)
			self.total_value.set_increments(1.0, 5.0)
			vbox.pack_start(self.total_value, False, False, 0)
			
			generate = gtk.Button(label=_('Generar listado'))
			generate.connect('clicked', self.generar)
			vbox.pack_start(generate, False, False, 0)
			
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
		
	def generar(self, w):
		if not self.lang_select.get_active_text() or not self.sex_select.get_active_text():
			self.error_dialog(_('Debes de seleccionar el idioma y el sexo'))
		else:
			lang = self.lang_select.get_active_text()
			sex = self.sex_select.get_active_text()
			total = int(self.total_value.get_text())
			# Comprobamos antes si existen los archivos
			txt_names = 'nombres/'+sex+'_'+lang+'.txt'
			txt_lastnames = 'apellidos/'+lang+'.txt'
			try:
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
					name = list_names[n].split()[0]+" "+list_lastnames[m].split()[0]
					i += 1
					iter = self.textbuffer.get_end_iter()
					self.textbuffer.insert(iter, name+"\n")
						
				names.close()
				lastnames.close()
				self.save.set_sensitive(True)
						
			except:
				self.error_dialog(_('No se pudieron abrir los archivos de texto.\nComprueba que están en los directorios correspondientes, que los nombres sean los correctos y/o que tengas permisos de lectura sobre ellos'))
				
	def save_on_file(self, w):
		try:
			txt = self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter())
			select_files = gtk.FileChooserDialog(title='Seleccione los ficheros a reproducir',action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_SAVE,gtk.RESPONSE_OK, gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
			select_files.set_current_folder(os.environ['HOME'])
			response = select_files.run()
			if response == gtk.RESPONSE_OK:
				select_files.hide()
				if os.path.exists(select_files.get_filenames()[0]):
					warning = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_YES_NO, message_format=_("¡Atención!"))
					warning.format_secondary_text(_('El archivo ya existe.\n¿Desea sobreescribirlo?'))
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
		info.set_version('1 Beta 3')
		info.set_license('GNU/GPL v3')
		info.set_comments(_("Gracias a Desmenbrator por la idea.\nA javierrivera2 por sus consejos para mejorar el código\nY como no, a todos vosotros por descargarlo y usarlo ^^"))
		#info.set_website('http://github.com/son-link/RedImages-2')
		#info.set_artists(['Otakon','Son Link'])
		info.set_translator_credits(_('Ingles: Son Link y Google'))
		#info.set_website_label(_("The proyect website"))
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

GUI()
gtk.main()
