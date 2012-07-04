import sublime, sublime_plugin
import re

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class CleanNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Find any string that starts with "## - "
        digits = re.compile("^\\d* - ")
        old_page = ''
        cleaned = ''
        for region in self.view.sel():
            if not region.empty():
                for line in self.view.substr(region).splitlines():
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
                
