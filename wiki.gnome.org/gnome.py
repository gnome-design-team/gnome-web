# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - GNOME theme

    Based on rightsidebar theme,
      Created by and for crw.
      Later it was rewritten by Nir Soffer for MoinMoin release 1.3.
      Copyright: 2005 by Nir Soffer

    Later is was rewritten for GNOME layout by Frederic Peters.

    @copyright: 2005 by Nir Soffer, 2007 by Frederic Peters, 2013 by William Jon McCann
    @license: GNU GPL, see COPYING for details.  
"""

from MoinMoin.theme import ThemeBase
from MoinMoin.parser.text_moin_wiki import Parser
from MoinMoin import macro
from MoinMoin import i18n, wikiutil, config, version
from MoinMoin.Page import Page
import sys, re, cStringIO

class Theme(ThemeBase):

    name = 'gnome'

    def __init__(self, request):
        ThemeBase.__init__(self, request)
        _ = self.request.getText
	_ = lambda x: x
	self.icons['diffrc'] = (_('Diffs'), 'gnome-moin-diff.png', 16, 16)
        self.icons.update({
                'attach': ('%(attach_count)s', 'mail-attachment-symbolic.png', 16, 16),
                'bottom': (_('[BOTTOM]'), 'go-bottom-symbolic.png', 16, 16),
                'deleted': (_('[DELETED]'), 'edit-delete-symbolic.png', 16, 16),
                'diff': (_('Diffs'), 'gnome-moin-diff.png', 16, 16),
                'diffrc': (_('[DIFF]'), 'gnome-moin-diff.png', 16, 16),
                'edit': (_('Edit'), 'text-editor-symbolic.png', 16, 16),
                'find': ('%(page_find_page)s', 'edit-find-symbolic.png', 16, 16),
                'help': ('%(page_help_contents)s', 'help-browser-symbolic.png', 16, 16),
                'home': (_('Home'), 'go-home-symbolic.png', 16, 16),
                'interwiki': ('[%(wikitag)s]', 'send-to-symbolic.png', 16, 16),
                'new': (_('[NEW]'), 'gnome-moin-new.png', 16, 16),
                'print': (_('Print'), 'printer-symbolic.png', 16, 16),
                'rss': (_('[RSS]'), 'gnome-moin-rss.png', 16, 16),
                'searchbutton': ('[?]', 'edit-find-symbolic.png', 16, 16),
                'top': (_('[TOP]'), 'go-top-symbolic.png', 16, 16),
                'updated': (_('[UPDATED]'), 'view-refresh-symbolic.png', 16, 16),
                'www': ('[WWW]', 'web-browser-symbolic.png', 16, 16),
                '/!\\': ("/!\\", 'dialog-warning-symbolic.png', 16, 16),
                '(!)': ("(!)", 'dialog-information-symbolic.png', 16, 16),
                '<!>': ("<!>", 'dialog-question-symbolic.png', 16, 16),
                '(./)': ("(./)", 'object-select-symbolic.png', 16, 16)
                 })

    # Squash the "fancy links" abomination. This is to some extent
    # a work-around for a Moin-1.3.5 bug where the user preference
    # doesn't work, but I don't want people to *ever* see them.
    def make_icon(self, icon, vars=None):
        if icon == 'www' or icon == 'mailto':
            return ''
        else:
            return ThemeBase.make_icon(self, icon, vars)

    def startPage(self):
        """ Start page div with page language and direction
        
        @rtype: unicode
        @return: page div with language and direction attribtues
        """
        if self.request.form.get('action', [''])[0] == 'edit':
            startpage = u'<div class="body editor"%s>\n' % self.content_lang_attr()
        else:
            startpage = u'<div class="body"%s>\n' % self.content_lang_attr()
        return startpage


    def splitNavilink(self, text, localize=1):
        pagename, link = ThemeBase.splitNavilink(self, text, localize = localize)
        return (pagename, re.sub(r'(<a.*?>)(.*)(</a>)', r'\1<span>\2</span>\3', link))

    def tabs(self, d):
        ### based on ThemeBase.navibar
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']

        # Process config navi_bar
        if request.cfg.navi_bar:
            for text in request.cfg.navi_bar:
                pagename, link = self.splitNavilink(text)
                if pagename == current:
                    cls = 'wikilink selected'
                else:
                    cls = 'wikilink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Add user links to wiki links, eliminating duplicates.
        userlinks = request.user.getQuickLinks()
        for text in userlinks:
            # Split text without localization, user knows what he wants
            pagename, link = self.splitNavilink(text, localize=0)
            if not pagename in found:
                if pagename == current:
                    cls = 'userlink selected'
                else:
                    cls = 'userlink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Add current page at end
        if not current in found:
            title = d['page'].split_title(request)
            title = self.shortenPagename(title)
            link = d['page'].link_to(request, title)
            link = re.sub(r'(<a.*?>)(.*)(</a>)', r'\1<span>\2</span>\3', link)
            cls = 'selected'
            items.append(item % (cls, link))

        # Assemble html
        items = u''.join(items)
        html = u'''
<div id="tabs">
  <ul id="portal-globalnav">
%s
  </ul>
</div> <!-- end of #tabs -->
''' % items
        return html



    def header(self, d):
        """
        Assemble page header
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText

        html = [
            u'''
  <div id="container">
  <div id="header">
    <!-- global gnome.org domain bar -->
    <div id="global_domain_bar">
      <div id="header_tabs">
        <div id="user_tab" class="tab">''',
            self.username(d),
            u'''
        </div>
        <div id="site_tab" class="tab">
          <a class="root" href="http://www.gnome.org/">GNOME.org</a>
        </div>
      </div>
    </div>
  </div>
<!-- end site header -->
  <div id="main_content">
''',

            self.msg(d),
            
            # Page
            self.startPage(),
            ]
        return u'\n'.join(html)

    def editorheader(self, d):
        _ = self.request.getText
        title = _('Edit "%(pagename)s"') % {'pagename': d['page'].split_title(self.request)}
        return u'\n'.join([self.header(d),
                u'<h1 class="editortitle">%s</h1>' % title])

    def footer_editbar(self, d):
        # Only show an editbar for logged-in users
        if (self.request.user.valid):
            html = [
                u'<div id="footer_edit">',
                self.editbar(d),
                u'</div>'
                ]
            return u'\n'.join(html)
        else:
            return u''
    
    def footer(self, d, **keywords):
        """ Assemble wiki footer
        
        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']

        html = [

            # End of page
            self.pageinfo(page),
            self.endPage(),

            # Post footer custom html
            #self.emit_custom_html(self.cfg.page_footer2),
            
            u'''

  <!-- end of main content -->
  </div>
  <!-- site footer -->
  <div id="footer">
    <!-- footer image -->
    <div id="footer_image">
      &nbsp;
    </div>
    <!-- footer grass -->
    <div id="footer_grass">
      &nbsp;
    </div>
    <div id="footer_container">
      <div id="footer_content">''',
            self.footer_editbar(d),
            u'''
        <div id="search">''',
            self.searchform(d),
            u'''
        </div>
        <div id="copyright">
        Copyright &copy; 2005 - 2013 <a href="http://www.gnome.org/">The GNOME Project</a>.
        Hosted by <a href="http://www.redhat.com/">Red Hat</a>.
        </div>
      </div>
    </div>
  </div>
  <!-- End of footer -->
  </div>
  <!-- End of container -->'''

            ]
        return u'\n'.join(html)
    

def execute(request):
    """ Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

class IncludeParser:
    def __init__(self, request, page):
        self.parser = Parser("", request)
        # Format the empty string, making it set its internal data (ugh!).
        out = cStringIO.StringIO()
        backup = sys.stdout, request.write
        sys.stdout, request.write = out, out.write
        self.parser.format(page.formatter)
        sys.stdout, request.write = backup
        self.include_re = re.compile("\[\[Include(?:\(.*?\))?\]\]")
        self.macro = macro.Macro(self.parser)

        # This is really deep and cool black magic. Basically, it creates
        # a local copy of the function macro.Include.execute that behaves
        # exactly like the original one, but with a different "Page"
        # global. This allows us to follow changes in the Include macro
        # without much trouble.
        from MoinMoin.macro.Include import execute
        func_globals = {}
        func_globals.update(execute.func_globals)
        class IncludePage(Page):
            incparser = self
            def send_page(self, request, msg=None, **keywords):
                request.write(self.incparser._parse(self.get_raw_body()))
        func_globals["Page"] = IncludePage
        self.execute = new.function(execute.func_code, func_globals,
                                    execute.func_name,
                                    execute.func_defaults)
