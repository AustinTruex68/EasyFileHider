import sublime
import sublime_plugin
import json
from collections import OrderedDict


class EasyFileHider(sublime_plugin.TextCommand):
	settingsHolder = 'settingsHolder.json'
	packageSettings = 'EasyFileHider.sublime-settings'
	userSettings = 'Preferences.sublime-settings'
	def run(self, edit):
		settings = '{ "file_exclude_patterns": [] }'
		fep = "file_exclude_patterns"

		def fetch_current_text():
			currentSettings = sublime.load_settings(self.packageSettings)
			return ",".join(map(str, currentSettings.get(fep)))

		def on_done(input_string):
			self.text = input_string
			write_new_set()

		def on_change(input_string):
			print("Input changed: %s " % input_string)

		def on_cancel():
			print("User canceled the input")

		def write_new_set():
			values = self.text.replace(" ", "").split(',')
			values = list(OrderedDict.fromkeys(values))
			if values[0] == "" or values[0] == " ":
				values = []

			uSet = sublime.load_settings(self.userSettings)
			currentSettings = sublime.load_settings(self.packageSettings)
			currentSettings.set(fep, values)
			uSet.set(fep, values)
			sublime.save_settings(self.packageSettings)
			sublime.save_settings(self.userSettings)


		window = self.view.window()
		window.show_input_panel("Files to hide:", fetch_current_text(), on_done, on_change, on_cancel)
