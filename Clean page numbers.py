import sublime, sublime_plugin
import re


# Clean page numbers from notes exported from Skim
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
                text = re.sub("\\* Anchored Note, page (\\d{1,5})\\n", "\\1 - ", text)
                # text = re.sub("\\* Highlight, page (\\d{1,5})\\n", "\\1 - ", text)
                text = re.sub("\\* Highlight, page (\\d{1,5})\\n(.*)\\n", "\\1 - \"\\2\"\\n", text)

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


# Convert page numbers from two-page PDFs in Skim to page ranges (1 -> 1-2; 2 -> 3-4; etc.)
# Run this after cleaning Skim's cruftiness with CleanNumbersCommand()
# TODO: Incorporate this into regular clean function
class CleanSpreadNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def clean_spreads(input_offset):
            digits = re.compile("^\\d* - ")
            cleaned = ''
            offset = int(input_offset) * 2
            for region in self.view.sel():
                if not region.empty():
                    text = self.view.substr(region)

                    for line in text.splitlines():
                        check_for_digits = digits.match(line)

                        if check_for_digits:
                            found_number = re.search("^(\\d{1,5}) - ", line)
                            number = int(found_number.group(1))
                            page_number = number + number - offset  # number + number - offset
                            spread_numbers = '{0}-{1} - '.format(page_number, page_number+1)
                            fixed_line = re.sub("^(\\d{1,5}) - ", spread_numbers, line)
                            cleaned += fixed_line + "\n"
                        else:
                            cleaned += line + "\n"
                    
                    self.view.replace(edit, region, cleaned)

        self.view.window().show_input_panel("First absolute page number:", '', clean_spreads, None, None)     
