#!/usr/bin/env python
import sublime, sublime_plugin
import re

# TODO: If line/selection isn't commented, comment it
# TODO: Look at TM_COMMENT_START to figure out actual comment character
class CommentHeaderCommand(sublime_plugin.TextCommand):
    def wrap_comment(self, line):
      line_length = max(len(s) for s in line.split('\n'))
      comment_line = '#' + '-' * (line_length + 1)
      return(comment_line + '\n' + line + '\n' + comment_line)

    def run(self, edit):
      sels = self.view.sel()

      for sel in sels:
        lines = self.view.line(sel)
        wrapped_code = self.wrap_comment(self.view.substr(lines))
        self.view.replace(edit, lines, wrapped_code)
