# -*- coding: utf-8 -*-
"""
icz.modeless - minimal modeless ExternalEvent plumbing for pyRevit windows.
Part of the icz BIM tool suite.
Author: icz

A modeless WPF window (.Show()) returns control to Revit immediately, so its
event handlers run OUTSIDE a valid Revit API context - any model/view change
made straight from a button click throws "...outside of transaction" or is
silently ignored. The supported pattern is to hand the work to an ExternalEvent
whose Execute runs on Revit's main thread in a valid API context.

This wraps that in one reusable class, so a window doesn't need a bespoke
IExternalEventHandler per action: build the callback inline (it closes over
whatever it needs) and raise it.

    self.nav = ExternalCall("Navigate")        # create in __init__ (valid ctx)
    ...
    def zoom(self, ids):
        def _do(uiapp):                         # runs in a valid API context
            uidoc = uiapp.ActiveUIDocument
            coll = List[ElementId](ids)
            uidoc.Selection.SetElementIds(coll)
            uidoc.ShowElements(coll)
        self.nav.raise_with(_do)

NOTE: the host *script* must also set  __persistentengine__ = True  at module
level, or pyRevit disposes the engine once .Show() returns and every later
callback fires against a dead engine (CTD / silent no-op). ExternalEvent.Create
must be called from a valid context (e.g. the window __init__ during the run).
"""
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent


class _CallbackHandler(IExternalEventHandler):
    def __init__(self, name):
        self._name = name
        self.callback = None        # function(uiapp) -> None

    def Execute(self, uiapp):
        cb = self.callback
        if cb is None:
            return
        try:
            cb(uiapp)
        except Exception as ex:
            # Never let an exception escape Execute - that crashes Revit.
            try:
                from pyrevit import forms
                forms.alert("{} failed:\n{}".format(self._name, ex), title=self._name)
            except:
                pass

    def GetName(self):
        return self._name


class ExternalCall(object):
    """Wrap an inline callback as a raisable ExternalEvent.

    Create instances from a valid Revit API context (typically a window
    __init__ that runs during script execution, before .Show() returns)."""

    def __init__(self, name="icz external call"):
        self.handler = _CallbackHandler(name)
        self.event = ExternalEvent.Create(self.handler)

    def raise_with(self, callback):
        """Queue callback(uiapp) to run on Revit's main thread (valid context).
        The latest callback wins if raised again before Revit goes idle."""
        self.handler.callback = callback
        return self.event.Raise()
