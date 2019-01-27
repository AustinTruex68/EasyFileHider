import sublime
import sublime_plugin
import json
from collections import OrderedDict


class EasyFileHider(sublime_plugin.TextCommand):
	settingsHolder = 'EasyFileHider/settingsHolder.json'
	def run(self, edit):
		settings = '{ "file_exclude_patterns": [] }'
		fep = "file_exclude_patterns"

		def fetch_current_text():
			try:
				fileHolder = open(self.settingsHolder, 'r+')
				setting = json.load(fileHolder)
			except Exception as e:
				fileHolder = open(self.settingsHolder, 'w')
				setting = json.loads(settings)

			return ",".join(map(str, setting[fep]))


		def on_done(input_string):
			self.text = input_string
			write_new_set()

		def on_change(input_string):
			print("Input changed: %s " % input_string)

		def on_cancel():
			print("User canceled the input")

		def write_new_set():
			# open placeholder file
			try:
				fileHolder = open(self.settingsHolder, 'r+')
				setting = json.load(fileHolder)
			except Exception as e:
				fileHolder = open(self.settingsHolder, 'w')
				setting = json.loads(settings)

			# clear out the current file
			fileHolder.close()
			fileHolder = open(self.settingsHolder, 'w')

			# write new to temp file
			values = self.text.replace(" ", "").split(',')
			values = list(OrderedDict.fromkeys(values))

			if values[0] == "" or values[0] == " ":
				setting[fep] = []
			else:
				setting[fep] = values

			json.dump(setting, fileHolder)

			# fetch and save settings
			userSettings = sublime.load_settings("Preferences.sublime-settings")
			userSettings.erase(fep)
			userSettings.set(fep, setting[fep])
			sublime.save_settings("Preferences.sublime-settings")


		window = self.view.window()
		window.show_input_panel("Files to hide:", fetch_current_text(), on_done, on_change, on_cancel)
