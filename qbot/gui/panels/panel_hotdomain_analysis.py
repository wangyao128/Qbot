
import wx

from qbot.common.file_utils import extract_content
from qbot.common.logging.logger import LOGGER as logger
from qbot.common.macros import strategy_choices
from qbot.gui import gui_utils
from qbot.gui.config import DATA_DIR_BKT_RESULT
from qbot.gui.elements.def_dialog import MessageDialog
from qbot.gui.widgets.widget_web import WebPanel


def OnBkt(event):
  wx.MessageBox("ok")

class PanelHotdomainAnalysis(wx.Panel):
  def __init__(self, parent=None, id=-1, displaySize=(1600, 900)):
    super(PanelHotdomainAnalysis, self).__init__(parent)
    self.hotdomain_opts = {
      "hot_date": "2025-06-12",
    }

  def _init_para_notebook(self):
    # 创建参数区面板
    self.ParaNoteb = wx.Notebook(self)
    self.ParaStPanel = wx.Panel(self.ParaNoteb, -1)  # 行情
    self.ParaBtPanel = wx.Panel(self.ParaNoteb, -1)  # 回测 back test
    self.ParaPtPanel = wx.Panel(self.ParaNoteb, -1)  # 条件选股 pick stock
    self.ParaPaPanel = wx.Panel(self.ParaNoteb, -1)  # 形态选股 patten

    # 第二层布局
    self.ParaStPanel.SetSizer(self.add_stock_para_lay(self.ParaStPanel))
    self.ParaBtPanel.SetSizer(self.add_backt_para_lay(self.ParaBtPanel))
    # self.ParaPtPanel.SetSizer(self.add_pick_para_lay(self.ParaPtPanel))
    # self.ParaPaPanel.SetSizer(self.add_patten_para_lay(self.ParaPaPanel))

    self.ParaNoteb.AddPage(self.ParaStPanel, "行情参数")
    self.ParaNoteb.AddPage(self.ParaBtPanel, "回测参数")
    # self.ParaNoteb.AddPage(self.ParaPtPanel, "条件选股")
    # self.ParaNoteb.AddPage(self.ParaPaPanel, "形态选股")

    return self.ParaNoteb
