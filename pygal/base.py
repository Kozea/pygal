

class BaseGraph(object):
    """Graphs commons"""

    def render(self):
        self.draw()
        return self.svg.render()

    def _in_browser(self):
        from lxml.html import open_in_browser
        self.draw()
        open_in_browser(self.svg.root, encoding='utf-8')
