import sublime, sublime_plugin
from subprocess import Popen, PIPE

path_to_cleanup_script = "/Users/andrew/Library/Application Support/MultiMarkdown/Utilities/table_cleanup.pl"

def _pipe_through_mmd_script(text):
	pipe = Popen([path_to_cleanup_script], stdin=PIPE, stdout=PIPE)
	pipe.stdin.write(text)
	pipe.stdin.close()
	return pipe.stdout.read()

class CleanTableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
            	selectText = self.view.substr(region)
                self.view.replace(edit, region, _pipe_through_mmd_script(selectText))
			# if region.empty():
			#     lineRegion = self.view.line(region)
			#     lineText = self.view.substr(lineRegion)