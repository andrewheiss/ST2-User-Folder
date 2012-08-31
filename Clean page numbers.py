import sublime, sublime_plugin
import re

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class PrepareNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text = re.sub("\\* Text Note, page (\\d{1,5})\\n", "\\1 - ", text)
                self.view.replace(edit, region, text)

class CleanNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        digits = re.compile("^\\d* - ")  # Find any string that starts with "## - "
        old_page = ''
        cleaned = ''
        for region in self.view.sel():
            if not region.empty():
                # Find/replace all the Skim junk (* Text Note, page 5) with cleaner text (5 - )
                text = self.view.substr(region)
                text = re.sub("\\* Text Note, page (\\d{1,5})\\n", "\\1 - ", text)

                # for line in self.view.substr(region).splitlines():
                for line in text.splitlines():
                    check_for_digits = digits.match(line)

                    if check_for_digits:
                        current_page = check_for_digits.group(0)

                        if current_page == old_page:
                            line = digits.sub('', line)
                            cleaned += line + '\n'
                        else:
                            old_page = current_page
                            cleaned += line + '\n'
                    else:
                        cleaned += line + '\n'
                self.view.replace(edit, region, cleaned.rstrip('\n'))  # rstrip removes trailing newlines
                
