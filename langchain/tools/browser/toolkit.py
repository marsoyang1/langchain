"""Playwright web browser toolkit."""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Type

from pydantic import Extra, Field, root_validator

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools.base import BaseTool
from langchain.tools.browser.base import BaseBrowserTool
from langchain.tools.browser.click import ClickTool
from langchain.tools.browser.extract_hyperlinks import ExtractHyperlinksTool
from langchain.tools.browser.extract_text import ExtractTextTool
from langchain.tools.browser.get_elements import GetElementsTool
from langchain.tools.browser.navigate import NavigateTool
from langchain.tools.browser.navigate_back import NavigateBackTool
from langchain.tools.browser.utils import create_playwright_browser

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser


class BrowserToolkit(BaseToolkit):
    """Toolkit for web browser tools."""

    browser: AsyncBrowser = Field(default_factory=create_playwright_browser)

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @root_validator
    def check_args(cls, values: dict) -> dict:
        """Check that the arguments are valid."""
        try:
            from playwright.async_api import Browser as AsyncBrowser  # noqa: F401
        except ImportError:
            raise ValueError(
                "The 'playwright' package is required to use this tool."
                " Please install it with 'pip install playwright'."
            )
        return values

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        tool_classes: List[Type[BaseBrowserTool]] = [
            ClickTool,
            NavigateTool,
            NavigateBackTool,
            ExtractTextTool,
            ExtractHyperlinksTool,
            GetElementsTool,
        ]

        return [tool_cls.from_browser(self.browser) for tool_cls in tool_classes]

    @classmethod
    def from_browser(cls, browser: AsyncBrowser) -> BrowserToolkit:
        from playwright.async_api import Browser as AsyncBrowser

        cls.update_forward_refs(AsyncBrowser=AsyncBrowser)
        return cls(browser=browser)