#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Multicast Python Module
# ..................................
# Copyright (c) 2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides consistent CI/CD output formatting for GitHub Actions.

This module implements a self-contained logging tool that formats output for GitHub Actions
workflows, supporting both annotation format and GitHub-flavored markdown summaries without
requiring any additional setup.

Classes:
	GithubActionsFormatter: Custom formatter for GitHub Actions annotations.
	MarkdownFormatter: Custom formatter for GitHub-flavored markdown output.
	ColorizedConsoleFormatter: Enhanced console formatter with color support.
	CIOutputTool: Main tool class for handling CI/CD output formatting.

Functions:
	configure_logging: Set up logging with appropriate handlers and formatters.
	main: CLI entry point for the tool.

Minimal Acceptance Testing:

	First set up test fixtures by importing modules.

	Testcase 0: Module should be importable.

		>>> import cioutput
		>>> cioutput.__doc__ is not None
		True
		>>>

	Testcase 1: Creating a basic logger should work.
		>>> import cioutput
		>>> import logging
		>>> logger = logging.getLogger("test")
		>>> logger is not None
		True
		>>>

	Testcase 2: Different formatters should be available.
		>>> import cioutput
		>>> gha_fmt = cioutput.GithubActionsFormatter()
		>>> md_fmt = cioutput.MarkdownFormatter()
		>>> console_fmt = cioutput.ColorizedConsoleFormatter()
		>>> all([gha_fmt, md_fmt, console_fmt])
		True
		>>>
"""

import os
import sys
import logging
import argparse
from enum import Enum, auto
from typing import Optional

# Module initialization
__module__ = os.path.basename(__file__)
module_logger = logging.getLogger(__name__)


class OutputFormat(Enum):
	"""Enum for supported output formats."""
	CONSOLE = auto()
	GHA = auto()  # GitHub Actions annotations
	MARKDOWN = auto()  # GitHub-flavored markdown


class LogLevel(Enum):
	"""Enum mapping between log level names and logging module levels."""
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	CRITICAL = logging.CRITICAL


class GithubActionsFormatter(logging.Formatter):
	"""Formatter for GitHub Actions annotation format.

	Creates log output compatible with GitHub Actions workflow commands
	for creating annotations viewable in the GitHub UI.
	"""

	# Map between log levels and GitHub Actions annotation types
	LEVEL_MAPPING = {
		logging.DEBUG: "debug",
		logging.INFO: "notice",
		logging.WARNING: "warning",
		logging.ERROR: "error",
		logging.CRITICAL: "error"
	}

	def format(self, record: logging.LogRecord) -> str:
		"""Format the log record as a GitHub Actions annotation.

		Args:
			record: The log record to format

		Returns:
			Formatted string in GitHub Actions annotation format
		"""
		# Extract file/line info if available in extra attributes
		is_boundary = getattr(record, "is_boundary", False)
		message = super().format(record)

		if is_boundary:
			return self._format_boundary(message)

		annotation_level = self.LEVEL_MAPPING.get(record.levelno, "notice")
		command = self._create_annotation_command(record, annotation_level)
		return f"{command}:: {message}"

	def _format_boundary(self, message: str) -> str:
		"""Format the boundary message for GitHub Actions.

		Args:
			message: The log message

		Returns:
			Formatted boundary string
		"""
		if message:
			return f"::group::{message}"
		return "::endgroup::"

	def _create_annotation_command(self, record: logging.LogRecord, annotation_level: str) -> str:
		"""Create the annotation command based on the log record.

		Args:
			record: The log record
			annotation_level: The level of the annotation

		Returns:
			The constructed annotation command
		"""
		command = f"::{annotation_level}"
		if annotation_level != "debug":
			command += self._add_location_parameters(record)
			command += self._add_title_parameter(record)
		return command

	def _add_location_parameters(self, record: logging.LogRecord) -> str:
		"""Add location parameters to the annotation command.

		Args:
			record: The log record

		Returns:
			Location parameters as a string
		"""
		params = []
		file_path = getattr(record, "file_path", None)
		line_num = getattr(record, "line_num", None)
		end_line_num = getattr(record, "end_line_num", None)
		col_num = getattr(record, "col_num", None)
		end_col_num = getattr(record, "end_col_num", None)
		if file_path:
			params.append(f" file={file_path}")
			if line_num:
				params.append(f"line={line_num}")
				if end_line_num:
					params.append(f"endLine={end_line_num}")
				if col_num:
					params.append(f"col={col_num}")
					if end_col_num:
						params.append(f"endCol={end_col_num}")
		return ",".join(params) if params else ""

	def _add_title_parameter(self, record: logging.LogRecord) -> str:
		"""Add the title parameter to the annotation command.

		Args:
			record: The log record

		Returns:
			Title parameter as a string
		"""
		title = getattr(record, "title", None)
		if title:
			return f",title={title}" if getattr(record, "file_path", None) else f" title={title}"
		return ""


class MarkdownFormatter(logging.Formatter):
	"""Formatter for GitHub-flavored markdown output.

	Creates log output formatted as GitHub-flavored markdown, suitable
	for GitHub Actions workflow summaries.
	"""

	# Map between log levels and markdown formatting
	LEVEL_MAPPING = {
		logging.DEBUG: (":speech_balloon:", "NOTE"),
		logging.INFO: (":information_source:", "NOTE"),
		logging.WARNING: (":warning:", "WARNING"),
		logging.ERROR: (":x:", "CAUTION"),
		logging.CRITICAL: (":fire:", "CAUTION")
	}

	def format(self, record: logging.LogRecord) -> str:
		"""Format the log record as GitHub-flavored markdown.

		Args:
			record: The log record to format

		Returns:
			Formatted string in GitHub-flavored markdown
		"""
		# Get the icon and level name
		icon, level_name = self.LEVEL_MAPPING.get(
			record.levelno, (":information_source:", "Info")
		)
		is_boundary = getattr(record, "is_boundary", False)
		# Format the basic message
		message = super().format(record)
		if is_boundary:
			if message and (len(message) > 0):
				return f"<details><summary>{message}</summary>\n"
			else:
				return "</details>"
		# Extract file/line info if available in extra attributes
		title_info = ""
		title = getattr(record, "title", None)
		file_info = ""
		file_path = getattr(record, "file_path", None)
		line_num = getattr(record, "line_num", None)
		end_line_num = getattr(record, "end_line_num", None)
		if title:
			title_info = f"**{title}**{icon}\n> "
		if file_path:
			file_info = f"\n> :file_folder: `{file_path}`"
			if line_num:
				file_info += f":{line_num}"
				if end_line_num:
					file_info += f"-{end_line_num}"
		# Format as markdown
		return f"> [!{level_name}]\n> {title_info}{message}{file_info}"


class ColorizedConsoleFormatter(logging.Formatter):
	"""Enhanced console formatter with color support.

	Creates log output with ANSI color codes for better readability
	in terminal environments.
	"""

	# ANSI color codes for different log levels
	COLORS = {
		logging.DEBUG: "\033[35m",      # Purple
		logging.INFO: "\033[32m",       # Green
		logging.WARNING: "\033[33m",    # Yellow
		logging.ERROR: "\033[31m",      # Red
		logging.CRITICAL: "\033[31m",   # Red
	}
	RESET = "\033[0m"

	def format(self, record: logging.LogRecord) -> str:
		"""Format the log record with colored output for console.

		Args:
			record: The log record to format

		Returns:
			Formatted string with ANSI color codes
		"""
		# Check if output is a terminal before using colors
		use_colors = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
		is_boundary = getattr(record, "is_boundary", False)
		# Format the basic message
		message = super().format(record)
		if is_boundary:
			return f"[START] {message}" if message else "[ END ]"
		if use_colors:
			# Get the color code for this level
			color = self.COLORS.get(record.levelno, self.RESET)
			level_name = logging.getLevelName(record.levelno)
			return f"{color}[{level_name}]{self.RESET} {message}"
		else:
			# No colors for non-terminal output
			level_name = logging.getLevelName(record.levelno)
			return f"[{level_name}] {message}"


class CIOutputTool:
	"""Main tool class for handling CI/CD output formatting.

	Provides methods for configuring and using different output formats
	for CI/CD workflows, particularly focused on GitHub Actions.
	"""

	def __init__(
		self,
		format_type: OutputFormat = OutputFormat.CONSOLE,
		log_level: LogLevel = LogLevel.INFO
	):
		"""Initialize the CI output tool.

		Args:
			format_type: The output format to use
			log_level: The minimum log level to display
		"""
		self.format_type = format_type
		self.log_level = log_level.value
		self.logger = self._configure_logging()

	def _configure_logging(self) -> logging.Logger:
		"""Set up logging with appropriate handlers and formatters.

		Returns:
			Configured logger instance
		"""
		# Create logger
		logger = logging.getLogger("cioutput")
		logger.setLevel(self.log_level)
		# Clear any existing handlers
		for handler in logger.handlers[:]:
			logger.removeHandler(handler)
		# Create formatter based on format type
		if self.format_type == OutputFormat.GHA:
			formatter = GithubActionsFormatter()
		elif self.format_type == OutputFormat.MARKDOWN:
			formatter = MarkdownFormatter()
		else:
			formatter = ColorizedConsoleFormatter()
		# Create and configure stdout handler
		stdout_handler = logging.StreamHandler(sys.stdout)
		stdout_handler.setFormatter(formatter)
		# Only output INFO and below to stdout
		stdout_handler.setLevel(self.log_level)
		stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
		logger.addHandler(stdout_handler)
		# Create and configure stderr handler for ERROR and above
		stderr_handler = logging.StreamHandler(sys.stderr)
		stderr_handler.setFormatter(formatter)
		stderr_handler.setLevel(logging.ERROR)
		logger.addHandler(stderr_handler)
		return logger

	def update_github_env(self, key: str, value: str) -> None:
		"""Update GitHub Actions environment variables.

		Uses GitHub Actions environment files to set environment variables
		that persist between steps.

		Args:
			key: Environment variable name
			value: Environment variable value
		"""
		if "GITHUB_ENV" in os.environ:
			with open(os.environ["GITHUB_ENV"], "a") as env_file:
				env_file.write(f"{key}={value}\n")

	def add_to_summary(self, content: str) -> None:
		"""Add content to GitHub Actions job summary.

		Appends the provided content to the GitHub Actions job summary file
		if running in a GitHub Actions environment.

		Args:
			content: Markdown content to add to the summary
		"""
		if "GITHUB_STEP_SUMMARY" in os.environ:
			with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary_file:
				summary_file.write(f"{content}\n")

	def log(
		self,
		message: str,
		level: LogLevel = LogLevel.INFO,
		is_boundary: Optional[bool] = None,
		title: Optional[str] = None,
		file_path: Optional[str] = None,
		line_num: Optional[int] = None,
		end_line_num: Optional[int] = None,
		col_num: Optional[int] = None,
		end_col_num: Optional[int] = None
	) -> None:
		"""Log a message with the configured formatter.

		Args:
			message: Message to log
			level: Log level to use
			group: Optional title for annotations
			title: Optional title for annotations
			file_path: Optional file path for annotations
			line_num: Optional line number for annotations
			end_line_num: Optional end-line number for annotations
			col_num: Optional column number for annotations
			end_col_num: Optional end-column number for annotations
		"""
		extra = self._build_extra_info(
			is_boundary, title, file_path,
			line_num, end_line_num, col_num, end_col_num,
		)
		self._log_message(message, level, extra)
		self._handle_github_actions_summary(level, message, file_path, line_num, extra)

	def _build_extra_info(
		self,
		is_boundary: Optional[bool],
		title: Optional[str],
		file_path: Optional[str],
		line_num: Optional[int],
		end_line_num: Optional[int],
		col_num: Optional[int],
		end_col_num: Optional[int]
	) -> dict:
		"""Build extra information for logging."""
		extra = {}
		if is_boundary is not None:
			extra["is_boundary"] = is_boundary
		if title:
			extra["title"] = title
		if file_path:
			extra["file_path"] = file_path
		if line_num is not None:
			extra["line_num"] = line_num
		if end_line_num is not None:
			extra["end_line_num"] = end_line_num
		if col_num is not None:
			extra["col_num"] = col_num
		if end_col_num is not None:
			extra["end_col_num"] = end_col_num
		return extra

	def _log_message(self, message: str, level: LogLevel, extra: dict) -> None:
		"""Log the message with the specified level and extra information."""
		self.logger.log(level.value, message, extra=extra if extra else None)

	def _handle_github_actions_summary(
		self,
		level: LogLevel,
		message: str,
		file_path: Optional[str],
		line_num: Optional[int],
		extra: dict
	) -> None:
		"""Handle logging for GitHub Actions summary."""
		if level.value >= logging.ERROR and self.format_type == OutputFormat.MARKDOWN:
			if "GITHUB_STEP_SUMMARY" in os.environ:
				md_formatter = MarkdownFormatter()
				record = logging.LogRecord(
					name=self.logger.name,
					level=level.value,
					pathname=file_path or "",
					lineno=line_num or 0,
					msg=message,
					args=(),
					exc_info=None
				)
				for key, value in extra.items():
					setattr(record, key, value)
				self.add_to_summary(md_formatter.format(record))

	def debug(self, message: str, **kwargs) -> None:
		"""Log a debug message.

		Args:
			message: Debug message to log
			**kwargs: Additional parameters (title, file_path, line_num, col_num)
		"""
		self.log(message, LogLevel.DEBUG, **kwargs)

	def info(self, message: str, **kwargs) -> None:
		"""Log an info message.

		Args:
			message: Info message to log
			**kwargs: Additional parameters (title, file_path, line_num, col_num)
		"""
		self.log(message, LogLevel.INFO, **kwargs)

	def warning(self, message: str, **kwargs) -> None:
		"""Log a warning message.

		Args:
			message: Warning message to log
			**kwargs: Additional parameters (title, file_path, line_num, col_num)
		"""
		self.log(message, LogLevel.WARNING, **kwargs)

	def error(self, message: str, **kwargs) -> None:
		"""Log an error message.

		Args:
			message: Error message to log
			**kwargs: Additional parameters (title, file_path, line_num, col_num)
		"""
		self.log(message, LogLevel.ERROR, **kwargs)

	def critical(self, message: str, **kwargs) -> None:
		"""Log a critical message.

		Args:
			message: Critical message to log
			**kwargs: Additional parameters (title, file_path, line_num, col_num)
		"""
		self.log(message, LogLevel.CRITICAL, **kwargs)


def detect_github_actions() -> bool:
	"""Detect if running in GitHub Actions environment.

	Returns:
		True if running in GitHub Actions, False otherwise
	"""
	return "GITHUB_ACTIONS" in os.environ and os.environ.get("GITHUB_ACTIONS") == "true"


def configure_output_tool() -> CIOutputTool:
	"""Parse command-line arguments and configure the output tool.

	Returns:
		Configured CIOutputTool instance
	"""
	parser = argparse.ArgumentParser(
		description="CI/CD output formatting tool for GitHub Actions",
	)
	parser.add_argument(
		"-f", "--format",
		choices=["auto", "console", "gha", "markdown"],
		default="auto",
		help="Output format (auto detects GHA environment if not specified)"
	)
	parser.add_argument(
		"-l", "--level",
		choices=["debug", "info", "warning", "error", "critical"],
		default="info",
		help="Log level for the message (if provided)"
	)
	parser.add_argument(
		"message",
		nargs="?",
		help="Optional message to log"
	)
	parser.add_argument(
		"-t", "--title",
		help="File path for GitHub Actions annotations"
	)
	parser.add_argument(
		"--file",
		help="File path for GitHub Actions annotations"
	)
	group = parser.add_argument_group()
	lineSubGroup = group.add_mutually_exclusive_group(required=False)
	colSubGroup = group.add_mutually_exclusive_group(required=False)
	lineSubGroup.add_argument(
		"--line",
		dest="line",
		type=int,
		metavar="LINE",
		help="Line number for GitHub Actions annotations"
	)
	lineSubGroup.add_argument(
		"--start-line",
		dest="line",
		type=int,
		metavar="START_LINE",
		help="Line number for GitHub Actions annotations"
	)
	colSubGroup.add_argument(
		"--col",
		dest="col",
		type=int,
		metavar="COL",
		help="Column number for GitHub Actions annotations"
	)
	colSubGroup.add_argument(
		"--start-col",
		dest="col",
		type=int,
		metavar="START_COL",
		help="Column number for GitHub Actions annotations"
	)
	group.add_argument(
		"--end-line",
		dest="end_line",
		type=int,
		help="End line number for GitHub Actions annotations"
	)
	group.add_argument(
		"--end-col",
		dest="end_col",
		type=int,
		metavar="END_COL",
		help="End column number for GitHub Actions annotations"
	)
	parser.add_argument(
		"--log-level",
		choices=["debug", "info", "warning", "error", "critical"],
		default="info",
		help="Minimum log level to display"
	)
	parser.add_argument(
		"--group",
		dest="is_group",
		default=False,
		action="store_true",
		help="Optionally treat this as a group boundary. Ends if message is empty, otherwise starts"
	)
	args = parser.parse_args()
	# Determine output format
	if args.format == "auto":
		format_type = OutputFormat.GHA if detect_github_actions() else OutputFormat.CONSOLE
	elif args.format == "gha":
		format_type = OutputFormat.GHA
	elif args.format == "markdown":
		format_type = OutputFormat.MARKDOWN
	else:
		format_type = OutputFormat.CONSOLE
	# Determine log level
	log_level = getattr(LogLevel, args.log_level.upper())
	# Create and configure the tool
	tool = CIOutputTool(format_type, log_level)
	# Process message if provided
	if args.message or args.is_group:
		msg_level = getattr(LogLevel, args.level.upper())
		tool.log(
			args.message if args.message else "",
			level=msg_level,
			is_boundary=args.is_group,
			title=args.title,
			file_path=args.file,
			line_num=args.line,
			end_line_num=args.end_line,
			col_num=args.col,
			end_col_num=args.end_col,
		)
	return tool


def main() -> int:
	"""Main function for CLI usage.

	Returns:
		Exit code (0 for success, non-zero for failure)
	"""
	try:
		tool = configure_output_tool()
		if tool:
			return 0
	except Exception as _cause:  # pragma: no branch
		print(f"Error initializing CI output tool: {_cause}", file=sys.stderr)
	return 1


if __name__ == "__main__":
	sys.exit(main())
